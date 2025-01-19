import re
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.cache_decorators import cache_method, invalidate_cache_on_save
from core.cache_manager import CacheManager


class Patient(models.Model):
    """نموذج المريض"""

    GENDER_CHOICES = [
        ("M", _("Male")),
        ("F", _("Female")),
    ]

    MARITAL_STATUS_CHOICES = [
        ("single", _("Single")),
        ("married", _("Married")),
        ("divorced", _("Divorced")),
        ("widowed", _("Widowed")),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
        verbose_name=_("User"),
    )

    date_of_birth = models.DateField(verbose_name=_("Date of Birth"))

    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, verbose_name=_("Gender")
    )

    marital_status = models.CharField(
        max_length=10, choices=MARITAL_STATUS_CHOICES, verbose_name=_("Marital Status"),
        default=MARITAL_STATUS_CHOICES[0][0]
    )

    phone_number = models.CharField(max_length=20, verbose_name=_("Phone Number"), default="")

    address = models.TextField(verbose_name=_("Address"), default="")

    emergency_contact_name = models.CharField(
        max_length=255, verbose_name=_("Emergency Contact Name"), default=""
    )

    emergency_contact_phone = models.CharField(
        max_length=20, verbose_name=_("Emergency Contact Phone"), default=""
    )

    occupation = models.CharField(
        max_length=100, blank=True, verbose_name=_("Occupation")
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        ordering = ["user__last_name", "user__first_name"]

    def __str__(self):
        return f"{self.user.get_full_name()}"

    def get_age(self):
        """حساب عمر المريض"""
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (
            today.month == self.date_of_birth.month
            and today.day < self.date_of_birth.day
        ):
            age -= 1
        return age

    def clean(self):
        """التحقق من صحة البيانات"""
        if self.date_of_birth:
            if self.date_of_birth > timezone.now().date():
                raise ValidationError(
                    {"date_of_birth": _("Date of birth cannot be in the future")}
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class MedicalRecord(models.Model):
    """نموذج السجل الطبي"""

    BLOOD_TYPES = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("O+", "O+"),
        ("O-", "O-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
    ]

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_record",
        verbose_name=_("Patient"),
    )

    blood_type = models.CharField(
        max_length=3, choices=BLOOD_TYPES, verbose_name=_("Blood Type")
    )

    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(300)],
        verbose_name=_("Height (cm)"),
    )

    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(500)],
        verbose_name=_("Weight (kg)"),
    )

    allergies = models.TextField(blank=True, verbose_name=_("Allergies"))

    chronic_conditions = models.TextField(
        blank=True, verbose_name=_("Chronic Conditions")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Medical Record")
        verbose_name_plural = _("Medical Records")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient.user.get_full_name()}'s Medical Record"

    def clean(self):
        """التحقق من صحة البيانات"""
        if self.height <= 0:
            raise ValidationError(_("Height must be greater than 0"))
        if self.weight <= 0:
            raise ValidationError(_("Weight must be greater than 0"))

    def save(self, *args, **kwargs):
        """حفظ السجل الطبي"""
        self.clean()
        super().save(*args, **kwargs)

    @property
    def bmi(self):
        """حساب مؤشر كتلة الجسم"""
        if self.height and self.weight:
            height_m = self.height / 100  # تحويل الطول من سم إلى متر
            return round(float(self.weight) / (float(height_m) ** 2), 2)
        return None

    @property
    def bmi_status(self):
        """تحديد حالة مؤشر كتلة الجسم"""
        bmi = self.bmi
        if bmi is None:
            return None
        if bmi < 18.5:
            return _("Underweight")
        elif 18.5 <= bmi < 25:
            return _("Normal")
        elif 25 <= bmi < 30:
            return _("Overweight")
        else:
            return _("Obese")


class MedicalVisit(models.Model):
    """نموذج الزيارة الطبية"""

    VISIT_TYPES = [
        ("regular", _("Regular Check-up")),
        ("emergency", _("Emergency")),
        ("follow_up", _("Follow-up")),
        ("consultation", _("Consultation")),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_visits",
        verbose_name=_("Patient"),
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_visits",
        verbose_name=_("Doctor"),
    )

    visit_type = models.CharField(
        max_length=20, choices=VISIT_TYPES, verbose_name=_("Visit Type")
    )

    visit_date = models.DateTimeField(verbose_name=_("Visit Date"))

    symptoms = models.TextField(verbose_name=_("Symptoms"))

    diagnosis = models.TextField(verbose_name=_("Diagnosis"))

    treatment = models.TextField(verbose_name=_("Treatment"))

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    follow_up_date = models.DateField(
        null=True, blank=True, verbose_name=_("Follow-up Date")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Medical Visit")
        verbose_name_plural = _("Medical Visits")
        ordering = ["-visit_date"]

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.visit_date}"


