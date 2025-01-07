from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone
import os

def radiology_image_path(instance, filename):
    """تحديد مسار حفظ صور الأشعة"""
    return f'radiology/images/{instance.result.id}/{filename}'

class RadiologyExamination(models.Model):
    """نموذج الفحوصات الإشعاعية"""
    
    CATEGORY_CHOICES = [
        ('xray', _('X-Ray')),
        ('ct', _('CT Scan')),
        ('mri', _('MRI')),
        ('ultrasound', _('Ultrasound')),
        ('mammogram', _('Mammogram')),
        ('dexa', _('DEXA Scan')),
        ('fluoroscopy', _('Fluoroscopy')),
        ('nuclear', _('Nuclear Medicine')),
        ('other', _('Other')),
    ]
    
    BODY_PART_CHOICES = [
        ('head', _('Head')),
        ('neck', _('Neck')),
        ('chest', _('Chest')),
        ('abdomen', _('Abdomen')),
        ('pelvis', _('Pelvis')),
        ('spine', _('Spine')),
        ('upper_limb', _('Upper Limb')),
        ('lower_limb', _('Lower Limb')),
        ('whole_body', _('Whole Body')),
        ('other', _('Other')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Code'))
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name=_('Category')
    )
    body_part = models.CharField(
        max_length=20,
        choices=BODY_PART_CHOICES,
        verbose_name=_('Body Part')
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Price')
    )
    preparation_instructions = models.TextField(
        blank=True,
        verbose_name=_('Preparation Instructions')
    )
    radiation_dose = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Radiation Dose')
    )
    duration = models.PositiveIntegerField(
        help_text=_('Duration in minutes'),
        verbose_name=_('Duration')
    )
    requires_contrast = models.BooleanField(
        default=False,
        verbose_name=_('Requires Contrast')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = _('Radiology Examination')
        verbose_name_plural = _('Radiology Examinations')
        ordering = ['name']

class RadiologyRequest(models.Model):
    """نموذج طلبات الأشعة"""
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('scheduled', _('Scheduled')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]
    
    PRIORITY_CHOICES = [
        ('normal', _('Normal')),
        ('urgent', _('Urgent')),
        ('emergency', _('Emergency')),
    ]
    
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='radiology_requests',
        verbose_name=_('Patient')
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requested_radiologies',
        verbose_name=_('Doctor')
    )
    examination = models.ForeignKey(
        RadiologyExamination,
        on_delete=models.CASCADE,
        related_name='requests',
        verbose_name=_('Examination')
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name=_('Status')
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name=_('Priority')
    )
    clinical_history = models.TextField(
        blank=True,
        verbose_name=_('Clinical History')
    )
    clinical_findings = models.TextField(
        blank=True,
        verbose_name=_('Clinical Findings')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )
    requested_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Requested At')
    )
    scheduled_for = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Scheduled For')
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completed At')
    )
    technician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='performed_radiologies',
        verbose_name=_('Technician')
    )
    radiologist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interpreted_radiologies',
        verbose_name=_('Radiologist')
    )
    equipment = models.ForeignKey(
        'RadiologyEquipment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='examinations',
        verbose_name=_('Equipment')
    )

    def __str__(self):
        return f"{self.examination.name} - {self.patient.get_full_name()}"

    class Meta:
        verbose_name = _('Radiology Request')
        verbose_name_plural = _('Radiology Requests')
        ordering = ['-requested_at']

class RadiologyResult(models.Model):
    """نموذج نتائج الأشعة"""
    
    request = models.OneToOneField(
        RadiologyRequest,
        on_delete=models.CASCADE,
        related_name='result',
        verbose_name=_('Request')
    )
    findings = models.TextField(verbose_name=_('Findings'))
    impression = models.TextField(verbose_name=_('Impression'))
    recommendations = models.TextField(
        blank=True,
        verbose_name=_('Recommendations')
    )
    technical_notes = models.TextField(
        blank=True,
        verbose_name=_('Technical Notes')
    )
    radiation_dose = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Actual Radiation Dose')
    )
    contrast_used = models.BooleanField(
        default=False,
        verbose_name=_('Contrast Used')
    )
    contrast_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Contrast Type')
    )
    contrast_volume = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Contrast Volume')
    )
    performed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Performed At')
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Verified At')
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_radiologies',
        verbose_name=_('Verified By')
    )

    def __str__(self):
        return f"Result for {self.request}"

    class Meta:
        verbose_name = _('Radiology Result')
        verbose_name_plural = _('Radiology Results')
        ordering = ['-performed_at']

