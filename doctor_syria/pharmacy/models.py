"""
Models for the pharmacy application.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import Patient
from core.models import TimestampMixin


class Medicine(TimestampMixin):
    """
    Model for managing medicines.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('اسم الدواء')
    )
    name_ar = models.CharField(
        max_length=255,
        verbose_name=_('اسم الدواء بالعربية')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('الوصف')
    )
    description_ar = models.TextField(
        blank=True,
        verbose_name=_('الوصف بالعربية')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('السعر')
    )
    quantity = models.IntegerField(
        default=0,
        verbose_name=_('الكمية المتوفرة')
    )
    minimum_quantity = models.IntegerField(
        default=10,
        verbose_name=_('الحد الأدنى للكمية')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('نشط')
    )

    class Meta:
        verbose_name = _('دواء')
        verbose_name_plural = _('الأدوية')
        ordering = ['name']

    def __str__(self):
        return self.name_ar or self.name


class Prescription(TimestampMixin):
    """
    Model for managing prescriptions.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='prescriptions',
        verbose_name=_('المريض')
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_('ملاحظات')
    )
    is_filled = models.BooleanField(
        default=False,
        verbose_name=_('تم صرف الوصفة')
    )

    class Meta:
        verbose_name = _('وصفة طبية')
        verbose_name_plural = _('الوصفات الطبية')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient} - {self.created_at}"


class PrescriptionItem(TimestampMixin):
    """
    Model for managing prescription items.
    """
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('الوصفة الطبية')
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name='prescription_items',
        verbose_name=_('الدواء')
    )
    quantity = models.IntegerField(
        verbose_name=_('الكمية')
    )
    dosage = models.CharField(
        max_length=255,
        verbose_name=_('الجرعة')
    )
    instructions = models.TextField(
        blank=True,
        verbose_name=_('تعليمات')
    )

    class Meta:
        verbose_name = _('عنصر الوصفة')
        verbose_name_plural = _('عناصر الوصفة')
        ordering = ['medicine__name']

    def __str__(self):
        return f"{self.medicine} - {self.quantity}"
