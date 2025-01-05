from django.db import models
from django.utils import timezone
from accounts.models import Patient, Doctor
from django.core.validators import MinValueValidator, MaxValueValidator

class MedicalRecord(models.Model):
    """الملف الطبي الأساسي"""
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ])
    height = models.DecimalField(max_digits=5, decimal_places=2, help_text="بالسنتيمتر")
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="بالكيلوغرام")
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    family_history = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"الملف الطبي لـ {self.patient.user.get_full_name()}"

    @property
    def bmi(self):
        """حساب مؤشر كتلة الجسم"""
        height_m = float(self.height) / 100
        return round(float(self.weight) / (height_m * height_m), 2)

class VitalSigns(models.Model):
    """المؤشرات الحيوية"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    blood_pressure_systolic = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(300)])
    blood_pressure_diastolic = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(200)])
    heart_rate = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(250)])
    temperature = models.DecimalField(max_digits=4, decimal_places=1)
    blood_sugar = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    oxygen_saturation = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"مؤشرات {self.patient.user.get_full_name()} في {self.date}"

class Medication(models.Model):
    """الأدوية والجرعات"""
    FREQUENCY_CHOICES = [
        ('daily', 'يومياً'),
        ('twice_daily', 'مرتين يومياً'),
        ('three_times', 'ثلاث مرات يومياً'),
        ('four_times', 'أربع مرات يومياً'),
        ('weekly', 'أسبوعياً'),
        ('monthly', 'شهرياً'),
        ('as_needed', 'عند الحاجة'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'نشط'),
        ('completed', 'مكتمل'),
        ('discontinued', 'متوقف'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    prescribing_doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.patient.user.get_full_name()}"

    @property
    def is_active(self):
        return self.status == 'active' and (not self.end_date or self.end_date >= timezone.now().date())

class MedicationReminder(models.Model):
    """تذكير بمواعيد الأدوية"""
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    time = models.TimeField()
    is_taken = models.BooleanField(default=False)
    taken_at = models.DateTimeField(null=True, blank=True)
    skipped = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def mark_as_taken(self):
        self.is_taken = True
        self.taken_at = timezone.now()
        self.save()

class Appointment(models.Model):
    """المواعيد الطبية"""
    STATUS_CHOICES = [
        ('scheduled', 'مجدول'),
        ('confirmed', 'مؤكد'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغي'),
        ('no_show', 'لم يحضر'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return f"موعد {self.patient.user.get_full_name()} مع د.{self.doctor.user.get_full_name()}"

class HealthGoal(models.Model):
    """أهداف صحية"""
    TYPE_CHOICES = [
        ('weight', 'الوزن'),
        ('exercise', 'التمارين'),
        ('diet', 'النظام الغذائي'),
        ('blood_pressure', 'ضغط الدم'),
        ('blood_sugar', 'سكر الدم'),
        ('other', 'أخرى'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_value = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    start_date = models.DateField()
    target_date = models.DateField()
    achieved = models.BooleanField(default=False)
    achieved_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.patient.user.get_full_name()}"

class ProgressUpdate(models.Model):
    """تحديثات التقدم"""
    goal = models.ForeignKey(HealthGoal, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"تحديث {self.goal.title} - {self.date}"

class LabResult(models.Model):
    """نتائج التحاليل المخبرية"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=200)
    test_date = models.DateField()
    result_value = models.CharField(max_length=100)
    normal_range = models.CharField(max_length=100)
    is_normal = models.BooleanField()
    lab_name = models.CharField(max_length=200)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='lab_results/', null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-test_date']

    def __str__(self):
        return f"{self.test_name} - {self.patient.user.get_full_name()}"

class Vaccination(models.Model):
    """سجل التطعيمات"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=200)
    dose_number = models.PositiveIntegerField()
    date_given = models.DateField()
    next_due_date = models.DateField(null=True, blank=True)
    administered_by = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date_given']

    def __str__(self):
        return f"{self.vaccine_name} - {self.patient.user.get_full_name()}"