class Prescription(models.Model):
    """نموذج الوصفة الطبية"""

    visit = models.ForeignKey(
        MedicalVisit,
        on_delete=models.CASCADE,
        related_name="prescriptions",
        verbose_name=_("Medical Visit"),
    )

    medication_name = models.CharField(
        max_length=255, verbose_name=_("Medication Name")
    )

    dosage = models.CharField(max_length=100, verbose_name=_("Dosage"))

    frequency = models.CharField(max_length=100, verbose_name=_("Frequency"))

    duration = models.CharField(max_length=100, verbose_name=_("Duration"))

    instructions = models.TextField(blank=True, verbose_name=_("Special Instructions"))

    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    expiry_date = models.DateField(verbose_name=_("Expiry Date"), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Prescription")
        verbose_name_plural = _("Prescriptions")

    def __str__(self):
        return f"{self.medication_name} - {self.visit.patient.user.get_full_name()}"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()

        # التحقق من تاريخ انتهاء الصلاحية
        if self.expiry_date and self.expiry_date < timezone.now().date():
            raise ValidationError(
                {"expiry_date": _("Expiry date cannot be in the past")}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class LabTest(models.Model):
    """نموذج التحليل المخبري"""

    TEST_STATUS = [
        ("pending", _("Pending")),
        ("in_progress", _("In Progress")),
        ("completed", _("Completed")),
        ("cancelled", _("Cancelled")),
    ]

    visit = models.ForeignKey(
        MedicalVisit,
        on_delete=models.CASCADE,
        related_name="lab_tests",
        verbose_name=_("Medical Visit"),
    )

    test_name = models.CharField(max_length=255, verbose_name=_("Test Name"))

    description = models.TextField(verbose_name=_("Description"))

    status = models.CharField(
        max_length=20, choices=TEST_STATUS, default="pending", verbose_name=_("Status")
    )

    results = models.TextField(blank=True, verbose_name=_("Results"))

    test_date = models.DateTimeField(verbose_name=_("Test Date"))

    results_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Results Date")
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Lab Test")
        verbose_name_plural = _("Lab Tests")
        ordering = ["-test_date"]

    def __str__(self):
        return f"{self.test_name} - {self.visit.patient.user.get_full_name()}"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()

        # التحقق من تواريخ الفحص والنتائج
        if self.results_date and self.test_date and self.results_date < self.test_date:
            raise ValidationError(
                {"results_date": _("Results date cannot be before test date")}
            )

        if self.test_date and self.test_date > timezone.now():
            if self.status != "pending":
                raise ValidationError(
                    {"status": _("Future tests must have pending status")}
                )

        if self.status == "completed" and not self.results:
            raise ValidationError({"results": _("Completed tests must have results")})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Radiology(models.Model):
    """نموذج الأشعة"""

    RADIOLOGY_TYPES = [
        ("xray", _("X-Ray")),
        ("ct", _("CT Scan")),
        ("mri", _("MRI")),
        ("ultrasound", _("Ultrasound")),
        ("other", _("Other")),
    ]

    visit = models.ForeignKey(
        MedicalVisit,
        on_delete=models.CASCADE,
        related_name="radiology_tests",
        verbose_name=_("Medical Visit"),
    )

    radiology_type = models.CharField(
        max_length=20, choices=RADIOLOGY_TYPES, verbose_name=_("Radiology Type")
    )

    body_part = models.CharField(max_length=100, verbose_name=_("Body Part"))

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    image = models.ImageField(upload_to="radiology/", verbose_name=_("Image"))

    report = models.TextField(blank=True, verbose_name=_("Report"))

    performed_at = models.DateTimeField(verbose_name=_("Performed At"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Radiology")
        verbose_name_plural = _("Radiology Tests")
        ordering = ["-performed_at"]

    def __str__(self):
        return f"{self.get_radiology_type_display()} - {self.visit.patient.user.get_full_name()}"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()

        # التحقق من تاريخ الإجراء
        if self.performed_at and self.performed_at > timezone.now():
            raise ValidationError(
                {"performed_at": _("Performance date cannot be in the future")}
            )

        # التحقق من وجود التقرير مع الصورة
        if self.image and not self.report:
            raise ValidationError(
                {"report": _("Report is required when image is uploaded")}
            )

    def save(self, *args, **kwargs):
        if self.image:
            # معالجة حجم الصورة
            from PIL import Image

            img = Image.open(self.image)

            # تحديد الحد الأقصى للأبعاد
            max_size = (1920, 1080)
            img.thumbnail(max_size, Image.LANCZOS)

            # حفظ الصورة المعالجة
            img.save(self.image.path, quality=85, optimize=True)

        self.full_clean()
        super().save(*args, **kwargs)


class Vaccination(models.Model):
    """نموذج التطعيم"""

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="vaccinations",
        verbose_name=_("Patient"),
    )

    vaccine_name = models.CharField(max_length=255, verbose_name=_("Vaccine Name"))

    dose_number = models.PositiveIntegerField(verbose_name=_("Dose Number"))

    date_given = models.DateTimeField(verbose_name=_("Date Given"))

    next_due_date = models.DateField(
        null=True, blank=True, verbose_name=_("Next Due Date")
    )

    administered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="administered_vaccines",
        verbose_name=_("Administered By"),
    )

    batch_number = models.CharField(max_length=100, verbose_name=_("Batch Number"))

    manufacturer = models.CharField(max_length=255, verbose_name=_("Manufacturer"))

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Vaccination")
        verbose_name_plural = _("Vaccinations")
        ordering = ["-date_given"]

    def __str__(self):
        return f"{self.vaccine_name} - {self.patient.user.get_full_name()}"


class Medication(models.Model):
    """نموذج الدواء"""

    name = models.CharField(max_length=255, verbose_name=_("Name"))

    generic_name = models.CharField(max_length=255, verbose_name=_("Generic Name"))

    manufacturer = models.CharField(max_length=255, verbose_name=_("Manufacturer"))

    description = models.TextField(verbose_name=_("Description"))

    dosage_form = models.CharField(max_length=100, verbose_name=_("Dosage Form"))

    strength = models.CharField(max_length=100, verbose_name=_("Strength"))

    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Price")
    )

    requires_prescription = models.BooleanField(
        default=True, verbose_name=_("Requires Prescription")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Medication")
        verbose_name_plural = _("Medications")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.strength})"


