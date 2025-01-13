"""
نماذج تطبيق الحسابات
"""

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .models import MedicalInformation, User


class LoginForm(forms.Form):
    """نموذج تسجيل الدخول"""

    username = forms.CharField(
        label=_("اسم المستخدم"),
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label=_("كلمة المرور"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class TwoFactorSetupForm(forms.Form):
    """نموذج إعداد المصادقة الثنائية"""

    pass  # لا نحتاج إلى حقول في هذا النموذج


class TwoFactorVerifyForm(forms.Form):
    """نموذج التحقق من المصادقة الثنائية"""

    token = forms.CharField(
        label=_("رمز التحقق"),
        max_length=6,
        validators=[
            RegexValidator(r"^\d{6}$", _("يجب أن يتكون رمز التحقق من 6 أرقام"))
        ],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("أدخل رمز التحقق المكون من 6 أرقام"),
            }
        ),
    )


class EmailVerificationForm(forms.Form):
    """نموذج التحقق من البريد الإلكتروني"""

    code = forms.CharField(
        label=_("رمز التحقق"),
        max_length=6,
        validators=[
            RegexValidator(r"^\d{6}$", _("يجب أن يتكون رمز التحقق من 6 أرقام"))
        ],
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("أدخل رمز التحقق المكون من 6 أرقام"),
            }
        ),
    )


class ProfileUpdateForm(forms.ModelForm):
    """نموذج تحديث الملف الشخصي"""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address",
            "birth_date",
            "profile_picture",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "birth_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "profile_picture": forms.FileInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        """التحقق من البريد الإلكتروني"""
        email = self.cleaned_data.get("email")
        if (
            email
            and User.objects.filter(email=email).exclude(id=self.instance.id).exists()
        ):
            raise forms.ValidationError(_("هذا البريد الإلكتروني مستخدم بالفعل"))
        return email

    def clean_phone(self):
        """التحقق من رقم الهاتف"""
        phone = self.cleaned_data.get("phone")
        if (
            phone
            and User.objects.filter(phone=phone).exclude(id=self.instance.id).exists()
        ):
            raise forms.ValidationError(_("هذا الرقم مستخدم بالفعل"))
        return phone


class MedicalInformationForm(forms.ModelForm):
    """نموذج المعلومات الطبية"""

    class Meta:
        model = MedicalInformation
        fields = [
            "blood_type",
            "allergies",
            "chronic_diseases",
            "emergency_contact",
            "emergency_phone",
        ]
        widgets = {
            "blood_type": forms.Select(attrs={"class": "form-control"}),
            "allergies": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "chronic_diseases": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "emergency_contact": forms.TextInput(attrs={"class": "form-control"}),
            "emergency_phone": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_emergency_phone(self):
        """التحقق من رقم هاتف الطوارئ"""
        phone = self.cleaned_data.get("emergency_phone")
        if phone and phone == self.instance.user.phone:
            raise forms.ValidationError(
                _("لا يمكن استخدام رقم هاتفك الشخصي كرقم للطوارئ")
            )
        return phone
