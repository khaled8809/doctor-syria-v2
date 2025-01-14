import os

from celery import Celery

# تعيين متغير بيئة الإعدادات الافتراضي لـ Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doctor_syria.settings")

app = Celery("doctor_syria")

# استخدام ملف الإعدادات الخاص بـ Django لتكوين Celery
app.config_from_object("django.conf:settings", namespace="CELERY")

# تحميل تلقائي للمهام من جميع ملفات tasks.py المسجلة في التطبيقات
app.autodiscover_tasks()