class Inventory(models.Model):
    """نموذج المخزون"""

    medication = models.ForeignKey(
        Medication,
        on_delete=models.CASCADE,
        related_name="inventory",
        verbose_name=_("Medication"),
    )

    batch_number = models.CharField(max_length=100, verbose_name=_("Batch Number"))

    expiry_date = models.DateField(verbose_name=_("Expiry Date"))

    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))

    reorder_level = models.PositiveIntegerField(verbose_name=_("Reorder Level"))

    location = models.CharField(max_length=100, verbose_name=_("Storage Location"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Inventory")
        verbose_name_plural = _("Inventory Items")
        ordering = ["medication__name"]

    def __str__(self):
        return f"{self.medication.name} - {self.batch_number}"

    def clean(self):
        """التحقق من صحة البيانات"""
        super().clean()

        # التحقق من تاريخ انتهاء الصلاحية
        if self.expiry_date and self.expiry_date < timezone.now().date():
            raise ValidationError(
                {"expiry_date": _("Expiry date cannot be in the past")}
            )

        # التحقق من مستوى إعادة الطلب
        if self.reorder_level >= self.quantity:
            raise ValidationError(
                {"reorder_level": _("Reorder level must be less than quantity")}
            )

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_quantity = None if is_new else Inventory.objects.get(pk=self.pk).quantity

        self.full_clean()
        super().save(*args, **kwargs)

        # إرسال إشعارات عند انخفاض المخزون
        if not is_new and old_quantity != self.quantity:
            if self.is_low_stock():
                from notifications.models import Notification

                Notification.objects.create(
                    title=_("Low Stock Alert"),
                    message=_(
                        f"Inventory item {self.medication.name} is running low. Current quantity: {self.quantity}"
                    ),
                    notification_type="inventory_alert",
                    related_object=self,
                )

    def is_low_stock(self):
        """التحقق من المخزون المنخفض"""
        return self.quantity <= self.reorder_level

    def is_expired(self):
        """التحقق من انتهاء الصلاحية"""
        return self.expiry_date and self.expiry_date <= timezone.now().date()

    @property
    def status(self):
        """حالة المخزون"""
        if self.is_expired():
            return "expired"
        elif self.is_low_stock():
            return "low_stock"
        return "normal"


class InventoryTransaction(models.Model):
    """نموذج حركة المخزون"""

    TRANSACTION_TYPES = [
        ("in", _("Stock In")),
        ("out", _("Stock Out")),
        ("return", _("Return")),
        ("adjustment", _("Adjustment")),
    ]

    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name=_("Inventory"),
    )

    transaction_type = models.CharField(
        max_length=20, choices=TRANSACTION_TYPES, verbose_name=_("Transaction Type")
    )

    quantity = models.IntegerField(verbose_name=_("Quantity"))

    reference = models.CharField(
        max_length=255, blank=True, verbose_name=_("Reference")
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_record_transactions',
        verbose_name=_("Performed By"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Inventory Transaction")
        verbose_name_plural = _("Inventory Transactions")
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.get_transaction_type_display()} - {self.inventory.medication.name}"
        )

    def save(self, *args, **kwargs):
        """تحديث المخزون عند إجراء الحركة"""
        if self.transaction_type == "in":
            self.inventory.quantity += self.quantity
        elif self.transaction_type == "out":
            self.inventory.quantity -= self.quantity
        elif self.transaction_type == "return":
            self.inventory.quantity += self.quantity
        elif self.transaction_type == "adjustment":
            # لا نقوم بأي تعديل على المخزون في حالة التعديل اليدوي
            pass

        self.inventory.save()
        super().save(*args, **kwargs)


class MedicalReport(models.Model):
    """نموذج التقرير الطبي"""

    REPORT_TYPES = [
        ("general", _("General Report")),
        ("specialist", _("Specialist Report")),
        ("lab", _("Laboratory Report")),
        ("radiology", _("Radiology Report")),
        ("surgery", _("Surgery Report")),
        ("discharge", _("Discharge Report")),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_reports",
        verbose_name=_("Patient"),
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="authored_reports",
        verbose_name=_("Doctor"),
    )

    report_type = models.CharField(
        max_length=20, choices=REPORT_TYPES, verbose_name=_("Report Type")
    )

    title = models.CharField(max_length=255, verbose_name=_("Title"))

    content = models.TextField(verbose_name=_("Content"))

    diagnosis = models.TextField(verbose_name=_("Diagnosis"))

    recommendations = models.TextField(verbose_name=_("Recommendations"))

    is_confidential = models.BooleanField(
        default=False, verbose_name=_("Is Confidential")
    )

    attachments = models.FileField(
        upload_to="reports/", blank=True, null=True, verbose_name=_("Attachments")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Medical Report")
        verbose_name_plural = _("Medical Reports")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_report_type_display()} - {self.patient.user.get_full_name()}"


class FollowUp(models.Model):
    """نموذج المتابعة الدورية"""

    PRIORITY_CHOICES = [
        ("low", _("Low")),
        ("medium", _("Medium")),
        ("high", _("High")),
        ("urgent", _("Urgent")),
    ]

    STATUS_CHOICES = [
        ("scheduled", _("Scheduled")),
        ("in_progress", _("In Progress")),
        ("completed", _("Completed")),
        ("cancelled", _("Cancelled")),
        ("missed", _("Missed")),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="follow_ups",
        verbose_name=_("Patient"),
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="doctor_follow_ups",
        verbose_name=_("Doctor"),
    )

    title = models.CharField(max_length=255, verbose_name=_("Title"))

    description = models.TextField(verbose_name=_("Description"))

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
        verbose_name=_("Priority"),
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="scheduled",
        verbose_name=_("Status"),
    )

    scheduled_date = models.DateTimeField(verbose_name=_("Scheduled Date"))

    actual_date = models.DateTimeField(
        null=True, blank=True, verbose_name=_("Actual Date")
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    reminder_sent = models.BooleanField(default=False, verbose_name=_("Reminder Sent"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Follow Up")
        verbose_name_plural = _("Follow Ups")
        ordering = ["-scheduled_date"]

    def __str__(self):
        return f"{self.title} - {self.patient.user.get_full_name()}"

    def is_overdue(self):
        """التحقق من تجاوز الموعد"""
        from django.utils import timezone

        return self.status == "scheduled" and self.scheduled_date < timezone.now()


class Treatment(models.Model):
    """نموذج العلاج"""

    TREATMENT_TYPES = [
        ("medication", _("Medication")),
        ("therapy", _("Therapy")),
        ("surgery", _("Surgery")),
        ("procedure", _("Medical Procedure")),
        ("diet", _("Diet Plan")),
        ("exercise", _("Exercise Plan")),
    ]

    FREQUENCY_CHOICES = [
        ("once", _("Once")),
        ("daily", _("Daily")),
        ("weekly", _("Weekly")),
        ("monthly", _("Monthly")),
        ("as_needed", _("As Needed")),
    ]

    follow_up = models.ForeignKey(
        FollowUp,
        on_delete=models.CASCADE,
        related_name="treatments",
        verbose_name=_("Follow Up"),
    )

    treatment_type = models.CharField(
        max_length=20, choices=TREATMENT_TYPES, verbose_name=_("Treatment Type")
    )

    name = models.CharField(max_length=255, verbose_name=_("Name"))

    description = models.TextField(verbose_name=_("Description"))

    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, verbose_name=_("Frequency")
    )

    duration = models.CharField(max_length=100, verbose_name=_("Duration"))

    instructions = models.TextField(verbose_name=_("Instructions"))

    start_date = models.DateField(verbose_name=_("Start Date"))

    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"))

    is_completed = models.BooleanField(default=False, verbose_name=_("Is Completed"))

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Treatment")
        verbose_name_plural = _("Treatments")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} - {self.follow_up.patient.user.get_full_name()}"

    def is_active(self):
        """التحقق من نشاط العلاج"""
        from django.utils import timezone

        today = timezone.now().date()
        return (
            not self.is_completed
            and self.start_date <= today
            and (not self.end_date or self.end_date >= today)
        )


class Progress(models.Model):
    """نموذج تقدم العلاج"""

    treatment = models.ForeignKey(
        Treatment,
        on_delete=models.CASCADE,
        related_name="progress_records",
        verbose_name=_("Treatment"),
    )

    date = models.DateField(verbose_name=_("Date"))

    status = models.TextField(verbose_name=_("Status"))

    observations = models.TextField(verbose_name=_("Observations"))

    complications = models.TextField(blank=True, verbose_name=_("Complications"))

    next_steps = models.TextField(verbose_name=_("Next Steps"))

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="recorded_progress",
        verbose_name=_("Recorded By"),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        verbose_name = _("Progress")
        verbose_name_plural = _("Progress Records")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.treatment} - {self.date}"


