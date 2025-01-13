"""
اختبارات وحدة تعدد اللغات
Internationalization Tests
"""

from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory

from doctor_syria.i18n import (
    LocaleMiddleware,
    format_date,
    format_number,
    get_language_urls,
    get_translation,
    get_user_language,
)

User = get_user_model()


@pytest.mark.django_db
class TestI18n:
    @pytest.fixture
    def client(self):
        return Client()

    @pytest.fixture
    def factory(self):
        return RequestFactory()

    @pytest.fixture
    def test_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        user.language = "ar"
        user.save()
        return user

    def test_user_language(self, factory, test_user):
        request = factory.get("/")
        request.user = test_user

        # Test authenticated user language
        assert get_user_language(request) == "ar"

        # Test anonymous user language
        request.user.is_authenticated = False
        request.LANGUAGE_CODE = "en"
        assert get_user_language(request) == "en"

    def test_translations(self):
        # Test Arabic translation
        assert get_translation("welcome", "ar") == "مرحباً بك في نظام طبيب سوريا"

        # Test English translation
        assert get_translation("welcome", "en") == "Welcome to Doctor Syria System"

        # Test French translation
        assert (
            get_translation("welcome", "fr") == "Bienvenue sur le système Doctor Syria"
        )

        # Test Turkish translation
        assert get_translation("welcome", "tr") == "Doctor Syria Sistemine Hoş Geldiniz"

        # Test fallback to Arabic for missing translation
        assert get_translation("nonexistent", "en") == get_translation(
            "nonexistent", "ar"
        )

    def test_language_urls(self, factory):
        request = factory.get("/test/")
        urls = get_language_urls(request)

        assert len(urls) == 4  # ar, en, fr, tr
        assert any(url["code"] == "ar" for url in urls)
        assert any(url["code"] == "en" for url in urls)
        assert all("/test/?lang=" in url["url"] for url in urls)

    def test_number_formatting(self):
        number = 12345.67

        # Test Arabic formatting
        arabic = format_number(number, "ar")
        assert "١" in arabic
        assert "٢" in arabic
        assert "٣" in arabic

        # Test other languages
        assert format_number(number, "en") == "12345.67"
        assert format_number(number, "fr") == "12345.67"

    def test_date_formatting(self):
        date = datetime(2025, 1, 8)

        # Test Arabic formatting
        arabic_date = format_date(date, "ar")
        assert "يناير" in arabic_date or "كانون الثاني" in arabic_date
        assert "٢٠٢٥" in arabic_date

        # Test English formatting
        english_date = format_date(date, "en")
        assert "January" in english_date
        assert "2025" in english_date

        # Test French formatting
        french_date = format_date(date, "fr")
        assert "janvier" in french_date
        assert "2025" in french_date

    def test_locale_middleware(self, factory, test_user):
        middleware = LocaleMiddleware(lambda r: r)

        # Test language switching
        request = factory.get("/?lang=en")
        request.user = test_user
        request.session = {}

        middleware(request)
        assert request.session.get("django_language") == "en"
        assert test_user.language == "en"

        # Test invalid language code
        request = factory.get("/?lang=invalid")
        request.user = test_user
        request.session = {}

        middleware(request)
        assert "django_language" not in request.session
