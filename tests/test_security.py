"""
اختبارات وحدة الأمان
Security Module Tests
"""

import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.test import Client, RequestFactory

from doctor_syria.security import (
    SecurityMiddleware,
    check_rate_limit,
    check_user_permissions,
    decrypt_sensitive_data,
    encrypt_sensitive_data,
    sanitize_input,
)

User = get_user_model()


@pytest.mark.django_db
class TestSecurity:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def factory(self):
        return RequestFactory()

    @pytest.fixture
    def test_user(self):
        return User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )

    def test_user_permissions(self, test_user):
        # Test regular user permissions
        assert not check_user_permissions(test_user, ["auth.add_user"])

        # Test superuser permissions
        test_user.is_superuser = True
        test_user.save()
        assert check_user_permissions(test_user, ["auth.add_user"])

    def test_rate_limit(self, factory):
        request = factory.get("/")
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        # First request should pass
        assert check_rate_limit(request, limit=1)

        # Second request should fail
        assert not check_rate_limit(request, limit=1)

    def test_sanitize_input(self):
        dirty_data = {
            "text": '<script>alert("xss")</script><p>Hello</p>',
            "nested": {
                "text": '<img src="x" onerror="alert(1)">',
            },
            "list": ["<script>alert(2)</script>", "<p>Safe</p>"],
        }

        clean_data = sanitize_input(dirty_data)

        assert "<script>" not in clean_data["text"]
        assert "<p>Hello</p>" in clean_data["text"]
        assert "<img" not in clean_data["nested"]["text"]
        assert "<script>" not in clean_data["list"][0]
        assert "<p>Safe</p>" in clean_data["list"][1]

    def test_encryption(self):
        sensitive_data = "sensitive information"
        encrypted = encrypt_sensitive_data(sensitive_data)
        decrypted = decrypt_sensitive_data(encrypted)

        assert encrypted != sensitive_data
        assert decrypted == sensitive_data

    def test_security_middleware(self, factory):
        middleware = SecurityMiddleware(lambda r: r)
        request = factory.post("/", {"data": '<script>alert("xss")</script>'})
        request.META["REMOTE_ADDR"] = "127.0.0.1"

        # Test rate limiting
        for _ in range(100):
            middleware(request)

        with pytest.raises(PermissionDenied):
            middleware(request)

        # Test input sanitization
        request = factory.post("/", {"data": '<script>alert("xss")</script>'})
        request.META["REMOTE_ADDR"] = "127.0.0.2"
        response = middleware(request)

        assert "<script>" not in str(request.POST)
