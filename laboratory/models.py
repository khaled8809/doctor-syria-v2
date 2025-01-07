from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Test(models.Model):
    """نموذج التحاليل المخبرية"""
    
    CATEGORY_CHOICES = [
        ('blood', _('Blood Test')),
        ('urine', _('Urine Test')),
        ('stool', _('Stool Test')),
        ('imaging', _('Imaging')),
        ('culture', _('Culture')),
        ('other', _('Other')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Code'))
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name=_('Category')
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
    normal_range = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Normal Range')
    )
    unit = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Unit')
    )
    processing_time = models.PositiveIntegerField(
        help_text=_('Processing time in hours'),
        verbose_name=_('Processing Time')
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
        verbose_name = _('Test')
        verbose_name_plural = _('Tests')
        ordering = ['name']

class TestRequest(models.Model):
    """نموذج طلبات التحاليل"""
    
    STATUS_CHOICES = [
        ('pending', _('Pending')),
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
        related_name='test_requests',
        verbose_name=_('Patient')
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='requested_tests',
        verbose_name=_('Doctor')
    )
    tests = models.ManyToManyField(
        Test,
        related_name='requests',
        verbose_name=_('Tests')
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
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )
    requested_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Requested At')
    )
    scheduled_for = models.DateTimeField(
        verbose_name=_('Scheduled For')
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Completed At')
    )
    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='processed_tests',
        verbose_name=_('Processed By')
    )

    def __str__(self):
        return f"Test Request #{self.pk} - {self.patient.get_full_name()}"

    def get_total_price(self):
        return sum(test.price for test in self.tests.all())

    class Meta:
        verbose_name = _('Test Request')
        verbose_name_plural = _('Test Requests')
        ordering = ['-requested_at']

class TestResult(models.Model):
    """نموذج نتائج التحاليل"""
    
    test_request = models.ForeignKey(
        TestRequest,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name=_('Test Request')
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        verbose_name=_('Test')
    )
    value = models.CharField(
        max_length=255,
        verbose_name=_('Value')
    )
    is_normal = models.BooleanField(
        default=True,
        verbose_name=_('Is Normal')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes')
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='performed_tests',
        verbose_name=_('Performed By')
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='verified_tests',
        verbose_name=_('Verified By')
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

    def __str__(self):
        return f"{self.test.name} - {self.test_request.patient.get_full_name()}"

    class Meta:
        verbose_name = _('Test Result')
        verbose_name_plural = _('Test Results')
        ordering = ['-performed_at']

class LabEquipment(models.Model):
    """نموذج معدات المختبر"""
    
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    model = models.CharField(max_length=255, verbose_name=_('Model'))
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Serial Number')
    )
    manufacturer = models.CharField(max_length=255, verbose_name=_('Manufacturer'))
    purchase_date = models.DateField(verbose_name=_('Purchase Date'))
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
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', _('Active')),
            ('maintenance', _('Under Maintenance')),
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

    class Meta:
        verbose_name = _('Lab Equipment')
        verbose_name_plural = _('Lab Equipment')
        ordering = ['name']

class QualityControl(models.Model):
    """نموذج ضبط الجودة"""
    
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name='quality_controls',
        verbose_name=_('Test')
    )
    equipment = models.ForeignKey(
        LabEquipment,
        on_delete=models.CASCADE,
        verbose_name=_('Equipment')
    )
    control_date = models.DateField(verbose_name=_('Control Date'))
    control_value = models.CharField(
        max_length=100,
        verbose_name=_('Control Value')
    )
    expected_range = models.CharField(
        max_length=100,
        verbose_name=_('Expected Range')
    )
    is_passed = models.BooleanField(verbose_name=_('Is Passed'))
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='quality_controls',
        verbose_name=_('Performed By')
    )
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    def __str__(self):
        return f"QC - {self.test.name} ({self.control_date})"

    class Meta:
        verbose_name = _('Quality Control')
        verbose_name_plural = _('Quality Controls')
        ordering = ['-control_date']
