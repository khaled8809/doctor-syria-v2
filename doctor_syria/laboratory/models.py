from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from accounts.models import Doctor, Laboratory, Patient


class TestCategory(models.Model):
    """فئات التحاليل"""

    name = models.CharField(_("الاسم"), max_length=100)
    description = models.TextField(_("الوصف"))
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name=_("الفئة الأب"),
    )
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    is_active = models.BooleanField(_("نشط"), default=True)

    class Meta:
        verbose_name = _("فئة تحاليل")
        verbose_name_plural = _("فئات التحاليل")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class LabTest(models.Model):
    """التحاليل المخبرية"""

    SAMPLE_TYPES = [
        ("blood", "دم"),
        ("urine", "بول"),
        ("stool", "براز"),
        ("saliva", "لعاب"),
        ("tissue", "نسيج"),
        ("swab", "مسحة"),
        ("other", "أخرى"),
    ]

    PRIORITY_LEVELS = [
        ("routine", "روتيني"),
        ("urgent", "عاجل"),
        ("emergency", "طارئ"),
    ]

    name = models.CharField(_("الاسم"), max_length=200)
    code = models.CharField(_("الرمز"), max_length=50, unique=True)
    category = models.ForeignKey(
        TestCategory,
        on_delete=models.CASCADE,
        related_name="tests",
        verbose_name=_("الفئة"),
    )
    description = models.TextField(_("الوصف"))
    preparation_instructions = models.TextField(_("تعليمات التحضير"))
    sample_type = models.CharField(
        _("نوع العينة"), max_length=20, choices=SAMPLE_TYPES
    )
    sample_volume = models.CharField(_("حجم العينة"), max_length=50)
    processing_time = models.DurationField(_("وقت المعالجة"))
    price = models.DecimalField(_("السعر"), max_digits=10, decimal_places=2)
    is_active = models.BooleanField(_("نشط"), default=True)
    requires_fasting = models.BooleanField(_("يتطلب صيام"), default=False)
    fasting_hours = models.PositiveIntegerField(
        _("ساعات الصيام"), null=True, blank=True
    )
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    class Meta:
        verbose_name = _("تحليل مخبري")
        verbose_name_plural = _("التحاليل المخبرية")
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class TestParameter(models.Model):
    """معايير التحليل"""

    PARAMETER_TYPES = [
        ("numeric", "رقمي"),
        ("text", "نصي"),
        ("choice", "اختياري"),
        ("range", "مجال"),
    ]

    test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE,
        related_name="parameters",
        verbose_name=_("التحليل"),
    )
    name = models.CharField(_("الاسم"), max_length=100)
    parameter_type = models.CharField(
        _("نوع المعيار"), max_length=20, choices=PARAMETER_TYPES
    )
    unit = models.CharField(_("الوحدة"), max_length=50, blank=True)
    possible_values = models.JSONField(
        _("القيم المحتملة"), null=True, blank=True
    )  # For choice type
    order = models.PositiveIntegerField(_("الترتيب"), default=0)

    class Meta:
        verbose_name = _("معيار تحليل")
        verbose_name_plural = _("معايير التحليل")
        ordering = ["test", "order"]

    def __str__(self):
        return f"{self.test.name} - {self.name}"


