from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    TemplateView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q, Count
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

from .models import Test, TestRequest, TestResult, LabEquipment, QualityControl
from .forms import (
    TestForm, TestRequestForm, TestResultForm, LabEquipmentForm,
    QualityControlForm, TestSearchForm, TestRequestSearchForm,
    DateRangeForm
)

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# Test Views
class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'laboratory/test_list.html'
    context_object_name = 'tests'
    paginate_by = 10

    def get_queryset(self):
        queryset = Test.objects.all()
        form = TestSearchForm(self.request.GET)
        
        if form.is_valid():
            search = form.cleaned_data.get('search')
            category = form.cleaned_data.get('category')
            is_active = form.cleaned_data.get('is_active')
            
            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(code__icontains=search) |
                    Q(description__icontains=search)
                )
            if category:
                queryset = queryset.filter(category=category)
            if is_active:
                queryset = queryset.filter(is_active=True)
                
        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TestSearchForm(self.request.GET)
        return context

class TestDetailView(LoginRequiredMixin, DetailView):
    model = Test
    template_name = 'laboratory/test_detail.html'
    context_object_name = 'test'

class TestCreateView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = 'laboratory/test_form.html'
    success_url = reverse_lazy('laboratory:test-list')
    success_message = _('تم إضافة التحليل بنجاح')

class TestUpdateView(LoginRequiredMixin, StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Test
    form_class = TestForm
    template_name = 'laboratory/test_form.html'
    success_url = reverse_lazy('laboratory:test-list')
    success_message = _('تم تحديث التحليل بنجاح')

class TestDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Test
    template_name = 'laboratory/test_confirm_delete.html'
    success_url = reverse_lazy('laboratory:test-list')
    success_message = _('تم حذف التحليل بنجاح')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

# Test Request Views
class TestRequestListView(LoginRequiredMixin, ListView):
    model = TestRequest
    template_name = 'laboratory/request_list.html'
    context_object_name = 'requests'
    paginate_by = 10

    def get_queryset(self):
        queryset = TestRequest.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(patient=self.request.user) |
                Q(doctor=self.request.user)
            )
            
        form = TestRequestSearchForm(self.request.GET)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            status = form.cleaned_data.get('status')
            priority = form.cleaned_data.get('priority')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            
            if search:
                queryset = queryset.filter(
                    Q(patient__first_name__icontains=search) |
                    Q(patient__last_name__icontains=search) |
                    Q(doctor__first_name__icontains=search) |
                    Q(doctor__last_name__icontains=search)
                )
            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if date_from:
                queryset = queryset.filter(requested_at__date__gte=date_from)
            if date_to:
                queryset = queryset.filter(requested_at__date__lte=date_to)
                
        return queryset.order_by('-requested_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = TestRequestSearchForm(self.request.GET)
        return context

class TestRequestDetailView(LoginRequiredMixin, DetailView):
    model = TestRequest
    template_name = 'laboratory/request_detail.html'
    context_object_name = 'request'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(patient=self.request.user) |
                Q(doctor=self.request.user)
            )
        return queryset

class TestRequestCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TestRequest
    form_class = TestRequestForm
    template_name = 'laboratory/request_form.html'
    success_url = reverse_lazy('laboratory:request-list')
    success_message = _('تم إنشاء طلب التحليل بنجاح')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.doctor = self.request.user
        return super().form_valid(form)

class TestRequestUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TestRequest
    form_class = TestRequestForm
    template_name = 'laboratory/request_form.html'
    success_url = reverse_lazy('laboratory:request-list')
    success_message = _('تم تحديث طلب التحليل بنجاح')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(doctor=self.request.user)
        return queryset

class TestRequestDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = TestRequest
    template_name = 'laboratory/request_confirm_delete.html'
    success_url = reverse_lazy('laboratory:request-list')
    success_message = _('تم حذف طلب التحليل بنجاح')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class TestRequestProcessView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = TestRequest
    template_name = 'laboratory/request_process.html'
    fields = ['status']
    success_url = reverse_lazy('laboratory:request-list')

    def form_valid(self, form):
        request = form.save(commit=False)
        request.processed_by = self.request.user
        if request.status == 'completed':
            request.completed_at = timezone.now()
        request.save()
        messages.success(self.request, _('تم تحديث حالة الطلب بنجاح'))
        return super().form_valid(form)

