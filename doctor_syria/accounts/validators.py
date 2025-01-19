import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    """
    التحقق من صحة رقم الهاتف السوري
    يجب أن يبدأ بـ +963 أو 00963 أو 0
    """
    phone_regex = re.compile(r"^(\+963|00963|0)?9\d{8}$")
    if not phone_regex.match(value):
        raise ValidationError(
            _("%(value)s ليس رقم هاتف سوري صحيح"),
            params={"value": value},
        )


def validate_syrian_id(value):
    """
    التحقق من صحة رقم الهوية السورية
    يجب أن يكون 11 رقم
    """
    if not re.match(r"^\d{11}$", value):
        raise ValidationError(
            _("رقم الهوية يجب أن يتكون من 11 رقم"),
        )


def validate_medical_license(value):
    """
    التحقق من صحة رقم الترخيص الطبي
    """
    if not re.match(r"^\d{5,10}$", value):
        raise ValidationError(
            _("رقم الترخيص الطبي غير صحيح"),
        )


def validate_password_strength(value):
    """
    التحقق من قوة كلمة المرور
    - على الأقل 8 أحرف
    - تحتوي على حرف كبير وحرف صغير
    - تحتوي على رقم
    - تحتوي على رمز خاص
    """
    if len(value) < 8:
        raise ValidationError(_("كلمة المرور يجب أن تكون 8 أحرف على الأقل"))
    if not re.search(r"[A-Z]", value):
        raise ValidationError(_("كلمة المرور يجب أن تحتوي على حرف كبير"))
    if not re.search(r"[a-z]", value):
        raise ValidationError(_("كلمة المرور يجب أن تحتوي على حرف صغير"))
    if not re.search(r"\d", value):
        raise ValidationError(_("كلمة المرور يجب أن تحتوي على رقم"))
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
        raise ValidationError(_("كلمة المرور يجب أن تحتوي على رمز خاص"))
