from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .choices import UserType

User = get_user_model()


@receiver(pre_save, sender=User)
def set_user_permissions(sender, instance, **kwargs):
    """
    تعيين الصلاحيات حسب نوع المستخدم
    """
    if not instance.pk:  # للمستخدمين الجدد فقط
        if instance.user_type == UserType.ADMIN:
            instance.is_staff = True
            instance.is_superuser = True
        elif instance.user_type in [
            UserType.DOCTOR,
            UserType.PHARMACY,
            UserType.LAB,
            UserType.HOSPITAL,
        ]:
            instance.is_staff = True
            instance.is_superuser = False


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    إنشاء الملف الشخصي للمستخدم بعد إنشاء الحساب
    """
    if created:
        if instance.user_type == UserType.PATIENT:
            from medical_records.models import PatientProfile

            PatientProfile.objects.create(user=instance)
        elif instance.user_type == UserType.DOCTOR:
            from medical_records.models import DoctorProfile

            DoctorProfile.objects.create(user=instance)
        # يمكن إضافة المزيد من الملفات الشخصية حسب نوع المستخدم
