from django.db import models
from django.utils.translation import gettext_lazy as _


class AppointmentStatus(models.TextChoices):
    """
    حالات المواعيد
    """

    PENDING = "pending", _("قيد الانتظار")
    CONFIRMED = "confirmed", _("مؤكد")
    COMPLETED = "completed", _("مكتمل")
    CANCELLED = "cancelled", _("ملغي")
    NO_SHOW = "no_show", _("لم يحضر")


class AppointmentType(models.TextChoices):
    """
    أنواع المواعيد
    """

    CONSULTATION = "consultation", _("استشارة")
    FOLLOW_UP = "follow_up", _("متابعة")
    EMERGENCY = "emergency", _("طوارئ")
    ROUTINE_CHECK = "routine_check", _("فحص روتيني")
    PROCEDURE = "procedure", _("إجراء طبي")


class RecordType(models.TextChoices):
    """
    أنواع السجلات الطبية
    """

    DIAGNOSIS = "diagnosis", _("تشخيص")
    PRESCRIPTION = "prescription", _("وصفة طبية")
    LAB_TEST = "lab_test", _("تحليل مخبري")
    RADIOLOGY = "radiology", _("صورة شعاعية")
    SURGERY = "surgery", _("عملية جراحية")
    VACCINATION = "vaccination", _("تطعيم")
    ALLERGY = "allergy", _("حساسية")
    CHRONIC_CONDITION = "chronic_condition", _("حالة مزمنة")


class Severity(models.TextChoices):
    """
    مستويات الخطورة
    """

    LOW = "low", _("منخفضة")
    MEDIUM = "medium", _("متوسطة")
    HIGH = "high", _("عالية")
    CRITICAL = "critical", _("حرجة")


class AllergyType(models.TextChoices):
    """
    أنواع الحساسية
    """

    FOOD = "food", _("طعام")
    MEDICATION = "medication", _("دواء")
    ENVIRONMENTAL = "environmental", _("بيئية")
    INSECT = "insect", _("حشرات")
    LATEX = "latex", _("لاتكس")
    OTHER = "other", _("أخرى")


class AllergyReaction(models.TextChoices):
    """
    ردود فعل الحساسية
    """

    MILD = "mild", _("خفيفة")
    MODERATE = "moderate", _("متوسطة")
    SEVERE = "severe", _("شديدة")
    ANAPHYLAXIS = "anaphylaxis", _("صدمة تأقية")


class VaccinationType(models.TextChoices):
    """
    أنواع التطعيمات
    """

    ROUTINE = "routine", _("روتيني")
    SEASONAL = "seasonal", _("موسمي")
    TRAVEL = "travel", _("سفر")
    COVID19 = "covid19", _("كوفيد-19")
    OTHER = "other", _("أخرى")