# Test Result Views
class TestResultListView(LoginRequiredMixin, ListView):
    model = TestResult
    template_name = 'laboratory/result_list.html'
    context_object_name = 'results'
    paginate_by = 10

    def get_queryset(self):
        queryset = TestResult.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(test_request__patient=self.request.user) |
                Q(test_request__doctor=self.request.user)
            )
        return queryset.order_by('-performed_at')

class TestResultDetailView(LoginRequiredMixin, DetailView):
    model = TestResult
    template_name = 'laboratory/result_detail.html'
    context_object_name = 'result'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                Q(test_request__patient=self.request.user) |
                Q(test_request__doctor=self.request.user)
            )
        return queryset

class TestResultPDFView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        result = get_object_or_404(TestResult, pk=kwargs['pk'])
        
        if not request.user.is_staff and request.user not in [
            result.test_request.patient,
            result.test_request.doctor
        ]:
            messages.error(request, _('ليس لديك صلاحية لعرض هذه النتيجة'))
            return redirect('laboratory:result-list')

        # إنشاء محتوى PDF
        html_string = render_to_string(
            'laboratory/result_pdf.html',
            {'result': result}
        )
        
        # تحويل HTML إلى PDF
        html = HTML(string=html_string)
        result = html.write_pdf()

        # إنشاء استجابة HTTP
        response = HttpResponse(content_type='application/pdf;')
        response['Content-Disposition'] = f'inline; filename=result_{result.pk}.pdf'
        response['Content-Transfer-Encoding'] = 'binary'
        
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())

        return response

# Report Views
class LaboratoryReportView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'laboratory/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # إحصائيات عامة
        context['total_tests'] = Test.objects.count()
        context['total_requests'] = TestRequest.objects.count()
        context['pending_requests'] = TestRequest.objects.filter(
            status='pending'
        ).count()
        context['completed_requests'] = TestRequest.objects.filter(
            status='completed'
        ).count()
        
        # التحاليل الأكثر طلباً
        context['popular_tests'] = Test.objects.annotate(
            request_count=Count('requests')
        ).order_by('-request_count')[:5]
        
        # المعدات التي تحتاج صيانة
        context['maintenance_equipment'] = LabEquipment.objects.filter(
            next_maintenance__lte=timezone.now().date()
        )
        
        return context

class DailyReportView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'laboratory/daily_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now().date()
        
        context['today_requests'] = TestRequest.objects.filter(
            requested_at__date=today
        )
        context['today_results'] = TestResult.objects.filter(
            performed_at__date=today
        )
        context['today_revenue'] = sum(
            request.get_total_price() for request in context['today_requests']
        )
        
        return context

class MonthlyReportView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'laboratory/monthly_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        form = DateRangeForm(self.request.GET)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            
            requests = TestRequest.objects.filter(
                requested_at__date__range=[date_from, date_to]
            )
            results = TestResult.objects.filter(
                performed_at__date__range=[date_from, date_to]
            )
            
            context.update({
                'date_from': date_from,
                'date_to': date_to,
                'requests': requests,
                'results': results,
                'total_revenue': sum(request.get_total_price() for request in requests),
                'total_tests': results.count(),
            })
        
        context['form'] = form
        return context

# Search View
class LaboratorySearchView(LoginRequiredMixin, TemplateView):
    template_name = 'laboratory/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        if query:
            tests = Test.objects.filter(
                Q(name__icontains=query) |
                Q(code__icontains=query) |
                Q(description__icontains=query)
            )
            
            requests = TestRequest.objects.filter(
                Q(patient__first_name__icontains=query) |
                Q(patient__last_name__icontains=query) |
                Q(doctor__first_name__icontains=query) |
                Q(doctor__last_name__icontains=query)
            )
            
            if not self.request.user.is_staff:
                requests = requests.filter(
                    Q(patient=self.request.user) |
                    Q(doctor=self.request.user)
                )
            
            context.update({
                'query': query,
                'tests': tests[:10],
                'requests': requests[:10],
            })
            
        return context
