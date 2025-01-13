"""
إعدادات تعدد اللغات
Internationalization Settings

This module contains settings and utilities for multilingual support.
"""

import logging
from typing import Any, Dict, List

from django.conf import settings
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# تكوين التسجيل | Configure logging
logger = logging.getLogger("i18n")

# اللغات المدعومة | Supported languages
LANGUAGES = [
    ("ar", _("العربية")),
    ("en", _("English")),
    ("fr", _("Français")),
    ("tr", _("Türkçe")),
]

# إعدادات الترجمة | Translation settings
LOCALE_PATHS = [
    settings.BASE_DIR / "locale",
]

LANGUAGE_CODE = "ar"
USE_I18N = True
USE_L10N = True

# قواميس الترجمة | Translation dictionaries
COMMON_TRANSLATIONS = {
    "ar": {
        "welcome": "مرحباً بك في نظام طبيب سوريا",
        "login": "تسجيل الدخول",
        "register": "تسجيل حساب جديد",
        "appointments": "المواعيد",
        "medical_records": "السجلات الطبية",
        "prescriptions": "الوصفات الطبية",
        "doctors": "الأطباء",
        "patients": "المرضى",
        "profile": "الملف الشخصي",
        "settings": "الإعدادات",
        "logout": "تسجيل الخروج",
    },
    "en": {
        "welcome": "Welcome to Doctor Syria System",
        "login": "Login",
        "register": "Register",
        "appointments": "Appointments",
        "medical_records": "Medical Records",
        "prescriptions": "Prescriptions",
        "doctors": "Doctors",
        "patients": "Patients",
        "profile": "Profile",
        "settings": "Settings",
        "logout": "Logout",
    },
    "fr": {
        "welcome": "Bienvenue sur le système Doctor Syria",
        "login": "Connexion",
        "register": "S'inscrire",
        "appointments": "Rendez-vous",
        "medical_records": "Dossiers médicaux",
        "prescriptions": "Ordonnances",
        "doctors": "Médecins",
        "patients": "Patients",
        "profile": "Profil",
        "settings": "Paramètres",
        "logout": "Déconnexion",
    },
    "tr": {
        "welcome": "Doctor Syria Sistemine Hoş Geldiniz",
        "login": "Giriş",
        "register": "Kayıt Ol",
        "appointments": "Randevular",
        "medical_records": "Tıbbi Kayıtlar",
        "prescriptions": "Reçeteler",
        "doctors": "Doktorlar",
        "patients": "Hastalar",
        "profile": "Profil",
        "settings": "Ayarlar",
        "logout": "Çıkış",
    },
}


def get_user_language(request: HttpRequest) -> str:
    """
    الحصول على لغة المستخدم
    Get user's preferred language

    Args:
        request: طلب HTTP | HTTP request

    Returns:
        str: Language code
    """
    if request.user.is_authenticated and hasattr(request.user, "language"):
        return request.user.language

    return request.LANGUAGE_CODE


def get_translation(key: str, language: str) -> str:
    """
    الحصول على الترجمة
    Get translation for a key

    Args:
        key: مفتاح الترجمة | Translation key
        language: رمز اللغة | Language code

    Returns:
        str: Translated text
    """
    try:
        return COMMON_TRANSLATIONS[language][key]
    except KeyError:
        logger.warning(f"Translation missing for key {key} in language {language}")
        return COMMON_TRANSLATIONS["ar"][key]  # Default to Arabic


def get_language_urls(request: HttpRequest) -> List[Dict[str, str]]:
    """
    الحصول على روابط تغيير اللغة
    Get language switcher URLs

    Args:
        request: طلب HTTP | HTTP request

    Returns:
        List[Dict]: List of language URLs
    """
    current_path = request.path
    urls = []

    for code, name in LANGUAGES:
        urls.append({"code": code, "name": name, "url": f"{current_path}?lang={code}"})

    return urls


class LocaleMiddleware:
    """
    وسيط اللغة
    Locale middleware for language processing
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Any:
        # تحديد لغة المستخدم | Set user language
        language = request.GET.get("lang")
        if language and language in dict(LANGUAGES):
            request.session["django_language"] = language
            if request.user.is_authenticated:
                request.user.language = language
                request.user.save()

        response = self.get_response(request)
        return response


def format_number(number: float, language: str) -> str:
    """
    تنسيق الأرقام حسب اللغة
    Format number according to language

    Args:
        number: الرقم | Number to format
        language: رمز اللغة | Language code

    Returns:
        str: Formatted number
    """
    if language == "ar":
        # تحويل الأرقام إلى العربية | Convert to Arabic numerals
        arabic_numerals = {
            "0": "٠",
            "1": "١",
            "2": "٢",
            "3": "٣",
            "4": "٤",
            "5": "٥",
            "6": "٦",
            "7": "٧",
            "8": "٨",
            "9": "٩",
        }
        return "".join(arabic_numerals.get(d, d) for d in str(number))

    return str(number)


def format_date(date: Any, language: str) -> str:
    """
    تنسيق التاريخ حسب اللغة
    Format date according to language

    Args:
        date: التاريخ | Date to format
        language: رمز اللغة | Language code

    Returns:
        str: Formatted date
    """
    from babel.dates import format_date as babel_format_date

    locale_map = {"ar": "ar_SY", "en": "en_US", "fr": "fr_FR", "tr": "tr_TR"}

    return babel_format_date(
        date, format="long", locale=locale_map.get(language, "ar_SY")
    )
