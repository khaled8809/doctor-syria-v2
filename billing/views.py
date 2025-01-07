from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

from .models import Invoice, InvoiceItem, Payment, InsuranceClaim, InsuranceProvider, FaturaPayment
from .serializers import (
    InvoiceSerializer, InvoiceItemSerializer, PaymentSerializer,
    InsuranceClaimSerializer, InsuranceProviderSerializer, InvoicePDFSerializer
)
from .services import StripeService, FaturaService
from django.conf import settings
from django.core.exceptions import PermissionDenied

class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet للفواتير"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """تخصيص الاستعلام حسب نوع المستخدم"""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff:
            return queryset
        elif hasattr(user, 'doctor'):
            return queryset.filter(doctor=user.doctor)
        elif hasattr(user, 'patient'):
            return queryset.filter(patient=user.patient)
        return queryset.none()

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        """إضافة عنصر للفاتورة"""
        invoice = self.get_object()
        serializer = InvoiceItemSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(invoice=invoice)
            invoice.calculate_total()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        """معالجة الدفع للفاتورة"""
        invoice = self.get_object()
        payment_method = request.data.get('payment_method')
        amount = request.data.get('amount')

        if not payment_method or not amount:
            return Response(
                {'error': 'Payment method and amount are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            payment = Payment.objects.create(
                invoice=invoice,
                amount=amount,
                payment_method=payment_method,
                status='completed'
            )
            invoice.mark_as_paid(payment_method)

        return Response({
            'message': 'Payment processed successfully',
            'payment_id': payment.id
        })

    @action(detail=True, methods=['get'])
    def generate_pdf(self, request, pk=None):
        """إنشاء PDF للفاتورة"""
        invoice = self.get_object()
        serializer = InvoicePDFSerializer(invoice)
        
        # تحضير قالب HTML
        html_string = render_to_string(
            'billing/invoice_template.html',
            {'invoice': serializer.data}
        )

        # إنشاء PDF
        html = HTML(string=html_string)
        result = html.write_pdf()

        # إرجاع الملف
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=invoice_{invoice.invoice_number}.pdf'
        response.write(result)
        
        return response

class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet للمدفوعات"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """تخصيص الاستعلام حسب نوع المستخدم"""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff:
            return queryset
        elif hasattr(user, 'doctor'):
            return queryset.filter(invoice__doctor=user.doctor)
        elif hasattr(user, 'patient'):
            return queryset.filter(invoice__patient=user.patient)
        return queryset.none()

    @action(detail=True, methods=['post'])
    def create_payment_intent(self, request, pk=None):
        """إنشاء نية دفع في Stripe"""
        payment = self.get_object()
        
        try:
            intent_data = StripeService.create_payment_intent(payment)
            return Response(intent_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def confirm_payment(self, request, pk=None):
        """تأكيد الدفع"""
        payment = self.get_object()
        payment_intent_id = request.data.get('payment_intent_id')
        
        if not payment_intent_id:
            return Response(
                {'error': 'Payment intent ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            success = StripeService.confirm_payment(payment_intent_id)
            if success:
                return Response({'message': 'Payment confirmed successfully'})
            return Response(
                {'error': 'Payment confirmation failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def refund_payment(self, request, pk=None):
        """استرداد الدفع"""
        payment = self.get_object()
        
        try:
            success = StripeService.create_refund(payment)
            if success:
                return Response({'message': 'Payment refunded successfully'})
            return Response(
                {'error': 'Refund failed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def create_fatura_payment(self, request, pk=None):
        """إنشاء دفع عبر Fatura"""
        payment = self.get_object()
        
        try:
            # إنشاء دفع في Fatura
            fatura_data = FaturaService.create_payment(payment)
            
            # حفظ معلومات الدفع
            FaturaPayment.objects.create(
                payment=payment,
                transaction_id=fatura_data['transaction_id'],
                payment_url=fatura_data['payment_url']
            )
            
            return Response({
                'payment_url': fatura_data['payment_url']
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def verify_fatura_payment(self, request, pk=None):
        """التحقق من حالة الدفع في Fatura"""
        payment = self.get_object()
        
        try:
            fatura_payment = payment.fatura_payment
            result = FaturaService.verify_payment(fatura_payment.transaction_id)
            
            if result['status'] == 'completed':
                # تحديث حالة الدفع
                fatura_payment.status = 'completed'
                fatura_payment.payment_method = result['payment_method']
                fatura_payment.payment_time = result['payment_time']
                fatura_payment.save()
                
                # تحديث حالة الدفع الرئيسي
                payment.status = 'completed'
                payment.save()
                
                # تحديث حالة الفاتورة
                payment.invoice.status = 'paid'
                payment.invoice.save()
            
            return Response(result)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class InsuranceProviderViewSet(viewsets.ModelViewSet):
    """ViewSet لشركات التأمين"""
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer
    permission_classes = [permissions.IsAuthenticated]

class InsuranceClaimViewSet(viewsets.ModelViewSet):
    """ViewSet لمطالبات التأمين"""
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def process_claim(self, request, pk=None):
        """معالجة مطالبة التأمين"""
        claim = self.get_object()
        status = request.data.get('status')
        amount_approved = request.data.get('amount_approved')

        if not status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            claim.status = status
            if amount_approved:
                claim.amount_approved = amount_approved
            claim.processed_at = timezone.now()
            claim.save()

            # إذا تمت الموافقة على المطالبة، قم بتحديث الفاتورة
            if status == 'approved':
                invoice = claim.invoice
                invoice.status = 'paid'
                invoice.payment_method = 'insurance'
                invoice.save()

        return Response({'message': 'Claim processed successfully'})

class StripeWebhookView(views.APIView):
    """معالجة Webhook من Stripe"""
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            StripeService.handle_webhook(payload, sig_header)
            return Response({'status': 'success'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class FaturaWebhookView(views.APIView):
    """معالجة Webhook من Fatura"""
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        signature = request.headers.get('X-Signature')
        timestamp = request.headers.get('X-Timestamp')
        
        if not signature or not timestamp:
            return Response(
                {'error': 'Missing signature or timestamp'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # التحقق من صحة التوقيع
            if not FaturaService.verify_webhook_signature(signature, timestamp, request.data):
                return Response(
                    {'error': 'Invalid signature'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # معالجة الحدث
            event_type = request.data.get('eventType')
            transaction_id = request.data.get('transactionId')
            
            fatura_payment = get_object_or_404(FaturaPayment, transaction_id=transaction_id)
            payment = fatura_payment.payment
            
            if event_type == 'payment.completed':
                fatura_payment.status = 'completed'
                fatura_payment.payment_method = request.data.get('paymentMethod')
                fatura_payment.payment_time = request.data.get('paymentTime')
                fatura_payment.save()
                
                payment.status = 'completed'
                payment.save()
                
                payment.invoice.status = 'paid'
                payment.invoice.save()
                
            elif event_type == 'payment.failed':
                fatura_payment.status = 'failed'
                fatura_payment.save()
                
                payment.status = 'failed'
                payment.save()
            
            return Response({'status': 'success'})
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """لوحة تحكم المدفوعات"""
    # التحقق من الصلاحيات
    if not request.user.is_staff:
        raise PermissionDenied
    
    # الإحصائيات
    today = timezone.now()
    thirty_days_ago = today - timezone.timedelta(days=30)
    
    payments = Payment.objects.filter(created_at__gte=thirty_days_ago)
    total_payments = payments.count()
    completed_payments = payments.filter(status='completed').count()
    pending_payments = payments.filter(status='pending').count()
    
    completed_percentage = (completed_payments / total_payments * 100) if total_payments > 0 else 0
    pending_percentage = (pending_payments / total_payments * 100) if total_payments > 0 else 0
    
    average_payment = payments.filter(status='completed').aggregate(avg=Avg('amount'))['avg'] or 0
    
    # بيانات الرسم البياني للمدفوعات
    daily_payments = payments.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id'),
        total=Sum('amount')
    ).order_by('date')
    
    payments_data = {
        'labels': [p['date'].strftime('%Y-%m-%d') for p in daily_payments],
        'datasets': [{
            'label': 'عدد المدفوعات',
            'data': [p['count'] for p in daily_payments],
            'borderColor': '#0d6efd',
            'fill': False
        }, {
            'label': 'إجمالي المدفوعات',
            'data': [float(p['total']) for p in daily_payments],
            'borderColor': '#198754',
            'fill': False
        }]
    }
    
    # بيانات الرسم البياني لطرق الدفع
    payment_methods = payments.values('payment_method').annotate(
        count=Count('id')
    ).order_by('-count')
    
    payment_methods_data = {
        'labels': [p['payment_method'] for p in payment_methods],
        'datasets': [{
            'data': [p['count'] for p in payment_methods],
            'backgroundColor': [
                '#0d6efd', '#198754', '#ffc107', '#dc3545', '#6c757d'
            ]
        }]
    }
    
    # قائمة المدفوعات مع الترقيم
    all_payments = Payment.objects.all().order_by('-created_at')
    paginator = Paginator(all_payments, 10)
    page = request.GET.get('page')
    payments_list = paginator.get_page(page)
    
    context = {
        'total_payments': total_payments,
        'completed_payments': completed_payments,
        'pending_payments': pending_payments,
        'completed_percentage': round(completed_percentage, 1),
        'pending_percentage': round(pending_percentage, 1),
        'average_payment': round(average_payment, 2),
        'payments_data': payments_data,
        'payment_methods_data': payment_methods_data,
        'payments': payments_list
    }
    
    return render(request, 'billing/dashboard.html', context)

def payment_form(request, payment_id):
    """عرض نموذج الدفع"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # التحقق من أن المستخدم لديه حق الوصول للدفع
    if not request.user.is_staff:
        if hasattr(request.user, 'patient'):
            if payment.invoice.patient.user != request.user:
                raise PermissionDenied
        elif hasattr(request.user, 'doctor'):
            if payment.invoice.doctor.user != request.user:
                raise PermissionDenied
        else:
            raise PermissionDenied
    
    context = {
        'payment': payment,
        'invoice': payment.invoice,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'billing/payment_form.html', context)