class Invoice(models.Model):
    """نموذج الفاتورة"""

    STATUS_CHOICES = [
        ("draft", _("Draft")),
        ("pending", _("Pending")),
        ("paid", _("Paid")),
        ("overdue", _("Overdue")),
        ("cancelled", _("Cancelled")),
    ]

    PAYMENT_METHOD_CHOICES = [
        ("cash", _("Cash")),
        ("credit_card", _("Credit Card")),
        ("debit_card", _("Debit Card")),
        ("bank_transfer", _("Bank Transfer")),
        ("insurance", _("Insurance")),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="medical_invoices",
        verbose_name=_("Patient"),
    )

    invoice_number = models.CharField(
        max_length=50, unique=True, verbose_name=_("Invoice Number")
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="draft", verbose_name=_("Status")
    )

    issue_date = models.DateField(verbose_name=_("Issue Date"))

    due_date = models.DateField(verbose_name=_("Due Date"))

    payment_method = models.CharField(
        max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name=_("Payment Method")
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Subtotal"),
    )

    tax = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Tax"),
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Discount"),
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Total"),
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
        ordering = ["-issue_date"]

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.patient.user.get_full_name()}"

    def clean(self):
        """التحقق من صحة البيانات"""
        if self.due_date and self.issue_date and self.due_date < self.issue_date:
            raise ValidationError(_("Due date cannot be before issue date"))

        if self.discount > self.subtotal:
            raise ValidationError(_("Discount cannot be greater than subtotal"))

    def save(self, *args, **kwargs):
        """حفظ الفاتورة مع حساب المجموع"""
        self.total = self.calculate_total()
        super().save(*args, **kwargs)

    def calculate_total(self):
        """حساب المجموع الكلي"""
        return self.subtotal + self.tax - self.discount

    def is_overdue(self):
        """التحقق من تجاوز موعد السداد"""
        from django.utils import timezone

        if self.status == "pending" and self.due_date < timezone.now().date():
            self.status = "overdue"
            self.save(update_fields=["status"])
            return True
        return False


