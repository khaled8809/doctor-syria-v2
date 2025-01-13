import os
import uuid
from datetime import datetime

from django.conf import settings
from django.utils import timezone


def generate_unique_id():
    """
    توليد معرف فريد
    """
    return str(uuid.uuid4())


def get_file_path(instance, filename):
    """
    إنشاء مسار فريد للملفات المرفوعة
    """
    ext = filename.split(".")[-1]
    filename = f"{generate_unique_id()}.{ext}"
    return os.path.join(f"uploads/{instance.__class__.__name__.lower()}", filename)


def format_phone_number(phone):
    """
    تنسيق رقم الهاتف
    """
    if not phone:
        return None
    # إزالة الأحرف غير الرقمية
    phone = "".join(filter(str.isdigit, phone))
    # إضافة رمز البلد إذا لم يكن موجوداً
    if len(phone) == 9:  # رقم سوري بدون رمز البلد
        phone = f"+963{phone}"
    return phone


def calculate_age(birth_date):
    """
    حساب العمر من تاريخ الميلاد
    """
    if not birth_date:
        return None
    today = timezone.now().date()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def format_currency(amount, currency="SYP"):
    """
    تنسيق المبلغ المالي
    """
    if amount is None:
        return None
    return f"{amount:,.2f} {currency}"


def get_client_ip(request):
    """
    الحصول على عنوان IP للمستخدم
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
