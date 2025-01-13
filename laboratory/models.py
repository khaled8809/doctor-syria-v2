from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class LabTest(models.Model):
    TEST_CATEGORIES = [
        ("blood", _("تحليل دم")),
        ("urine", _("تحليل بول")),
        ("stool", _("تحليل براز")),
        ("other", _("أخرى")),
    ]

    name = models.CharField(_("اسم التحليل"), max_length=100)
    code = models.CharField(_("رمز التحليل"), max_length=20, unique=True)
    category = models.CharField(
        _("فئة التحليل"), max_length=20, choices=TEST_CATEGORIES
    )
    description = models.TextField(_("وصف التحليل"), blank=True)
    price = models.DecimalField(_("السعر"), max_digits=10, decimal_places=2)
    normal_range = models.CharField(_("النطاق الطبيعي"), max_length=100, blank=True)
    unit = models.CharField(_("وحدة القياس"), max_length=20)
    is_active = models.BooleanField(_("نشط"), default=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    class Meta:
        verbose_name = _("تحليل مخبري")
        verbose_name_plural = _("تحاليل مخبرية")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class LabResult(models.Model):
    RESULT_STATUS = [
        ("normal", _("طبيعي")),
        ("abnormal", _("غير طبيعي")),
        ("critical", _("حرج")),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lab_results",
        verbose_name=_("المريض"),
    )
    test = models.ForeignKey(
        LabTest,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name=_("التحليل"),
    )
    value = models.CharField(_("النتيجة"), max_length=100)
    status = models.CharField(
        _("الحالة"), max_length=20, choices=RESULT_STATUS, default="normal"
    )
    notes = models.TextField(_("ملاحظات"), blank=True)
    performed_at = models.DateTimeField(_("تاريخ إجراء التحليل"), auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_lab_results",
        verbose_name=_("تم الإنشاء بواسطة"),
    )

    class Meta:
        verbose_name = _("نتيجة تحليل")
        verbose_name_plural = _("نتائج التحاليل")
        ordering = ["-performed_at"]

    def __str__(self):
        return f"{self.test.name} - {self.patient} ({self.performed_at.date()})"