class InvoiceItem(models.Model):
    """نموذج عنصر الفاتورة"""

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Invoice"),
    )

    description = models.CharField(max_length=255, verbose_name=_("Description"))

    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], verbose_name=_("Quantity")
    )

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Unit Price"),
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Total"),
    )

    class Meta:
        verbose_name = _("Invoice Item")
        verbose_name_plural = _("Invoice Items")
        ordering = ["id"]

    def __str__(self):
        return f"{self.description} - {self.invoice.invoice_number}"

    def clean(self):
        """التحقق من صحة البيانات"""
        if self.quantity * self.unit_price != self.total:
            raise ValidationError(
                _("Total must be equal to quantity multiplied by unit price")
            )

    def save(self, *args, **kwargs):
        """حفظ عنصر الفاتورة مع حساب المجموع"""
        # حساب المجموع قبل الحفظ
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # تحديث مجموع الفاتورة
        self.invoice.subtotal = sum(item.total for item in self.invoice.items.all())
        self.invoice.save()


class Payment(models.Model):
    """نموذج الدفع"""

    STATUS_CHOICES = [
        ("pending", _("Pending")),
        ("completed", _("Completed")),
        ("failed", _("Failed")),
        ("refunded", _("Refunded")),
    ]

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name=_("Invoice"),
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Amount"),
    )

    payment_method = models.CharField(
        max_length=20,
        choices=Invoice.PAYMENT_METHOD_CHOICES,
        verbose_name=_("Payment Method"),
    )

    transaction_id = models.CharField(
        max_length=100, blank=True, verbose_name=_("Transaction ID")
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )

    payment_date = models.DateTimeField(verbose_name=_("Payment Date"))

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ["-payment_date"]

    def __str__(self):
        return f"Payment {self.id} - {self.invoice.invoice_number}"

    def clean(self):
        """التحقق من صحة البيانات"""
        if self.amount > self.invoice.total:
            raise ValidationError(
                _("Payment amount cannot be greater than invoice total")
            )

        total_payments = sum(
            payment.amount for payment in self.invoice.payments.exclude(id=self.id)
        )
        if total_payments + self.amount > self.invoice.total:
            raise ValidationError(_("Total payments cannot exceed invoice total"))

    def save(self, *args, **kwargs):
        """حفظ الدفع مع تحديث حالة الفاتورة"""
        super().save(*args, **kwargs)

        # تحديث حالة الفاتورة
        total_payments = sum(
            payment.amount
            for payment in self.invoice.payments.filter(status="completed")
        )
        if total_payments >= self.invoice.total:
            self.invoice.status = "paid"
            self.invoice.save(update_fields=["status"])
        elif total_payments > 0:
            self.invoice.status = "pending"
            self.invoice.save(update_fields=["status"])


