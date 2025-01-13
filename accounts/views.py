"""
Views for the accounts app
"""

import logging

import pyotp
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_http_methods

from .forms import (
    EmailVerificationForm,
    LoginForm,
    MedicalInformationForm,
    ProfileUpdateForm,
    TwoFactorSetupForm,
    TwoFactorVerifyForm,
)
from .models import MedicalInformation, User

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """عرض تسجيل الدخول"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.get(username=username)

                # التحقق من قفل الحساب
                if user.is_locked:
                    messages.error(
                        request,
                        "الحساب مقفل مؤقتاً بسبب محاولات تسجيل دخول متكررة. الرجاء المحاولة بعد 30 دقيقة.",
                    )
                    logger.warning(f"محاولة تسجيل دخول لحساب مقفل: {username}")
                    return render(request, "registration/login.html", {"form": form})

                # التحقق من المصادقة
                if user.check_password(password):
                    # تحديث معلومات الجهاز
                    device_info = {
                        "device_id": request.META.get("HTTP_USER_AGENT", ""),
                        "device_type": "web",
                        "ip_address": request.META.get("REMOTE_ADDR"),
                    }
                    try:
                        user.add_device_info(device_info)
                    except ValidationError as e:
                        logger.error(f"خطأ في تحديث معلومات الجهاز: {str(e)}")

                    if user.two_factor_enabled:
                        # إذا كانت المصادقة الثنائية مفعلة
                        request.session["2fa_user_id"] = user.id
                        return redirect("accounts:2fa_verify")

                    # تسجيل الدخول مباشرة إذا لم تكن المصادقة الثنائية مفعلة
                    login(request, user)
                    user.reset_failed_login()
                    user.update_last_activity()
                    logger.info(f"تم تسجيل دخول المستخدم: {username}")
                    return redirect("accounts:dashboard")
                else:
                    user.increment_failed_login()
                    remaining_attempts = user.get_remaining_login_attempts()
                    if remaining_attempts > 0:
                        messages.error(
                            request,
                            f"كلمة المرور غير صحيحة. تبقى لديك {remaining_attempts} محاولات.",
                        )
                    else:
                        messages.error(
                            request,
                            "تم قفل الحساب مؤقتاً بسبب محاولات تسجيل دخول متكررة.",
                        )
                    logger.warning(f"محاولة تسجيل دخول فاشلة: {username}")
            except User.DoesNotExist:
                logger.warning(f"محاولة تسجيل دخول بمستخدم غير موجود: {username}")
                messages.error(request, "اسم المستخدم غير موجود")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def enable_2fa(request):
    """تفعيل المصادقة الثنائية"""
    if request.method == "POST":
        form = TwoFactorSetupForm(request.POST)
        if form.is_valid():
            try:
                # تفعيل المصادقة الثنائية
                secret = pyotp.random_base32()
                totp = pyotp.TOTP(secret)

                # التحقق من عدم وجود مصادقة ثنائية مفعلة مسبقاً
                if request.user.two_factor_enabled:
                    messages.error(request, "المصادقة الثنائية مفعلة بالفعل")
                    return redirect("accounts:security_settings")

                request.user.two_factor_secret = secret
                request.user.two_factor_enabled = True
                request.user.save()

                # إنشاء رابط QR
                provisioning_uri = totp.provisioning_uri(
                    request.user.email, issuer_name="Doctor Syria"
                )

                logger.info(
                    f"تم تفعيل المصادقة الثنائية للمستخدم: {request.user.username}"
                )

                return render(
                    request,
                    "registration/2fa_setup.html",
                    {"qr_uri": provisioning_uri, "secret": secret},
                )

            except ValidationError as e:
                messages.error(request, f"خطأ في حفظ الإعدادات: {str(e)}")
                logger.error(f"خطأ في تفعيل المصادقة الثنائية: {str(e)}")
            except Exception as e:
                messages.error(request, "حدث خطأ غير متوقع. الرجاء المحاولة مرة أخرى.")
                logger.error(f"خطأ غير متوقع في تفعيل المصادقة الثنائية: {str(e)}")
    else:
        form = TwoFactorSetupForm()

    return render(request, "registration/2fa_setup.html", {"form": form})


@require_http_methods(["GET", "POST"])
def verify_2fa(request):
    """التحقق من المصادقة الثنائية"""
    if "2fa_user_id" not in request.session:
        return redirect("accounts:login")

    if request.method == "POST":
        form = TwoFactorVerifyForm(request.POST)
        if form.is_valid():
            try:
                user = get_object_or_404(User, id=request.session["2fa_user_id"])
                token = form.cleaned_data["token"]

                totp = pyotp.TOTP(user.two_factor_secret)
                if totp.verify(token):
                    login(request, user)
                    user.reset_failed_login()
                    user.update_last_activity()
                    del request.session["2fa_user_id"]
                    logger.info(
                        f"تم التحقق من المصادقة الثنائية للمستخدم: {user.username}"
                    )
                    return redirect("accounts:dashboard")
                else:
                    logger.warning(f"رمز تحقق غير صحيح للمستخدم: {user.username}")
                    messages.error(request, "رمز التحقق غير صحيح")
            except Exception as e:
                logger.error(f"خطأ في التحقق من المصادقة الثنائية: {str(e)}")
                messages.error(request, "حدث خطأ أثناء التحقق")
    else:
        form = TwoFactorVerifyForm()

    return render(request, "accounts/2fa_verify.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def verify_email(request):
    """التحقق من البريد الإلكتروني"""
    if request.method == "POST":
        try:
            # إرسال رمز التحقق عبر البريد
            verification_code = get_random_string(length=6, allowed_chars="0123456789")
            request.session["email_verification_code"] = verification_code

            # إرسال البريد
            context = {"user": request.user, "verification_code": verification_code}
            email_html = render_to_string("emails/verify_email.html", context)
            send_mail(
                "تحقق من بريدك الإلكتروني - Doctor Syria",
                "",
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                html_message=email_html,
            )

            logger.info(f"تم إرسال رمز التحقق إلى: {request.user.email}")
            messages.success(request, "تم إرسال رمز التحقق إلى بريدك الإلكتروني")
            return redirect("accounts:verify_email_confirm")
        except Exception as e:
            logger.error(f"خطأ في إرسال رمز التحقق: {str(e)}")
            messages.error(request, "حدث خطأ أثناء إرسال رمز التحقق")

    return render(request, "accounts/verify_email.html")


@login_required
@require_http_methods(["GET", "POST"])
def verify_email_confirm(request):
    """تأكيد التحقق من البريد الإلكتروني"""
    if request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            try:
                code = form.cleaned_data["code"]
                stored_code = request.session.get("email_verification_code")

                if code == stored_code:
                    request.user.email_verified = True
                    request.user.save()
                    del request.session["email_verification_code"]
                    logger.info(f"تم التحقق من البريد الإلكتروني: {request.user.email}")
                    messages.success(request, "تم التحقق من بريدك الإلكتروني بنجاح")
                    return redirect("accounts:profile")
                else:
                    logger.warning(f"رمز تحقق بريد غير صحيح: {request.user.email}")
                    messages.error(request, "رمز التحقق غير صحيح")
            except Exception as e:
                logger.error(f"خطأ في تأكيد التحقق من البريد: {str(e)}")
                messages.error(request, "حدث خطأ أثناء التحقق من البريد")
    else:
        form = EmailVerificationForm()

    return render(request, "accounts/verify_email_confirm.html", {"form": form})


@login_required
def dashboard(request):
    """لوحة التحكم"""
    try:
        context = {
            "today_appointments_count": 0,  # يمكن تنفيذ هذا حسب احتياجات المشروع
            "new_prescriptions_count": 0,
            "active_patients_count": User.objects.filter(
                role="patient", is_active=True
            ).count(),
            "doctors_count": User.objects.filter(role="doctor", is_active=True).count(),
            "upcoming_appointments": [],
            "notifications": [],
            "recent_activities": request.user.get_recent_activities(),
        }
        logger.info(f"تم عرض لوحة التحكم للمستخدم: {request.user.username}")
        return render(request, "dashboard/index.html", context)
    except Exception as e:
        logger.error(f"خطأ في عرض لوحة التحكم: {str(e)}")
        messages.error(request, "حدث خطأ أثناء تحميل لوحة التحكم")
        return redirect("accounts:login")


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    """الملف الشخصي"""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                logger.info(f"تم تحديث الملف الشخصي: {request.user.username}")
                messages.success(request, "تم تحديث الملف الشخصي بنجاح")
                return redirect("accounts:profile")
            except Exception as e:
                logger.error(f"خطأ في تحديث الملف الشخصي: {str(e)}")
                messages.error(request, "حدث خطأ أثناء تحديث الملف الشخصي")
    else:
        form = ProfileUpdateForm(instance=request.user)

    # إضافة نموذج المعلومات الطبية إذا كان المستخدم مريضاً
    medical_form = None
    if request.user.role == User.Roles.PATIENT:
        medical_info, created = MedicalInformation.objects.get_or_create(
            user=request.user
        )
        medical_form = MedicalInformationForm(instance=medical_info)

    return render(
        request, "accounts/profile.html", {"form": form, "medical_form": medical_form}
    )


@login_required
@require_http_methods(["POST"])
def update_medical_info(request):
    """تحديث المعلومات الطبية"""
    if request.user.role != User.Roles.PATIENT:
        messages.error(request, "غير مسموح لك بتحديث المعلومات الطبية")
        return redirect("accounts:profile")

    try:
        medical_info, created = MedicalInformation.objects.get_or_create(
            user=request.user
        )
        form = MedicalInformationForm(request.POST, instance=medical_info)

        if form.is_valid():
            form.save()
            logger.info(f"تم تحديث المعلومات الطبية للمستخدم: {request.user.username}")
            messages.success(request, "تم تحديث المعلومات الطبية بنجاح")
        else:
            logger.warning(
                f"خطأ في تحديث المعلومات الطبية للمستخدم: {request.user.username}"
            )
            messages.error(request, "الرجاء تصحيح الأخطاء أدناه")
            return render(
                request,
                "accounts/profile.html",
                {
                    "form": ProfileUpdateForm(instance=request.user),
                    "medical_form": form,
                },
            )
    except Exception as e:
        logger.error(f"خطأ في تحديث المعلومات الطبية: {str(e)}")
        messages.error(request, "حدث خطأ أثناء تحديث المعلومات الطبية")

    return redirect("accounts:profile")


@login_required
def security_settings(request):
    """إعدادات الأمان"""
    try:
        context = {
            "devices": request.user.device_info,
            "last_login": request.user.last_login,
            "last_password_change": request.user.last_password_change,
            "two_factor_enabled": request.user.two_factor_enabled,
            "email_verified": request.user.email_verified,
        }
        logger.info(f"تم عرض إعدادات الأمان للمستخدم: {request.user.username}")
        return render(request, "accounts/security.html", context)
    except Exception as e:
        logger.error(f"خطأ في عرض إعدادات الأمان: {str(e)}")
        messages.error(request, "حدث خطأ أثناء تحميل إعدادات الأمان")
        return redirect("accounts:profile")


@login_required
def logout_view(request):
    """تسجيل الخروج"""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("accounts:login")


import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .utils.id_card_generator import IDCardGenerator


@login_required
def barcode_scanner(request):
    """عرض صفحة مسح الباركود"""
    return render(request, "barcode/scanner.html")


@login_required
def download_id_card(request, user_id):
    """تحميل البطاقة التعريفية"""
    user = get_object_or_404(User, id=user_id)

    # التحقق من الصلاحيات
    if not request.user.is_staff and request.user != user:
        return HttpResponse("غير مصرح", status=403)

    # توليد البطاقة
    generator = IDCardGenerator()
    card_path = generator.create_card(user)

    # تحميل البطاقة
    file_path = os.path.join(settings.MEDIA_ROOT, card_path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="image/png")
            response[
                "Content-Disposition"
            ] = f"attachment; filename=id_card_{user.id}.png"
            return response

    return HttpResponse("البطاقة غير موجودة", status=404)
