from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    # إدارة الموظفين
    path('employees/', views.EmployeeListView.as_view(), name='employee-list'),
    path('employees/create/', views.EmployeeCreateView.as_view(), name='employee-create'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/<int:pk>/update/', views.EmployeeUpdateView.as_view(), name='employee-update'),
    path('employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='employee-delete'),
    
    # الإجازات
    path('leaves/', views.LeaveListView.as_view(), name='leave-list'),
    path('leaves/create/', views.LeaveCreateView.as_view(), name='leave-create'),
    path('leaves/<int:pk>/', views.LeaveDetailView.as_view(), name='leave-detail'),
    path('leaves/<int:pk>/update/', views.LeaveUpdateView.as_view(), name='leave-update'),
    path('leaves/<int:pk>/delete/', views.LeaveDeleteView.as_view(), name='leave-delete'),
    path('leaves/<int:pk>/approve/', views.LeaveApproveView.as_view(), name='leave-approve'),
    path('leaves/<int:pk>/reject/', views.LeaveRejectView.as_view(), name='leave-reject'),
    
    # المناوبات
    path('shifts/', views.ShiftListView.as_view(), name='shift-list'),
    path('shifts/create/', views.ShiftCreateView.as_view(), name='shift-create'),
    path('shifts/<int:pk>/', views.ShiftDetailView.as_view(), name='shift-detail'),
    path('shifts/<int:pk>/update/', views.ShiftUpdateView.as_view(), name='shift-update'),
    path('shifts/<int:pk>/delete/', views.ShiftDeleteView.as_view(), name='shift-delete'),
    
    # الحضور والانصراف
    path('attendance/', views.AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/create/', views.AttendanceCreateView.as_view(), name='attendance-create'),
    path('attendance/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    path('attendance/<int:pk>/update/', views.AttendanceUpdateView.as_view(), name='attendance-update'),
    
    # الرواتب
    path('payroll/', views.PayrollListView.as_view(), name='payroll-list'),
    path('payroll/create/', views.PayrollCreateView.as_view(), name='payroll-create'),
    path('payroll/<int:pk>/', views.PayrollDetailView.as_view(), name='payroll-detail'),
    path('payroll/<int:pk>/update/', views.PayrollUpdateView.as_view(), name='payroll-update'),
    path('payroll/<int:pk>/slip/', views.PayrollSlipView.as_view(), name='payroll-slip'),
    
    # التقييمات
    path('evaluations/', views.EvaluationListView.as_view(), name='evaluation-list'),
    path('evaluations/create/', views.EvaluationCreateView.as_view(), name='evaluation-create'),
    path('evaluations/<int:pk>/', views.EvaluationDetailView.as_view(), name='evaluation-detail'),
    path('evaluations/<int:pk>/update/', views.EvaluationUpdateView.as_view(), name='evaluation-update'),
    
    # التدريب
    path('training/', views.TrainingListView.as_view(), name='training-list'),
    path('training/create/', views.TrainingCreateView.as_view(), name='training-create'),
    path('training/<int:pk>/', views.TrainingDetailView.as_view(), name='training-detail'),
    path('training/<int:pk>/update/', views.TrainingUpdateView.as_view(), name='training-update'),
    path('training/<int:pk>/complete/', views.TrainingCompleteView.as_view(), name='training-complete'),
    
    # التقارير
    path('reports/', views.HRReportView.as_view(), name='reports'),
    path('reports/attendance/', views.AttendanceReportView.as_view(), name='attendance-report'),
    path('reports/leaves/', views.LeaveReportView.as_view(), name='leave-report'),
    path('reports/payroll/', views.PayrollReportView.as_view(), name='payroll-report'),
    path('reports/performance/', views.PerformanceReportView.as_view(), name='performance-report'),
]