class Insurance(models.Model):
    """نموذج التأمين"""

    STATUS_CHOICES = [
        ("active", _("Active")),
        ("inactive", _("Inactive")),
        ("expired", _("Expired")),
        ("pending", _("Pending Approval")),
    ]

    COVERAGE_TYPE_CHOICES = [
        ("full", _("Full Coverage")),
        ("partial", _("Partial Coverage")),
        ("basic", _("Basic Coverage")),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="insurances",
        verbose_name=_("Patient"),
    )

    provider = models.CharField(max_length=100, verbose_name=_("Insurance Provider"))

    policy_number = models.CharField(
        max_length=50, unique=True, verbose_name=_("Policy Number")
    )

    coverage_type = models.CharField(
        max_length=20, choices=COVERAGE_TYPE_CHOICES, verbose_name=_("Coverage Type")
    )

    coverage_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text=_("Coverage percentage (0-100)"),
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name=_("Coverage Percentage"),
    )

    start_date = models.DateField(verbose_name=_("Start Date"))

    end_date = models.DateField(verbose_name=_("End Date"))

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )

    deductible = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Deductible Amount"),
    )

    max_coverage = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Maximum Coverage Amount"),
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Insurance")
        verbose_name_plural = _("Insurances")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.provider} ({self.policy_number})"

    def clean(self):
        """التحقق من صحة البيانات"""
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError(_("End date cannot be before start date"))

    def save(self, *args, **kwargs):
        """حفظ التأمين مع تحديث الحالة"""
        from django.utils import timezone

        today = timezone.now().date()

        if self.end_date < today:
            self.status = "expired"
        elif self.start_date <= today <= self.end_date and self.status != "inactive":
            self.status = "active"

        super().save(*args, **kwargs)

    def is_active(self):
        """التحقق من نشاط التأمين"""
        from django.utils import timezone

        today = timezone.now().date()
        return self.status == "active" and self.start_date <= today <= self.end_date

    def calculate_coverage(self, amount):
        """حساب مبلغ التغطية"""
        if not self.is_active():
            return Decimal("0.00")

        # حساب التغطية بناءً على النسبة المئوية
        covered_amount = amount * Decimal(str(self.coverage_percentage / 100))

        # التأكد من أن المبلغ لا يتجاوز الحد الأقصى للتغطية
        if covered_amount > self.max_coverage:
            return self.max_coverage

        return covered_amount


