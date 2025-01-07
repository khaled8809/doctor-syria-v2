from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from .models import (
    Employee, Leave, Shift, Attendance, Payroll,
    Evaluation, Training
)
from .forms import (
    EmployeeForm, LeaveForm, ShiftForm, AttendanceForm,
    PayrollForm, EvaluationForm, TrainingForm,
    EmployeeSearchForm, LeaveSearchForm, DateRangeForm
)

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

# Employee Views
class EmployeeListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Employee
    template_name = 'hr/employee_list.html'
    context_object_name = 'employees'
    paginate_by = 10

    def get_queryset(self):
        queryset = Employee.objects.all()
        form = EmployeeSearchForm(self.request.GET)
        
        if form.is_valid():
            search = form.cleaned_data.get('search')
            department = form.cleaned_data.get('department')
            employment_type = form.cleaned_data.get('employment_type')
            is_active = form.cleaned_data.get('is_active')
            
            if search:
                queryset = queryset.filter(
                    Q(user__first_name__icontains=search) |
                    Q(user__last_name__icontains=search) |
                    Q(employee_id__icontains=search)
                )
            if department:
                queryset = queryset.filter(department=department)
            if employment_type:
                queryset = queryset.filter(employment_type=employment_type)
            if is_active:
                queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('user__first_name', 'user__last_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = EmployeeSearchForm(self.request.GET)
        return context

class EmployeeCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'hr/employee_form.html'
    success_url = reverse_lazy('hr:employee-list')

    def form_valid(self, form):
        messages.success(self.request, _('تم إضافة الموظف بنجاح.'))
        return super().form_valid(form)

class EmployeeDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Employee
    template_name = 'hr/employee_detail.html'
    context_object_name = 'employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        employee = self.get_object()
        context.update({
            'leaves': employee.leaves.all()[:5],
            'attendance': employee.attendance_records.all()[:5],
            'payroll': employee.payroll_records.all()[:5],
            'evaluations': employee.evaluations.all()[:5],
            'trainings': employee.trainings.all()[:5],
        })
        return context

class EmployeeUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'hr/employee_form.html'
    success_url = reverse_lazy('hr:employee-list')

    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث بيانات الموظف بنجاح.'))
        return super().form_valid(form)

class EmployeeDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Employee
    template_name = 'hr/employee_confirm_delete.html'
    success_url = reverse_lazy('hr:employee-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('تم حذف الموظف بنجاح.'))
        return super().delete(request, *args, **kwargs)

# Leave Views
class LeaveListView(LoginRequiredMixin, ListView):
    model = Leave
    template_name = 'hr/leave_list.html'
    context_object_name = 'leaves'
    paginate_by = 10

    def get_queryset(self):
        queryset = Leave.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__user=self.request.user)
        
        form = LeaveSearchForm(self.request.GET)
        if form.is_valid():
            leave_type = form.cleaned_data.get('leave_type')
            status = form.cleaned_data.get('status')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            
            if leave_type:
                queryset = queryset.filter(leave_type=leave_type)
            if status:
                queryset = queryset.filter(status=status)
            if date_from:
                queryset = queryset.filter(start_date__gte=date_from)
            if date_to:
                queryset = queryset.filter(end_date__lte=date_to)
        
        return queryset.order_by('-start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = LeaveSearchForm(self.request.GET)
        return context

class LeaveCreateView(LoginRequiredMixin, CreateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'hr/leave_form.html'
    success_url = reverse_lazy('hr:leave-list')

    def form_valid(self, form):
        form.instance.employee = self.request.user.employee_profile
        messages.success(self.request, _('تم تقديم طلب الإجازة بنجاح.'))
        return super().form_valid(form)

class LeaveDetailView(LoginRequiredMixin, DetailView):
    model = Leave
    template_name = 'hr/leave_detail.html'
    context_object_name = 'leave'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__user=self.request.user)
        return queryset

class LeaveUpdateView(LoginRequiredMixin, UpdateView):
    model = Leave
    form_class = LeaveForm
    template_name = 'hr/leave_form.html'
    success_url = reverse_lazy('hr:leave-list')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                employee__user=self.request.user,
                status='pending'
            )
        return queryset

    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث طلب الإجازة بنجاح.'))
        return super().form_valid(form)

class LeaveDeleteView(LoginRequiredMixin, DeleteView):
    model = Leave
    template_name = 'hr/leave_confirm_delete.html'
    success_url = reverse_lazy('hr:leave-list')

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(
                employee__user=self.request.user,
                status='pending'
            )
        return queryset

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('تم حذف طلب الإجازة بنجاح.'))
        return super().delete(request, *args, **kwargs)

