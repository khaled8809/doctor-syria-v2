from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):
    """نموذج المستخدم المخصص"""
    
    class Roles(models.TextChoices):
        ADMIN = 'admin', _('مدير')
        DOCTOR = 'doctor', _('طبيب')
        NURSE = 'nurse', _('ممرض')
        PHARMACIST = 'pharmacist', _('صيدلي')
        LAB_TECHNICIAN = 'lab_technician', _('فني مختبر')
        RECEPTIONIST = 'receptionist', _('موظف استقبال')
        PATIENT = 'patient', _('مريض')

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.PATIENT,
        verbose_name=_('الدور')
    )
    
    phone = PhoneNumberField(
        unique=True,
        null=True,
        blank=True,
        verbose_name=_('رقم الهاتف')
    )
    
    address = models.TextField(
        blank=True,
        verbose_name=_('العنوان')
    )
    
    birth_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('تاريخ الميلاد')
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        verbose_name=_('الصورة الشخصية')
    )
    
    # معلومات الطبيب
    specialization = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('التخصص')
    )
    
    license_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('رقم الترخيص')
    )

    # معلومات المريض
    blood_type = models.CharField(
        max_length=5,
        blank=True,
        verbose_name=_('فصيلة الدم')
    )
    
    allergies = models.TextField(
        blank=True,
        verbose_name=_('الحساسية')
    )
    
    chronic_diseases = models.TextField(
        blank=True,
        verbose_name=_('الأمراض المزمنة')
    )
    
    emergency_contact = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('جهة اتصال للطوارئ')
    )
    
    emergency_phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name=_('هاتف الطوارئ')
    )
    
    # حقول تتبع
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('تاريخ الإنشاء')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('تاريخ التحديث')
    )
    
    last_login_ip = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('آخر عنوان IP')
    )
    
    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمين')
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def get_role(self):
        return self.get_role_display()

    @property
    def is_doctor(self):
        return self.role == self.Roles.DOCTOR

    @property
    def is_nurse(self):
        return self.role == self.Roles.NURSE

    @property
    def is_pharmacist(self):
        return self.role == self.Roles.PHARMACIST

    @property
    def is_lab_technician(self):
        return self.role == self.Roles.LAB_TECHNICIAN

    @property
    def is_receptionist(self):
        return self.role == self.Roles.RECEPTIONIST

    @property
    def is_patient(self):
        return self.role == self.Roles.PATIENT

    @property
    def is_medical_staff(self):
        """التحقق مما إذا كان المستخدم من الطاقم الطبي"""
        return self.role in [self.Roles.DOCTOR, self.Roles.NURSE]
    
    @property
    def is_support_staff(self):
        """التحقق مما إذا كان المستخدم من الطاقم المساند"""
        return self.role in [self.Roles.PHARMACIST, self.Roles.LAB_TECHNICIAN]
    
    def get_role_permissions(self):
        """الحصول على صلاحيات الدور"""
        role_permissions = {
            self.Roles.ADMIN: ['all'],
            self.Roles.DOCTOR: [
                'view_patient',
                'add_prescription',
                'view_medical_record',
                'add_medical_record',
                'view_appointment',
                'add_appointment',
            ],
            self.Roles.NURSE: [
                'view_patient',
                'view_medical_record',
                'add_vital_signs',
                'view_appointment',
            ],
            self.Roles.PHARMACIST: [
                'view_prescription',
                'add_medicine',
                'view_inventory',
            ],
            self.Roles.LAB_TECHNICIAN: [
                'view_lab_request',
                'add_lab_result',
                'view_medical_record',
            ],
            self.Roles.RECEPTIONIST: [
                'view_appointment',
                'add_appointment',
                'view_patient',
            ],
            self.Roles.PATIENT: [
                'view_own_medical_record',
                'view_own_prescription',
                'view_own_appointment',
                'add_appointment_request',
            ]
        }
        return role_permissions.get(self.role, [])
