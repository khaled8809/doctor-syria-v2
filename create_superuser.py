import os
import django
from django.contrib.auth import get_user_model

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "doctor_syria.settings.base")
    django.setup()

    User = get_user_model()

    # إنشاء مستخدم مدير إذا لم يكن موجوداً
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123456",
            first_name="مدير",
            last_name="النظام",
        )
        print("تم إنشاء المستخدم المدير بنجاح")
    else:
        print("المستخدم المدير موجود بالفعل")

except Exception as e:
    print(f"حدث خطأ: {e}")
