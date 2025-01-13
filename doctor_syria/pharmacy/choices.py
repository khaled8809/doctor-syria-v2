from django.db import models
from django.utils.translation import gettext_lazy as _


class MedicineCategory(models.TextChoices):
    """
    فئات الأدوية
    """

    PRESCRIPTION = "prescription", _("أدوية وصفة طبية")
    OTC = "otc", _("أدوية بدون وصفة")
    CONTROLLED = "controlled", _("أدوية مراقبة")
    SUPPLEMENTS = "supplements", _("مكملات غذائية")
    MEDICAL_SUPPLIES = "medical_supplies", _("مستلزمات طبية")
    COSMETICS = "cosmetics", _("مستحضرات تجميل")
    OTHER = "other", _("أخرى")


class MedicineForm(models.TextChoices):
    """
    أشكال الأدوية
    """

    TABLET = "tablet", _("أقراص")
    CAPSULE = "capsule", _("كبسولات")
    SYRUP = "syrup", _("شراب")
    INJECTION = "injection", _("حقن")
    CREAM = "cream", _("كريم")
    OINTMENT = "ointment", _("مرهم")
    DROPS = "drops", _("قطرات")
    INHALER = "inhaler", _("بخاخ")
    SUPPOSITORY = "suppository", _("تحاميل")
    PATCH = "patch", _("لصقات")


class StorageCondition(models.TextChoices):
    """
    ظروف التخزين
    """

    ROOM_TEMP = "room_temp", _("درجة حرارة الغرفة")
    REFRIGERATED = "refrigerated", _("مبرد")
    FROZEN = "frozen", _("مجمد")
    COOL_DRY = "cool_dry", _("بارد وجاف")
    PROTECTED_LIGHT = "protected_light", _("محمي من الضوء")


class OrderStatus(models.TextChoices):
    """
    حالات الطلبات
    """

    PENDING = "pending", _("قيد الانتظار")
    CONFIRMED = "confirmed", _("مؤكد")
    PROCESSING = "processing", _("قيد التجهيز")
    READY = "ready", _("جاهز للتسليم")
    DELIVERED = "delivered", _("تم التسليم")
    CANCELLED = "cancelled", _("ملغي")


class PaymentMethod(models.TextChoices):
    """
    طرق الدفع
    """

    CASH = "cash", _("نقداً")
    CREDIT_CARD = "credit_card", _("بطاقة ائتمان")
    INSURANCE = "insurance", _("تأمين صحي")
    BANK_TRANSFER = "bank_transfer", _("تحويل بنكي")


class PaymentStatus(models.TextChoices):
    """
    حالات الدفع
    """

    PENDING = "pending", _("قيد الانتظار")
    PAID = "paid", _("مدفوع")
    PARTIALLY_PAID = "partially_paid", _("مدفوع جزئياً")
    REFUNDED = "refunded", _("مسترد")
    FAILED = "failed", _("فشل الدفع")