class ReferenceRange(models.Model):
    """المعدلات الطبيعية"""

    parameter = models.ForeignKey(
        TestParameter,
        on_delete=models.CASCADE,
        related_name="reference_ranges",
        verbose_name=_("المعيار"),
    )
    min_value = models.DecimalField(
        _("القيمة الدنيا"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    max_value = models.DecimalField(
        _("القيمة القصوى"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    gender = models.CharField(_("الجنس"), max_length=20, null=True, blank=True)
    min_age = models.PositiveIntegerField(_("العمر الأدنى"), null=True, blank=True)
    max_age = models.PositiveIntegerField(_("العمر الأقصى"), null=True, blank=True)
    description = models.TextField(_("الوصف"), blank=True)
    condition = models.CharField(
        _("الحالة"), max_length=100, blank=True
    )  # e.g., pregnancy, diabetes

    class Meta:
        verbose_name = _("معدل طبيعي")
        verbose_name_plural = _("المعدلات الطبيعية")

    def __str__(self):
        return f"{self.parameter.name} ({self.min_value}-{self.max_value} {self.parameter.unit})"


class TestRequest(models.Model):
    """طلبات التحليل"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("approved", "تمت الموافقة"),
        ("sample_collected", "تم جمع العينة"),
        ("processing", "قيد المعالجة"),
        ("completed", "مكتمل"),
        ("cancelled", "ملغي"),
    ]

    PRIORITY_CHOICES = [
        ("routine", "روتيني"),
        ("urgent", "عاجل"),
        ("emergency", "طارئ"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="test_requests",
        verbose_name=_("المريض"),
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="test_requests",
        null=True,
        blank=True,
        verbose_name=_("الطبيب"),
    )
    laboratory = models.ForeignKey(
        Laboratory,
        on_delete=models.CASCADE,
        related_name="test_requests",
        verbose_name=_("المختبر"),
    )
    tests = models.ManyToManyField(
        LabTest,
        related_name="test_requests",
        verbose_name=_("التحاليل"),
    )
    status = models.CharField(
        _("الحالة"), max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    priority = models.CharField(
        _("الأولوية"),
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="routine",
    )
    diagnosis = models.TextField(_("التشخيص"), blank=True)
    clinical_notes = models.TextField(_("ملاحظات سريرية"), blank=True)
    requested_date = models.DateTimeField(_("تاريخ الطلب"), auto_now_add=True)
    appointment_date = models.DateTimeField(_("موعد التحليل"))
    completion_date = models.DateTimeField(
        _("تاريخ الإكمال"), null=True, blank=True
    )
    is_fasting = models.BooleanField(_("صائم"), default=False)
    insurance_approval = models.BooleanField(
        _("موافقة التأمين"), default=False
    )
    total_cost = models.DecimalField(
        _("التكلفة الإجمالية"), max_digits=10, decimal_places=2
    )
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("طلب تحليل")
        verbose_name_plural = _("طلبات التحليل")
        ordering = ["-requested_date"]

    def __str__(self):
        return f"{self.patient} - {self.requested_date}"

    def save(self, *args, **kwargs):
        if not self.total_cost:
            self.total_cost = sum(test.price for test in self.tests.all())
        super().save(*args, **kwargs)


class SampleCollection(models.Model):
    """جمع العينات"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("collected", "تم الجمع"),
        ("rejected", "مرفوض"),
        ("insufficient", "غير كافي"),
        ("contaminated", "ملوث"),
    ]

    test_request = models.OneToOneField(
        TestRequest,
        on_delete=models.CASCADE,
        related_name="sample",
        verbose_name=_("طلب التحليل"),
    )
    collection_date = models.DateTimeField(_("تاريخ الجمع"))
    collected_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="collected_samples",
        verbose_name=_("تم الجمع بواسطة"),
    )
    status = models.CharField(
        _("الحالة"), max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    rejection_reason = models.TextField(_("سبب الرفض"), blank=True)
    container_type = models.CharField(_("نوع الحاوية"), max_length=100)
    storage_location = models.CharField(_("موقع التخزين"), max_length=100)
    temperature = models.DecimalField(
        _("درجة الحرارة"), max_digits=5, decimal_places=2, null=True, blank=True
    )
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("جمع عينة")
        verbose_name_plural = _("جمع العينات")

    def __str__(self):
        return f"عينة {self.test_request}"


class TestResult(models.Model):
    """نتائج التحليل"""

    test_request = models.OneToOneField(
        TestRequest,
        on_delete=models.CASCADE,
        related_name="result",
        verbose_name=_("طلب التحليل"),
    )
    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="performed_tests",
        verbose_name=_("تم التحليل بواسطة"),
    )
    verified_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="verified_tests",
        verbose_name=_("تم التحقق بواسطة"),
    )
    result_date = models.DateTimeField(_("تاريخ النتيجة"), auto_now_add=True)
    results = models.JSONField(_("النتائج"))
    interpretation = models.TextField(_("التفسير"))
    is_normal = models.BooleanField(_("طبيعي"))
    is_critical = models.BooleanField(_("حرج"), default=False)
    critical_values = models.JSONField(_("القيم الحرجة"), null=True, blank=True)
    attachments = models.FileField(
        _("المرفقات"), upload_to="test_results/", null=True, blank=True
    )
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta:
        verbose_name = _("نتيجة تحليل")
        verbose_name_plural = _("نتائج التحليل")

    def __str__(self):
        return f"نتيجة {self.test_request}"


class QualityControl(models.Model):
    """ضبط الجودة"""

    CONTROL_TYPES = [
        ("internal", "داخلي"),
        ("external", "خارجي"),
    ]

    test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE,
        related_name="quality_controls",
        verbose_name=_("التحليل"),
    )
    control_type = models.CharField(
        _("نوع الضبط"), max_length=20, choices=CONTROL_TYPES
    )
    lot_number = models.CharField(_("رقم التشغيلة"), max_length=100)
    control_date = models.DateField(_("تاريخ الضبط"))
    performed_by = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="performed_controls",
        verbose_name=_("تم الضبط بواسطة"),
    )
    expected_results = models.JSONField(_("النتائج المتوقعة"))
    actual_results = models.JSONField(_("النتائج الفعلية"))
    is_passed = models.BooleanField(_("نجح"))
    corrective_action = models.TextField(_("الإجراء التصحيحي"), blank=True)

    class Meta:
        verbose_name = _("ضبط جودة")
        verbose_name_plural = _("ضبط الجودة")

    def __str__(self):
        return f"ضبط جودة {self.test.name} - {self.control_date}"
