from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor_syria.settings.development')
django.setup()

User = get_user_model()

# إنشاء مستخدم مدير إذا لم يكن موجوداً
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='admin123456',
        first_name='مدير',
        last_name='النظام',
        role='admin'
    )
    print('تم إنشاء المستخدم المدير بنجاح')
else:
    print('المستخدم المدير موجود بالفعل')
