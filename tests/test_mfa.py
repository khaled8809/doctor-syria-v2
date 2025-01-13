"""
اختبارات وحدة المصادقة متعددة العوامل
Multi-Factor Authentication Tests
"""

import base64
from unittest.mock import MagicMock, patch

import pyotp
import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.test import Client, RequestFactory

from doctor_syria.auth.mfa import MFAManager

User = get_user_model()


@pytest.mark.django_db
class TestMFA:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def factory(self):
        return RequestFactory()

    @pytest.fixture
    def test_user(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            phone_number="+1234567890",
        )
        return user

    @pytest.fixture
    def mfa_manager(self, test_user):
        return MFAManager(test_user)

    def test_totp_setup(self, mfa_manager):
        # Test secret generation
        secret = mfa_manager._get_or_create_secret()
        assert len(secret) == 32
        assert pyotp.TOTP(secret).verify(pyotp.TOTP(secret).now())

        # Test QR code generation
        qr_code = mfa_manager.generate_qr_code()
        assert isinstance(qr_code, str)
        assert base64.b64decode(qr_code)

    def test_backup_codes(self, mfa_manager):
        # Generate backup codes
        codes = mfa_manager.generate_backup_codes()
        assert len(codes) == 8
        assert all(len(code) == 16 for code in codes)

        # Verify and use backup code
        code = codes[0]
        assert mfa_manager.verify_backup_code(code)
        assert not mfa_manager.verify_backup_code(code)  # Code should be used up
        assert len(mfa_manager.user.backup_codes) == 7

    @patch("twilio.rest.Client")
    def test_sms_verification(self, mock_twilio, mfa_manager):
        # Setup mock
        mock_client = MagicMock()
        mock_twilio.return_value = mock_client

        # Test SMS sending
        assert mfa_manager.send_sms_code()
        mock_client.messages.create.assert_called_once()

        # Test code verification
        cache_key = f"sms_code_{mfa_manager.user.id}"
        code = cache.get(cache_key)
        assert mfa_manager.verify_sms_code(code)
        assert not mfa_manager.verify_sms_code(code)  # Code should be used up

    def test_email_verification(self, mfa_manager):
        # Test email sending
        assert mfa_manager.send_email_code()
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [mfa_manager.user.email]

        # Test code verification
        cache_key = f"email_code_{mfa_manager.user.id}"
        code = cache.get(cache_key)
        assert mfa_manager.verify_email_code(code)
        assert not mfa_manager.verify_email_code(code)  # Code should be used up

    def test_preferred_method(self, mfa_manager):
        # Test default method
        assert mfa_manager.get_preferred_method() == "totp"

        # Test setting valid method
        assert mfa_manager.set_preferred_method("sms")
        assert mfa_manager.get_preferred_method() == "sms"

        # Test setting invalid method
        assert not mfa_manager.set_preferred_method("invalid")
        assert mfa_manager.get_preferred_method() == "sms"

    def test_totp_verification(self, mfa_manager):
        # Test valid code
        totp = pyotp.TOTP(mfa_manager._get_or_create_secret())
        code = totp.now()
        assert mfa_manager.verify_totp(code)

        # Test invalid code
        assert not mfa_manager.verify_totp("000000")
        assert not mfa_manager.verify_totp("invalid")
