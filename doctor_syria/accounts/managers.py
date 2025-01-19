from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from .choices import UserType


class CustomUserManager(BaseUserManager):
    """
    مدير مخصص للمستخدم حيث البريد الإلكتروني هو المعرف الفريد
    للمصادقة بدلاً من اسم المستخدم.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("يجب تحديد البريد الإلكتروني"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("user_type", UserType.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    def doctors(self):
        """جلب جميع الأطباء"""
        return self.filter(user_type=UserType.DOCTOR, is_active=True)

    def patients(self):
        """جلب جميع المرضى"""
        return self.filter(user_type=UserType.PATIENT, is_active=True)

    def pharmacies(self):
        """جلب جميع الصيدليات"""
        return self.filter(user_type=UserType.PHARMACY, is_active=True)

    def labs(self):
        """جلب جميع المختبرات"""
        return self.filter(user_type=UserType.LAB, is_active=True)

    def hospitals(self):
        """جلب جميع المستشفيات"""
        return self.filter(user_type=UserType.HOSPITAL, is_active=True)
