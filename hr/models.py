from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal

class Employee(models.Model):
    """نموذج الموظفين"""
    
    GENDER_CHOICES = [
        ('M', _('Male')),
        ('F', _('Female')),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('single', _('Single')),
        ('married', _('Married')),
        ('divorced', _('Divorced')),
        ('widowed', _('Widowed')),
    ]
    
    EMPLOYMENT_TYPE_CHOICES = [
        ('full_time', _('Full Time')),
        ('part_time', _('Part Time')),
        ('contract', _('Contract')),
        ('temporary', _('Temporary')),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile',
        verbose_name=_('User')
    )
    employee_id = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Employee ID')
    )
    department = models.CharField(
        max_length=100,
        verbose_name=_('Department')
    )
    position = models.CharField(
        max_length=100,
        verbose_name=_('Position')
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        verbose_name=_('Employment Type')
    )
    join_date = models.DateField(
        verbose_name=_('Join Date')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('End Date')
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name=_('Gender')
    )
    date_of_birth = models.DateField(
        verbose_name=_('Date of Birth')
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        verbose_name=_('Marital Status')
    )
    phone = models.CharField(
        max_length=20,
        verbose_name=_('Phone')
    )
    emergency_contact = models.CharField(
        max_length=20,
        verbose_name=_('Emergency Contact')
    )
    address = models.TextField(
        verbose_name=_('Address')
    )
    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Basic Salary')
    )
    bank_account = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Bank Account')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.employee_id})"

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['user__first_name', 'user__last_name']

class Leave(models.Model):
    """نموذج الإجازات"""
    
    LEAVE_TYPE_CHOICES = [
        ('annual', _('Annual Leave')),
        ('sick', _('Sick Leave')),
        ('emergency', _('Emergency Leave')),
        ('unpaid', _('Unpaid Leave')),
        ('other', _('Other')),
    ]
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('approved', _('Approved')),
        ('rejected', _('Rejected')),
        ('cancelled', _('Cancelled')),
    ]
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='leaves',
        verbose_name=_('Employee')
    )
    leave_type = models.CharField(
        max_length=20,
        choices=LEAVE_TYPE_CHOICES,
        verbose_name=_('Leave Type')
    )
    start_date = models.DateField(
        verbose_name=_('Start Date')
    )
    end_date = models.DateField(
        verbose_name=_('End Date')
    )
    reason = models.TextField(
        verbose_name=_('Reason')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_leaves',
        verbose_name=_('Approved By')
    )
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Approved At')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )

    def __str__(self):
        return f"{self.employee} - {self.get_leave_type_display()}"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()
        if self.start_date > self.end_date:
            raise ValidationError(_('End date must be after start date'))

    class Meta:
        verbose_name = _('Leave')
        verbose_name_plural = _('Leaves')
        ordering = ['-start_date']

class Shift(models.Model):
    """نموذج المناوبات"""
    
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name')
    )
    start_time = models.TimeField(
        verbose_name=_('Start Time')
    )
    end_time = models.TimeField(
        verbose_name=_('End Time')
    )
    break_duration = models.IntegerField(
        default=60,
        help_text=_('Break duration in minutes'),
        verbose_name=_('Break Duration')
    )
    is_night_shift = models.BooleanField(
        default=False,
        verbose_name=_('Is Night Shift')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Shift')
        verbose_name_plural = _('Shifts')
        ordering = ['start_time']

class Attendance(models.Model):
    """نموذج الحضور والانصراف"""
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name=_('Employee')
    )
    date = models.DateField(
        verbose_name=_('Date')
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendance_records',
        verbose_name=_('Shift')
    )
    check_in = models.DateTimeField(
        verbose_name=_('Check In')
    )
    check_out = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Check Out')
    )
    late_arrival = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_('Late Arrival')
    )
    early_departure = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_('Early Departure')
    )
    overtime = models.DurationField(
        null=True,
        blank=True,
        verbose_name=_('Overtime')
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('present', _('Present')),
            ('absent', _('Absent')),
            ('late', _('Late')),
            ('half_day', _('Half Day')),
        ],
        verbose_name=_('Status')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )

    def __str__(self):
        return f"{self.employee} - {self.date}"

    class Meta:
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendance Records')
        ordering = ['-date', '-check_in']
        unique_together = ['employee', 'date']

