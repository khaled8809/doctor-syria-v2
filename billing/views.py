import tempfile

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
# تعطيل مؤقتاً
# from weasyprint import HTML

from .models import (
    FaturaPayment,
    InsuranceClaim,
    InsuranceProvider,
    Invoice,
    InvoiceItem,
    Payment,
)
from .serializers import (
    InsuranceClaimSerializer,
    InsuranceProviderSerializer,
    InvoiceItemSerializer,
    InvoicePDFSerializer,
    InvoiceSerializer,
    PaymentSerializer,
)
from .services import FaturaService, StripeService


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
        elif hasattr(user, "doctor"):
            return queryset.filter(doctor=user.doctor)
        elif hasattr(user, "patient"):
            return queryset.filter(patient=user.patient)
        return queryset.none()

    @action(detail=True, methods=["post"])
    def add_item(self, request, pk=None):
        """إضافة عنصر للفاتورة"""
        invoice = self.get_object()
        serializer = InvoiceItemSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(invoice=invoice)
            invoice.calculate_total()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def process_payment(self, request, pk=None):
        """معالجة الدفع للفاتورة"""
        invoice = self.get_object()
        payment_method = request.data.get("payment_method")
        amount = request.data.get("amount")

        if not payment_method or not amount:
            return Response(
                {"error": "Payment method and amount are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            payment = Payment.objects.create(
                invoice=invoice,
                amount=amount,
                payment_method=payment_method,
                status="completed",
            )
            invoice.mark_as_paid(payment_method)

        return Response(
            {"message": "Payment processed successfully", "payment_id": payment.id}
        )

    @action(detail=True, methods=["get"])
    def generate_pdf(self, request, pk=None):
        """إنشاء PDF للفاتورة"""
        invoice = self.get_object()
        serializer = InvoicePDFSerializer(invoice)

        # تحضير قالب HTML
        html_string = render_to_string(
            "billing/invoice_template.html", {"invoice": serializer.data}
        )

        # إرجاع HTML مؤقتاً بدلاً من PDF
        response = HttpResponse(content_type="text/html")
        response[
            "Content-Disposition"
        ] = f"inline; filename=invoice_{invoice.invoice_number}.html"
        response.write(html_string)

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
        elif hasattr(user, "doctor"):
            return queryset.filter(invoice__doctor=user.doctor)
        elif hasattr(user, "patient"):
            return queryset.filter(invoice__patient=user.patient)
        return queryset.none()

    @action(detail=True, methods=["post"])
    def create_payment_intent(self, request, pk=None):
        """إنشاء نية دفع في Stripe"""
        payment = self.get_object()

        try:
            intent_data = StripeService.create_payment_intent(payment)
            return Response(intent_data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def confirm_payment(self, request, pk=None):
        """تأكيد الدفع"""
        payment = self.get_object()
        payment_intent_id = request.data.get("payment_intent_id")

        if not payment_intent_id:
            return Response(
                {"error": "Payment intent ID is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            success = StripeService.confirm_payment(payment_intent_id)
            if success:
                return Response({"message": "Payment confirmed successfully"})
            return Response(
                {"error": "Payment confirmation failed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def refund_payment(self, request, pk=None):
        """استرداد الدفع"""
        payment = self.get_object()

        try:
            success = StripeService.create_refund(payment)
            if success:
                return Response({"message": "Payment refunded successfully"})
            return Response(
                {"error": "Refund failed"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def create_fatura_payment(self, request, pk=None):
        """إنشاء دفع عبر Fatura"""
        payment = self.get_object()

        try:
            # إنشاء دفع في Fatura
            fatura_data = FaturaService.create_payment(payment)

            # حفظ معلومات الدفع
            FaturaPayment.objects.create(
                payment=payment,
                transaction_id=fatura_data["transaction_id"],
                payment_url=fatura_data["payment_url"],
            )

            return Response(
                {
                    "message": "Fatura payment created successfully",
                    "payment_url": fatura_data["payment_url"],
                }
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def verify_fatura_payment(self, request, pk=None):
        """التحقق من حالة الدفع في Fatura"""
        payment = self.get_object()

        try:
            fatura_payment = payment.fatura_payment
            status_data = FaturaService.check_payment_status(
                fatura_payment.transaction_id
            )

            if status_data["status"] == "completed":
                payment.status = "completed"
                payment.save()
                return Response({"message": "Payment verified successfully"})

            return Response({"status": status_data["status"]})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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

    def get_queryset(self):
        """تخصيص الاستعلام حسب نوع المستخدم"""
        queryset = super().get_queryset()
        user = self.request.user

        if user.is_staff:
            return queryset
        elif hasattr(user, "doctor"):
            return queryset.filter(invoice__doctor=user.doctor)
        elif hasattr(user, "patient"):
            return queryset.filter(invoice__patient=user.patient)
        return queryset.none()

    @action(detail=True, methods=["post"])
    def process_claim(self, request, pk=None):
        """معالجة مطالبة التأمين"""
        claim = self.get_object()
        status = request.data.get("status")
        notes = request.data.get("notes")

        if not status:
            return Response(
                {"error": "Status is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        claim.status = status
        claim.notes = notes
        claim.processed_at = timezone.now()
        claim.save()

        return Response({"message": "Claim processed successfully"})


class StripeWebhookView(viewsets.ViewSet):
    """معالجة Webhook من Stripe"""

    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """معالجة الإشعار من Stripe"""
        payload = request.body
        sig_header = request.headers.get("stripe-signature")

        try:
            event = StripeService.construct_webhook_event(payload, sig_header)
            return Response({"status": "success"})
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class FaturaWebhookView(viewsets.ViewSet):
    """معالجة Webhook من Fatura"""

    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """معالجة الإشعار من Fatura"""
        try:
            # التحقق من صحة التوقيع
            signature = request.headers.get("x-fatura-signature")
            if not FaturaService.verify_webhook_signature(
                request.body, signature
            ):
                raise PermissionDenied("Invalid signature")

            # معالجة الإشعار
            data = request.data
            transaction_id = data.get("transaction_id")
            status = data.get("status")

            if not transaction_id or not status:
                return Response(
                    {"error": "Missing required fields"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # تحديث حالة الدفع
            fatura_payment = get_object_or_404(
                FaturaPayment, transaction_id=transaction_id
            )
            payment = fatura_payment.payment

            if status == "completed":
                payment.status = "completed"
                payment.save()

                # تحديث حالة الفاتورة
                invoice = payment.invoice
                invoice.mark_as_paid("fatura")

            elif status == "failed":
                payment.status = "failed"
                payment.save()

            return Response({"status": "success"})

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Sum
from django.utils import timezone


@login_required
def dashboard(request):
    """لوحة تحكم المدفوعات"""
    # إحصائيات عامة
    total_invoices = Invoice.objects.count()
    total_payments = Payment.objects.filter(status="completed").count()
    total_revenue = Payment.objects.filter(status="completed").aggregate(
        Sum("amount")
    )["amount__sum"] or 0

    # إحصائيات حسب طريقة الدفع
    payment_methods = (
        Payment.objects.filter(status="completed")
        .values("payment_method")
        .annotate(
            count=Count("id"),
            total=Sum("amount"),
            avg=Avg("amount"),
        )
    )

    # إحصائيات حسب الحالة
    status_stats = (
        Payment.objects.values("status")
        .annotate(count=Count("id"), total=Sum("amount"))
        .order_by("status")
    )

    # إحصائيات شهرية
    monthly_stats = (
        Payment.objects.filter(status="completed")
        .extra(select={"month": "EXTRACT(month FROM created_at)"})
        .values("month")
        .annotate(count=Count("id"), total=Sum("amount"))
        .order_by("month")
    )

    # الفواتير الأخيرة
    latest_invoices = Invoice.objects.select_related(
        "patient", "doctor"
    ).order_by("-created_at")[:10]

    # المدفوعات الأخيرة
    latest_payments = Payment.objects.select_related(
        "invoice", "invoice__patient"
    ).order_by("-created_at")[:10]

    # مطالبات التأمين
    insurance_claims = InsuranceClaim.objects.select_related(
        "invoice",
        "insurance_provider",
        "invoice__patient",
    ).order_by("-created_at")[:10]

    # إحصائيات التأمين
    insurance_stats = (
        InsuranceClaim.objects.values("status")
        .annotate(count=Count("id"), total=Sum("amount"))
        .order_by("status")
    )

    context = {
        "total_invoices": total_invoices,
        "total_payments": total_payments,
        "total_revenue": total_revenue,
        "payment_methods": payment_methods,
        "status_stats": status_stats,
        "monthly_stats": monthly_stats,
        "latest_invoices": latest_invoices,
        "latest_payments": latest_payments,
        "insurance_claims": insurance_claims,
        "insurance_stats": insurance_stats,
    }

    return render(request, "billing/dashboard.html", context)


@login_required
def payment_form(request, payment_id):
    """عرض نموذج الدفع"""
    payment = get_object_or_404(Payment, id=payment_id)

    # التحقق من الصلاحيات
    user = request.user
    if not user.is_staff:
        if hasattr(user, "doctor") and payment.invoice.doctor != user.doctor:
            raise PermissionDenied()
        elif (
            hasattr(user, "patient")
            and payment.invoice.patient != user.patient
        ):
            raise PermissionDenied()

    context = {
        "payment": payment,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    }

    return render(request, "billing/payment_form.html", context)