class LeaveApproveView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Leave
    template_name = 'hr/leave_approve.html'
    fields = ['notes']
    success_url = reverse_lazy('hr:leave-list')

    def form_valid(self, form):
        leave = form.instance
        leave.status = 'approved'
        leave.approved_by = self.request.user
        leave.approved_at = timezone.now()
        messages.success(self.request, _('تمت الموافقة على طلب الإجازة.'))
        return super().form_valid(form)

class LeaveRejectView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Leave
    template_name = 'hr/leave_reject.html'
    fields = ['notes']
    success_url = reverse_lazy('hr:leave-list')

    def form_valid(self, form):
        leave = form.instance
        leave.status = 'rejected'
        leave.approved_by = self.request.user
        leave.approved_at = timezone.now()
        messages.success(self.request, _('تم رفض طلب الإجازة.'))
        return super().form_valid(form)

# Shift Views
class ShiftListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Shift
    template_name = 'hr/shift_list.html'
    context_object_name = 'shifts'
    paginate_by = 10

    def get_queryset(self):
        return Shift.objects.all().order_by('start_time')

class ShiftCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'hr/shift_form.html'
    success_url = reverse_lazy('hr:shift-list')

    def form_valid(self, form):
        messages.success(self.request, _('تم إنشاء المناوبة بنجاح.'))
        return super().form_valid(form)

class ShiftDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Shift
    template_name = 'hr/shift_detail.html'
    context_object_name = 'shift'

class ShiftUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Shift
    form_class = ShiftForm
    template_name = 'hr/shift_form.html'
    success_url = reverse_lazy('hr:shift-list')

    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث المناوبة بنجاح.'))
        return super().form_valid(form)

class ShiftDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Shift
    template_name = 'hr/shift_confirm_delete.html'
    success_url = reverse_lazy('hr:shift-list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('تم حذف المناوبة بنجاح.'))
        return super().delete(request, *args, **kwargs)

# Attendance Views
class AttendanceListView(LoginRequiredMixin, ListView):
    model = Attendance
    template_name = 'hr/attendance_list.html'
    context_object_name = 'attendance_records'
    paginate_by = 10

    def get_queryset(self):
        queryset = Attendance.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__user=self.request.user)
        
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        
        return queryset.order_by('-date', '-check_in')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_range_form'] = DateRangeForm(self.request.GET)
        return context

class AttendanceCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'hr/attendance_form.html'
    success_url = reverse_lazy('hr:attendance-list')

    def form_valid(self, form):
        attendance = form.instance
        
        # حساب التأخير والمغادرة المبكرة
        if attendance.check_in and attendance.shift:
            shift_start = timezone.make_aware(
                timezone.datetime.combine(
                    attendance.date,
                    attendance.shift.start_time
                )
            )
            if attendance.check_in > shift_start:
                attendance.late_arrival = attendance.check_in - shift_start
        
        if attendance.check_out and attendance.shift:
            shift_end = timezone.make_aware(
                timezone.datetime.combine(
                    attendance.date,
                    attendance.shift.end_time
                )
            )
            if attendance.check_out < shift_end:
                attendance.early_departure = shift_end - attendance.check_out
            elif attendance.check_out > shift_end:
                attendance.overtime = attendance.check_out - shift_end
        
        messages.success(self.request, _('تم تسجيل الحضور بنجاح.'))
        return super().form_valid(form)

class AttendanceDetailView(LoginRequiredMixin, DetailView):
    model = Attendance
    template_name = 'hr/attendance_detail.html'
    context_object_name = 'attendance'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__user=self.request.user)
        return queryset

class AttendanceUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Attendance
    form_class = AttendanceForm
    template_name = 'hr/attendance_form.html'
    success_url = reverse_lazy('hr:attendance-list')

    def form_valid(self, form):
        attendance = form.instance
        
        # إعادة حساب التأخير والمغادرة المبكرة
        attendance.late_arrival = None
        attendance.early_departure = None
        attendance.overtime = None
        
        if attendance.check_in and attendance.shift:
            shift_start = timezone.make_aware(
                timezone.datetime.combine(
                    attendance.date,
                    attendance.shift.start_time
                )
            )
            if attendance.check_in > shift_start:
                attendance.late_arrival = attendance.check_in - shift_start
        
        if attendance.check_out and attendance.shift:
            shift_end = timezone.make_aware(
                timezone.datetime.combine(
                    attendance.date,
                    attendance.shift.end_time
                )
            )
            if attendance.check_out < shift_end:
                attendance.early_departure = shift_end - attendance.check_out
            elif attendance.check_out > shift_end:
                attendance.overtime = attendance.check_out - shift_end
        
        messages.success(self.request, _('تم تحديث سجل الحضور بنجاح.'))
        return super().form_valid(form)

