"""
URLs for the accounts app
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .api.barcode import BarcodeScannerView, RegenerateIDCardView

app_name = "accounts"

urlpatterns = [
    # المصادقة الأساسية
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    path(
        "profile/medical-info/", views.update_medical_info, name="update_medical_info"
    ),
    # المصادقة الثنائية
    path("2fa/enable/", views.enable_2fa, name="enable_2fa"),
    path("2fa/verify/", views.verify_2fa, name="2fa_verify"),
    # التحقق من البريد الإلكتروني
    path("email/verify/", views.verify_email, name="verify_email"),
    path(
        "email/verify/confirm/", views.verify_email_confirm, name="verify_email_confirm"
    ),
    # إعدادات الأمان
    path("security/", views.security_settings, name="security_settings"),
    # إعادة تعيين كلمة المرور
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url="/accounts/password_reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/accounts/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # تغيير كلمة المرور
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            success_url="/accounts/password_change/done/",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # مسارات الباركود
    path("barcode/scan/", views.barcode_scanner, name="barcode_scanner"),
    path("api/barcode/scan/", BarcodeScannerView.as_view(), name="barcode_scan"),
    path("id-card/<int:user_id>/", views.download_id_card, name="download_id_card"),
    path(
        "api/id-card/regenerate/",
        RegenerateIDCardView.as_view(),
        name="regenerate_id_card",
    ),
]