class RadiologyImage(models.Model):
    """نموذج صور الأشعة"""
    
    result = models.ForeignKey(
        RadiologyResult,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Result')
    )
    image = models.ImageField(
        upload_to=radiology_image_path,
        verbose_name=_('Image')
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Description')
    )
    sequence_number = models.PositiveIntegerField(
        default=1,
        verbose_name=_('Sequence Number')
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Uploaded At')
    )

    def __str__(self):
        return f"Image {self.sequence_number} for {self.result}"

    class Meta:
        verbose_name = _('Radiology Image')
        verbose_name_plural = _('Radiology Images')
        ordering = ['sequence_number']

class RadiologyEquipment(models.Model):
    """نموذج أجهزة الأشعة"""
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    model = models.CharField(max_length=255, verbose_name=_('Model'))
    manufacturer = models.CharField(max_length=255, verbose_name=_('Manufacturer'))
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Serial Number')
    )
    equipment_type = models.CharField(
        max_length=20,
        choices=RadiologyExamination.CATEGORY_CHOICES,
        verbose_name=_('Equipment Type')
    )
    installation_date = models.DateField(verbose_name=_('Installation Date'))
    warranty_expiry = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Warranty Expiry')
    )
    last_maintenance = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Last Maintenance')
    )
    next_maintenance = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Next Maintenance')
    )
    calibration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Calibration Date')
    )
    room_number = models.CharField(
        max_length=50,
        verbose_name=_('Room Number')
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', _('Active')),
            ('maintenance', _('Under Maintenance')),
            ('repair', _('Under Repair')),
            ('inactive', _('Inactive')),
        ],
        default='active',
        verbose_name=_('Status')
    )
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    def __str__(self):
        return f"{self.name} - {self.model}"

    def needs_maintenance(self):
        if self.next_maintenance:
            return self.next_maintenance <= timezone.now().date()
        return False

    def needs_calibration(self):
        if self.calibration_date:
            days_since_calibration = (timezone.now().date() - self.calibration_date).days
            return days_since_calibration > 365  # سنة واحدة
        return True

    class Meta:
        verbose_name = _('Radiology Equipment')
        verbose_name_plural = _('Radiology Equipment')
        ordering = ['name']

class EquipmentMaintenance(models.Model):
    """نموذج صيانة الأجهزة"""
    
    equipment = models.ForeignKey(
        RadiologyEquipment,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        verbose_name=_('Equipment')
    )
    maintenance_type = models.CharField(
        max_length=20,
        choices=[
            ('preventive', _('Preventive')),
            ('corrective', _('Corrective')),
            ('calibration', _('Calibration')),
        ],
        verbose_name=_('Maintenance Type')
    )
    maintenance_date = models.DateField(verbose_name=_('Maintenance Date'))
    performed_by = models.CharField(
        max_length=255,
        verbose_name=_('Performed By')
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_('Cost')
    )
    description = models.TextField(verbose_name=_('Description'))
    actions_taken = models.TextField(verbose_name=_('Actions Taken'))
    parts_replaced = models.TextField(
        blank=True,
        verbose_name=_('Parts Replaced')
    )
    next_maintenance = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Next Maintenance Due')
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('completed', _('Completed')),
            ('pending', _('Pending')),
            ('failed', _('Failed')),
        ],
        default='completed',
        verbose_name=_('Status')
    )
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    def __str__(self):
        return f"{self.equipment} - {self.maintenance_type} ({self.maintenance_date})"

    class Meta:
        verbose_name = _('Equipment Maintenance')
        verbose_name_plural = _('Equipment Maintenance')
        ordering = ['-maintenance_date']