class InsuranceClaim(models.Model):
    """نموذج مطالبة التأمين"""

    STATUS_CHOICES = [
        ("submitted", _("Submitted")),
        ("processing", _("Processing")),
        ("approved", _("Approved")),
        ("rejected", _("Rejected")),
        ("paid", _("Paid")),
    ]

    insurance = models.ForeignKey(
        Insurance,
        on_delete=models.PROTECT,
        related_name="claims",
        verbose_name=_("Insurance"),
    )

    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.PROTECT,
        related_name="insurance_claims",
        verbose_name=_("Invoice"),
    )

    claim_number = models.CharField(
        max_length=50, unique=True, verbose_name=_("Claim Number")
    )

    submission_date = models.DateField(verbose_name=_("Submission Date"))

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="submitted",
        verbose_name=_("Status"),
    )

    amount_claimed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Amount Claimed"),
    )

    amount_approved = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name=_("Amount Approved"),
    )

    rejection_reason = models.TextField(blank=True, verbose_name=_("Rejection Reason"))

    documents = models.FileField(
        upload_to="insurance_claims/",
        blank=True,
        verbose_name=_("Supporting Documents"),
    )

    notes = models.TextField(blank=True, verbose_name=_("Notes"))

    processed_date = models.DateField(
        null=True, blank=True, verbose_name=_("Processed Date")
    )

    payment_date = models.DateField(
        null=True, blank=True, verbose_name=_("Payment Date")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Insurance Claim")
        verbose_name_plural = _("Insurance Claims")
        ordering = ["-submission_date"]

    def __str__(self):
        return f"Claim {self.claim_number} - {self.insurance.policy_number}"

    def clean(self):
        """التحقق من صحة البيانات"""
        if not self.insurance.is_active():
            raise ValidationError(_("Insurance policy is not active"))

        if self.amount_claimed > self.invoice.total:
            raise ValidationError(
                _("Claimed amount cannot be greater than invoice total")
            )

        if self.amount_approved and self.amount_approved > self.amount_claimed:
            raise ValidationError(
                _("Approved amount cannot be greater than claimed amount")
            )

        if self.status == "rejected" and not self.rejection_reason:
            raise ValidationError(
                _("Rejection reason is required when claim is rejected")
            )

        if self.status == "paid" and not self.payment_date:
            raise ValidationError(_("Payment date is required when claim is paid"))

    def save(self, *args, **kwargs):
        """حفظ المطالبة مع التحقق من الحالة"""
        if not self.pk:  # إذا كانت مطالبة جديدة
            if not self.amount_claimed:
                self.amount_claimed = self.insurance.calculate_coverage(
                    self.invoice.total
                )

        if self.status == "approved" and not self.processed_date:
            self.processed_date = timezone.now().date()

        super().save(*args, **kwargs)

    def is_approved(self):
        """التحقق من الموافقة على المطالبة"""
        return self.status == "approved"

    def is_rejected(self):
        """التحقق من رفض المطالبة"""
        return self.status == "rejected"

    def is_paid(self):
        """التحقق من دفع المطالبة"""
        return self.status == "paid"
