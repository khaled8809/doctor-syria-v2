"""
وحدة المصادقة متعددة العوامل
Multi-Factor Authentication Module

This module handles 2FA functionality including:
- TOTP (Time-based One-Time Password)
- SMS verification
- Email verification
- Backup codes
"""

import base64
import logging
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple

import pyotp
import qrcode
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string

User = get_user_model()
logger = logging.getLogger("auth.mfa")


class MFAManager:
    """
    إدارة المصادقة متعددة العوامل
    Multi-Factor Authentication Manager
    """

    def __init__(self, user: Any):
        self.user = user
        self.totp = pyotp.TOTP(self._get_or_create_secret())

    def _get_or_create_secret(self) -> str:
        """
        الحصول على أو إنشاء سر TOTP
        Get or create TOTP secret
        """
        if not hasattr(self.user, "mfa_secret"):
            self.user.mfa_secret = pyotp.random_base32()
            self.user.save()
        return self.user.mfa_secret

    def generate_qr_code(self) -> str:
        """
        إنشاء رمز QR للتطبيق
        Generate QR code for authenticator app

        Returns:
            str: Base64 encoded QR code image
        """
        provisioning_uri = self.totp.provisioning_uri(
            self.user.email, issuer_name="Doctor Syria"
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")

        return base64.b64encode(buffer.getvalue()).decode()

    def verify_totp(self, code: str) -> bool:
        """
        التحقق من رمز TOTP
        Verify TOTP code

        Args:
            code: الرمز | The code to verify

        Returns:
            bool: True if code is valid
        """
        try:
            return self.totp.verify(code)
        except Exception as e:
            logger.error(f"TOTP verification error for user {self.user.email}: {e}")
            return False

    def generate_backup_codes(self, count: int = 8) -> List[str]:
        """
        إنشاء رموز احتياطية
        Generate backup codes

        Args:
            count: عدد الرموز | Number of codes to generate

        Returns:
            List[str]: List of backup codes
        """
        codes = [get_random_string(16) for _ in range(count)]
        self.user.backup_codes = codes
        self.user.save()
        return codes

    def verify_backup_code(self, code: str) -> bool:
        """
        التحقق من رمز احتياطي
        Verify backup code

        Args:
            code: الرمز | The code to verify

        Returns:
            bool: True if code is valid
        """
        if not hasattr(self.user, "backup_codes"):
            return False

        if code in self.user.backup_codes:
            # Remove used code
            self.user.backup_codes.remove(code)
            self.user.save()
            return True
        return False

    def send_sms_code(self) -> bool:
        """
        إرسال رمز عبر SMS
        Send verification code via SMS

        Returns:
            bool: True if SMS was sent successfully
        """
        if not self.user.phone_number:
            return False

        code = get_random_string(6, allowed_chars="0123456789")
        cache_key = f"sms_code_{self.user.id}"
        cache.set(cache_key, code, 300)  # 5 minutes expiry

        try:
            # Use your SMS service here
            # For example, using Twilio:
            from twilio.rest import Client

            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            client.messages.create(
                body=f"Your Doctor Syria verification code is: {code}",
                from_=settings.TWILIO_PHONE_NUMBER,
                to=self.user.phone_number,
            )
            return True
        except Exception as e:
            logger.error(f"SMS sending error for user {self.user.email}: {e}")
            return False

    def verify_sms_code(self, code: str) -> bool:
        """
        التحقق من رمز SMS
        Verify SMS code

        Args:
            code: الرمز | The code to verify

        Returns:
            bool: True if code is valid
        """
        cache_key = f"sms_code_{self.user.id}"
        stored_code = cache.get(cache_key)

        if stored_code and stored_code == code:
            cache.delete(cache_key)
            return True
        return False

    def send_email_code(self) -> bool:
        """
        إرسال رمز عبر البريد الإلكتروني
        Send verification code via email

        Returns:
            bool: True if email was sent successfully
        """
        code = get_random_string(6, allowed_chars="0123456789")
        cache_key = f"email_code_{self.user.id}"
        cache.set(cache_key, code, 300)  # 5 minutes expiry

        try:
            context = {"user": self.user, "code": code, "site_name": "Doctor Syria"}

            html_message = render_to_string("auth/mfa_email.html", context)

            send_mail(
                subject="Your Verification Code",
                message=f"Your Doctor Syria verification code is: {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                html_message=html_message,
            )
            return True
        except Exception as e:
            logger.error(f"Email sending error for user {self.user.email}: {e}")
            return False

    def verify_email_code(self, code: str) -> bool:
        """
        التحقق من رمز البريد الإلكتروني
        Verify email code

        Args:
            code: الرمز | The code to verify

        Returns:
            bool: True if code is valid
        """
        cache_key = f"email_code_{self.user.id}"
        stored_code = cache.get(cache_key)

        if stored_code and stored_code == code:
            cache.delete(cache_key)
            return True
        return False

    def get_preferred_method(self) -> str:
        """
        الحصول على طريقة التحقق المفضلة
        Get user's preferred 2FA method

        Returns:
            str: Preferred method (totp, sms, or email)
        """
        return getattr(self.user, "mfa_method", "totp")

    def set_preferred_method(self, method: str) -> bool:
        """
        تعيين طريقة التحقق المفضلة
        Set user's preferred 2FA method

        Args:
            method: الطريقة | The method to set

        Returns:
            bool: True if method was set successfully
        """
        if method not in ["totp", "sms", "email"]:
            return False

        self.user.mfa_method = method
        self.user.save()
        return True
