"""Views for the accounts app."""

import logging
import os

import pyotp
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods

from .forms import (
    LoginForm,
    MedicalInformationForm,
    ProfileUpdateForm,
    TwoFactorVerifyForm,
    TwoFactorSetupForm,
    EmailVerificationForm,
)
from .models import MedicalInformation, User
from appointments.models import Appointment
from .services import get_new_prescriptions_count, get_upcoming_appointments, get_user_notifications
from .utils.id_card_generator import IDCardGenerator

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login process."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                logger.info(f"User logged in: {username}")
                return redirect("accounts:dashboard")
            else:
                logger.warning(f"Failed login attempt: {username}")
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def enable_2fa(request):
    """Enable two-factor authentication process."""
    if request.method == "POST":
        form = TwoFactorSetupForm(request.POST)
        if form.is_valid():
            try:
                secret = pyotp.random_base32()
                request.user.two_factor_secret = secret
                request.user.two_factor_enabled = True
                request.user.save()

                logger.info(f"2FA enabled for user: {request.user.username}")
                messages.success(request, "Two-factor authentication enabled successfully.")
                return redirect("accounts:security_settings")
            except ValidationError as e:
                logger.error(f"Error enabling 2FA: {str(e)}")
                messages.error(request, str(e))
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TwoFactorSetupForm()

    return render(request, "registration/2fa_setup.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def verify_2fa(request):
    """Verify two-factor authentication code process."""
    if request.method == "POST":
        form = TwoFactorVerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            totp = pyotp.TOTP(request.user.two_factor_secret)

            if totp.verify(code):
                login(request, request.user)
                logger.info(f"2FA verification successful: {request.user.username}")
                return redirect("accounts:dashboard")
            else:
                logger.warning(f"Invalid 2FA code: {request.user.username}")
                messages.error(request, "Invalid verification code.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TwoFactorVerifyForm()

    return render(request, "accounts/2fa_verify.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def verify_email(request):
    """Send email verification code process."""
    if request.method == "POST":
        try:
            verification_code = get_random_string(32)
            request.user.email_verification_code = verification_code
            request.user.save()

            context = {
                "user": request.user,
                "verification_code": verification_code,
            }
            email_body = render_to_string("accounts/email/verify_email.html", context)
            send_mail(
                "Verify your email",
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                html_message=email_body,
            )

            logger.info(f"Verification email sent to: {request.user.email}")
            messages.success(request, "Verification email sent.")
            return redirect("accounts:verify_email_confirm")
        except Exception as e:
            logger.error(f"Error sending verification email: {str(e)}")
            messages.error(request, "Error sending verification email.")

    return render(request, "accounts/verify_email.html")


@login_required
@require_http_methods(["GET", "POST"])
def verify_email_confirm(request):
    """Confirm email verification code process."""
    if request.method == "POST":
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            if code == request.user.email_verification_code:
                request.user.email_verified = True
                request.user.save()
                logger.info(f"Email verified for user: {request.user.username}")
                messages.success(request, "Email verified successfully.")
                return redirect("accounts:profile")
            else:
                logger.warning(f"Invalid verification code: {request.user.username}")
                messages.error(request, "Invalid verification code.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = EmailVerificationForm()

    return render(request, "accounts/verify_email_confirm.html", {"form": form})


@login_required
@cache_page(60 * 15)  # Cache for 15 minutes
def dashboard(request):
    """Display the dashboard for the current user process."""
    try:
        # Optimize queries using select_related and prefetch_related
        active_patients = (
            User.objects.filter(role="patient", is_active=True)
            .select_related("patient_profile")
            .count()
        )

        active_doctors = (
            User.objects.filter(role="doctor", is_active=True)
            .select_related("doctor_profile")
            .count()
        )

        # Get today's appointments efficiently
        today = timezone.now().date()
        today_appointments = (
            Appointment.objects.filter(appointment_date__date=today)
            .select_related("doctor", "patient")
            .count()
        )

        # Get recent activities with optimized queries
        recent_activities = (
            request.user.get_recent_activities()
            .select_related("user")
            .prefetch_related("content_type")
        )

        context = {
            "today_appointments_count": today_appointments,
            "new_prescriptions_count": cache.get_or_set(
                f"new_prescriptions_{request.user.id}",
                lambda: get_new_prescriptions_count(request.user),
                timeout=60 * 15,
            ),
            "active_patients_count": active_patients,
            "doctors_count": active_doctors,
            "upcoming_appointments": get_upcoming_appointments(request.user),
            "notifications": get_user_notifications(request.user),
            "recent_activities": recent_activities[:10],
        }

        logger.info(f"Dashboard viewed by user: {request.user.username}")
        return render(request, "dashboard/index.html", context)

    except Exception as e:
        logger.error(f"Error displaying dashboard: {str(e)}", exc_info=True)
        messages.error(request, "Error loading dashboard.")
        return redirect("accounts:login")


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    """Update user profile process."""
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            try:
                form.save()
                logger.info(f"Profile updated: {request.user.username}")
                messages.success(request, "Profile updated successfully.")
                return redirect("accounts:profile")
            except Exception as e:
                logger.error(f"Error updating profile: {str(e)}")
                messages.error(request, "Error updating profile.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    medical_form = None
    if request.user.role == User.Roles.PATIENT:
        medical_info, created = MedicalInformation.objects.get_or_create(user=request.user)
        medical_form = MedicalInformationForm(instance=medical_info)

    return render(request, "accounts/profile.html", {"form": form, "medical_form": medical_form})


@login_required
@require_http_methods(["POST"])
def update_medical_info(request):
    """Update user medical information process."""
    if request.user.role != User.Roles.PATIENT:
        messages.error(request, "Not authorized to update medical information.")
        return redirect("accounts:profile")

    try:
        medical_info, created = MedicalInformation.objects.get_or_create(user=request.user)
        form = MedicalInformationForm(request.POST, instance=medical_info)

        if form.is_valid():
            form.save()
            logger.info(f"Medical info updated: {request.user.username}")
            messages.success(request, "Medical information updated successfully.")
        else:
            logger.warning(f"Invalid medical info update: {request.user.username}")
            messages.error(request, "Please correct the errors below.")
            return render(
                request,
                "accounts/profile.html",
                {
                    "form": ProfileUpdateForm(instance=request.user),
                    "medical_form": form,
                },
            )
    except Exception as e:
        logger.error(f"Error updating medical info: {str(e)}")
        messages.error(request, "Error updating medical information.")

    return redirect("accounts:profile")


@login_required
def security_settings(request):
    """Display security settings process."""
    try:
        context = {
            "devices": request.user.device_info,
            "last_login": request.user.last_login,
            "last_password_change": request.user.last_password_change,
            "two_factor_enabled": request.user.two_factor_enabled,
            "email_verified": request.user.email_verified,
        }
        logger.info(f"Security settings viewed: {request.user.username}")
        return render(request, "accounts/security.html", context)
    except Exception as e:
        logger.error(f"Error displaying security settings: {str(e)}")
        messages.error(request, "Error loading security settings.")
        return redirect("accounts:profile")


@login_required
def logout_view(request):
    """Log out the current user process."""
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("accounts:login")


@login_required
def barcode_scanner(request):
    """Display barcode scanner page process."""
    return render(request, "barcode/scanner.html")


@login_required
def download_id_card(request, user_id):
    """Download user ID card process."""
    user = get_object_or_404(User, id=user_id)

    if not request.user.is_staff and request.user != user:
        return HttpResponse("Unauthorized", status=403)

    generator = IDCardGenerator()
    card_path = generator.create_card(user)

    file_path = os.path.join(settings.MEDIA_ROOT, card_path)
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="image/png")
            response["Content-Disposition"] = f"attachment; filename=id_card_{user.id}.png"
            return response

    return HttpResponse("Card not found", status=404)