# Payroll Views
class PayrollListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Payroll
    template_name = 'hr/payroll_list.html'
    context_object_name = 'payroll_records'
    paginate_by = 10

    def get_queryset(self):
        queryset = Payroll.objects.all()
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        
        if date_from:
            queryset = queryset.filter(period_start__gte=date_from)
        if date_to:
            queryset = queryset.filter(period_end__lte=date_to)
        
        return queryset.order_by('-period_start')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_range_form'] = DateRangeForm(self.request.GET)
        return context

class PayrollCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'hr/payroll_form.html'
    success_url = reverse_lazy('hr:payroll-list')

    def form_valid(self, form):
        payroll = form.instance
        payroll.calculate_net_salary()
        messages.success(self.request, _('تم إنشاء سجل الراتب بنجاح.'))
        return super().form_valid(form)

class PayrollDetailView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Payroll
    template_name = 'hr/payroll_detail.html'
    context_object_name = 'payroll'

class PayrollUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Payroll
    form_class = PayrollForm
    template_name = 'hr/payroll_form.html'
    success_url = reverse_lazy('hr:payroll-list')

    def form_valid(self, form):
        payroll = form.instance
        payroll.calculate_net_salary()
        messages.success(self.request, _('تم تحديث سجل الراتب بنجاح.'))
        return super().form_valid(form)

class PayrollSlipView(LoginRequiredMixin, DetailView):
    model = Payroll
    template_name = 'hr/payroll_slip.html'
    context_object_name = 'payroll'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__user=self.request.user)
        return queryset

# Evaluation Views
class EvaluationListView(LoginRequiredMixin, ListView):
    model = Evaluation
    template_name = 'hr/evaluation_list.html'
    context_object_name = 'evaluations'
    paginate_by = 10

    def get_queryset(self):
        queryset = Evaluation.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__user=self.request.user)
        return queryset.order_by('-evaluation_date')

class EvaluationCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'hr/evaluation_form.html'
    success_url = reverse_lazy('hr:evaluation-list')

    def form_valid(self, form):
        evaluation = form.instance
        evaluation.evaluator = self.request.user
        evaluation.calculate_overall_score()
        messages.success(self.request, _('تم إنشاء التقييم بنجاح.'))
        return super().form_valid(form)

class EvaluationDetailView(LoginRequiredMixin, DetailView):
    model = Evaluation
    template_name = 'hr/evaluation_detail.html'
    context_object_name = 'evaluation'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(employee__user=self.request.user)
        return queryset

class EvaluationUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Evaluation
    form_class = EvaluationForm
    template_name = 'hr/evaluation_form.html'
    success_url = reverse_lazy('hr:evaluation-list')

    def form_valid(self, form):
        evaluation = form.instance
        evaluation.calculate_overall_score()
        messages.success(self.request, _('تم تحديث التقييم بنجاح.'))
        return super().form_valid(form)

# Training Views
class TrainingListView(LoginRequiredMixin, ListView):
    model = Training
    template_name = 'hr/training_list.html'
    context_object_name = 'trainings'
    paginate_by = 10

    def get_queryset(self):
        queryset = Training.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(participants__user=self.request.user)
        return queryset.order_by('-start_date')

class TrainingCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Training
    form_class = TrainingForm
    template_name = 'hr/training_form.html'
    success_url = reverse_lazy('hr:training-list')

    def form_valid(self, form):
        messages.success(self.request, _('تم إنشاء البرنامج التدريبي بنجاح.'))
        return super().form_valid(form)

class TrainingDetailView(LoginRequiredMixin, DetailView):
    model = Training
    template_name = 'hr/training_detail.html'
    context_object_name = 'training'

class TrainingUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Training
    form_class = TrainingForm
    template_name = 'hr/training_form.html'
    success_url = reverse_lazy('hr:training-list')

    def form_valid(self, form):
        messages.success(self.request, _('تم تحديث البرنامج التدريبي بنجاح.'))
        return super().form_valid(form)