class Payroll(models.Model):
    """نموذج الرواتب"""
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='payroll_records',
        verbose_name=_('Employee')
    )
    period_start = models.DateField(
        verbose_name=_('Period Start')
    )
    period_end = models.DateField(
        verbose_name=_('Period End')
    )
    basic_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Basic Salary')
    )
    overtime_hours = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Overtime Hours')
    )
    overtime_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.5,
        validators=[MinValueValidator(0)],
        verbose_name=_('Overtime Rate')
    )
    allowances = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Allowances')
    )
    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_('Deductions')
    )
    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Net Salary')
    )
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('bank', _('Bank Transfer')),
            ('cash', _('Cash')),
            ('cheque', _('Cheque')),
        ],
        verbose_name=_('Payment Method')
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', _('Pending')),
            ('paid', _('Paid')),
            ('cancelled', _('Cancelled')),
        ],
        default='pending',
        verbose_name=_('Payment Status')
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Paid At')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )

    def __str__(self):
        return f"{self.employee} - {self.period_start} to {self.period_end}"

    def calculate_net_salary(self):
        """حساب صافي الراتب"""
        overtime_pay = (
            self.overtime_hours *
            self.overtime_rate *
            (self.basic_salary / 30 / 8)  # يوم/ساعات العمل
        )
        gross_salary = self.basic_salary + overtime_pay + self.allowances
        self.net_salary = gross_salary - self.deductions
        return self.net_salary

    class Meta:
        verbose_name = _('Payroll')
        verbose_name_plural = _('Payroll Records')
        ordering = ['-period_start']
        unique_together = ['employee', 'period_start', 'period_end']

class Evaluation(models.Model):
    """نموذج تقييم الأداء"""
    
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='evaluations',
        verbose_name=_('Employee')
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conducted_evaluations',
        verbose_name=_('Evaluator')
    )
    evaluation_date = models.DateField(
        verbose_name=_('Evaluation Date')
    )
    period_start = models.DateField(
        verbose_name=_('Period Start')
    )
    period_end = models.DateField(
        verbose_name=_('Period End')
    )
    performance_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Performance Score')
    )
    attendance_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Attendance Score')
    )
    punctuality_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Punctuality Score')
    )
    productivity_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Productivity Score')
    )
    quality_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Quality Score')
    )
    initiative_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Initiative Score')
    )
    teamwork_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Teamwork Score')
    )
    communication_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Communication Score')
    )
    overall_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_('Overall Score')
    )
    strengths = models.TextField(
        verbose_name=_('Strengths')
    )
    areas_for_improvement = models.TextField(
        verbose_name=_('Areas for Improvement')
    )
    goals = models.TextField(
        verbose_name=_('Goals for Next Period')
    )
    comments = models.TextField(
        blank=True,
        verbose_name=_('Comments')
    )
    employee_comments = models.TextField(
        blank=True,
        verbose_name=_('Employee Comments')
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', _('Draft')),
            ('submitted', _('Submitted')),
            ('acknowledged', _('Acknowledged')),
            ('completed', _('Completed')),
        ],
        default='draft',
        verbose_name=_('Status')
    )

    def __str__(self):
        return f"{self.employee} - {self.evaluation_date}"

    def calculate_overall_score(self):
        """حساب النتيجة الإجمالية"""
        scores = [
            self.performance_score,
            self.attendance_score,
            self.punctuality_score,
            self.productivity_score,
            self.quality_score,
            self.initiative_score,
            self.teamwork_score,
            self.communication_score,
        ]
        self.overall_score = sum(scores) // len(scores)
        return self.overall_score

    class Meta:
        verbose_name = _('Evaluation')
        verbose_name_plural = _('Evaluations')
        ordering = ['-evaluation_date']

class Training(models.Model):
    """نموذج التدريب"""
    
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title')
    )
    description = models.TextField(
        verbose_name=_('Description')
    )
    trainer = models.CharField(
        max_length=255,
        verbose_name=_('Trainer')
    )
    start_date = models.DateField(
        verbose_name=_('Start Date')
    )
    end_date = models.DateField(
        verbose_name=_('End Date')
    )
    location = models.CharField(
        max_length=255,
        verbose_name=_('Location')
    )
    participants = models.ManyToManyField(
        Employee,
        related_name='trainings',
        verbose_name=_('Participants')
    )
    max_participants = models.PositiveIntegerField(
        verbose_name=_('Maximum Participants')
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Cost')
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('planned', _('Planned')),
            ('in_progress', _('In Progress')),
            ('completed', _('Completed')),
            ('cancelled', _('Cancelled')),
        ],
        default='planned',
        verbose_name=_('Status')
    )
    materials = models.TextField(
        blank=True,
        verbose_name=_('Training Materials')
    )
    prerequisites = models.TextField(
        blank=True,
        verbose_name=_('Prerequisites')
    )
    objectives = models.TextField(
        verbose_name=_('Objectives')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Training')
        verbose_name_plural = _('Training Programs')
        ordering = ['-start_date']