class TrainingCompleteView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Training
    template_name = 'hr/training_complete.html'
    fields = ['notes']
    success_url = reverse_lazy('hr:training-list')

    def form_valid(self, form):
        training = form.instance
        training.status = 'completed'
        messages.success(self.request, _('تم إكمال البرنامج التدريبي بنجاح.'))
        return super().form_valid(form)

# Report Views
class HRReportView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'hr/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'total_employees': Employee.objects.filter(is_active=True).count(),
            'total_leaves': Leave.objects.filter(
                start_date__year=timezone.now().year
            ).count(),
            'total_trainings': Training.objects.filter(
                status='completed'
            ).count(),
            'pending_leaves': Leave.objects.filter(
                status='pending'
            ).count(),
        })
        return context

class AttendanceReportView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'hr/attendance_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateRangeForm(self.request.GET)
        
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            
            attendance = Attendance.objects.filter(
                date__range=[date_from, date_to]
            )
            
            context.update({
                'total_records': attendance.count(),
                'present_count': attendance.filter(status='present').count(),
                'absent_count': attendance.filter(status='absent').count(),
                'late_count': attendance.filter(status='late').count(),
                'attendance_by_department': Employee.objects.values(
                    'department'
                ).annotate(
                    total=models.Count('attendance_records'),
                    present=models.Count(
                        'attendance_records',
                        filter=models.Q(
                            attendance_records__status='present',
                            attendance_records__date__range=[date_from, date_to]
                        )
                    )
                )
            })
        
        context['form'] = form
        return context

class LeaveReportView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'hr/leave_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateRangeForm(self.request.GET)
        
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            
            leaves = Leave.objects.filter(
                start_date__range=[date_from, date_to]
            )
            
            context.update({
                'total_leaves': leaves.count(),
                'approved_leaves': leaves.filter(status='approved').count(),
                'rejected_leaves': leaves.filter(status='rejected').count(),
                'pending_leaves': leaves.filter(status='pending').count(),
                'leaves_by_type': leaves.values(
                    'leave_type'
                ).annotate(
                    count=models.Count('id')
                ),
                'leaves_by_department': Employee.objects.values(
                    'department'
                ).annotate(
                    total=models.Count('leaves'),
                    approved=models.Count(
                        'leaves',
                        filter=models.Q(
                            leaves__status='approved',
                            leaves__start_date__range=[date_from, date_to]
                        )
                    )
                )
            })
        
        context['form'] = form
        return context

class PayrollReportView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'hr/payroll_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateRangeForm(self.request.GET)
        
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            
            payroll = Payroll.objects.filter(
                period_start__range=[date_from, date_to]
            )
            
            context.update({
                'total_payroll': payroll.aggregate(
                    total=models.Sum('net_salary')
                )['total'],
                'total_basic': payroll.aggregate(
                    total=models.Sum('basic_salary')
                )['total'],
                'total_allowances': payroll.aggregate(
                    total=models.Sum('allowances')
                )['total'],
                'total_deductions': payroll.aggregate(
                    total=models.Sum('deductions')
                )['total'],
                'payroll_by_department': Employee.objects.values(
                    'department'
                ).annotate(
                    total_salary=models.Sum(
                        'payroll_records__net_salary',
                        filter=models.Q(
                            payroll_records__period_start__range=[
                                date_from,
                                date_to
                            ]
                        )
                    )
                )
            })
        
        context['form'] = form
        return context

class PerformanceReportView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'hr/performance_report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DateRangeForm(self.request.GET)
        
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            
            evaluations = Evaluation.objects.filter(
                evaluation_date__range=[date_from, date_to]
            )
            
            context.update({
                'total_evaluations': evaluations.count(),
                'average_score': evaluations.aggregate(
                    avg=models.Avg('overall_score')
                )['avg'],
                'performance_by_department': Employee.objects.values(
                    'department'
                ).annotate(
                    avg_score=models.Avg(
                        'evaluations__overall_score',
                        filter=models.Q(
                            evaluations__evaluation_date__range=[
                                date_from,
                                date_to
                            ]
                        )
                    )
                ),
                'score_distribution': {
                    'excellent': evaluations.filter(
                        overall_score__gte=90
                    ).count(),
                    'very_good': evaluations.filter(
                        overall_score__range=[80, 89]
                    ).count(),
                    'good': evaluations.filter(
                        overall_score__range=[70, 79]
                    ).count(),
                    'average': evaluations.filter(
                        overall_score__range=[60, 69]
                    ).count(),
                    'below_average': evaluations.filter(
                        overall_score__lt=60
                    ).count(),
                }
            })
        
        context['form'] = form
        return context
