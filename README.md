# Doctor Syria Platform

نظام إدارة المستشفيات والعيادات الطبية

## هيكل المشروع

```
doctor-syria-v2/
├── accounts/            # إدارة المستخدمين والصلاحيات
├── analytics/          # تحليلات البيانات
├── api/               # واجهة برمجة التطبيقات
├── appointments/      # إدارة المواعيد
├── billing/          # نظام الفواتير
├── core/             # وظائف أساسية مشتركة
├── doctor_syria/     # إعدادات المشروع الرئيسية
├── hospitals/        # إدارة المستشفيات
├── medical_records/  # السجلات الطبية
├── monitoring/       # مراقبة النظام
├── security/         # أمان النظام
└── templates/        # قوالب النظام
```

## المتطلبات

- Python 3.9+
- PostgreSQL 13+
- Redis 6+

## التثبيت

1. إنشاء بيئة Python افتراضية:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

3. نسخ ملف `.env.example` إلى `.env` وتعديل الإعدادات:
```bash
cp .env.example .env
```

4. تهيئة قاعدة البيانات:
```bash
python manage.py migrate
```

5. إنشاء مستخدم مدير:
```bash
python manage.py createsuperuser
```

## التشغيل

1. تشغيل الخادم المحلي:
```bash
python manage.py runserver
```

2. تشغيل خادم Redis:
```bash
redis-server
```

3. تشغيل Celery (إذا كان مطلوباً):
```bash
celery -A doctor_syria worker -l info
```

## الأمان

- تم تفعيل HTTPS
- المصادقة الثنائية مفعلة
- تم تفعيل CSRF protection
- تم تفعيل rate limiting
- تم تفعيل HSTS

## المساهمة

يرجى قراءة [CONTRIBUTING.md](CONTRIBUTING.md) للحصول على تفاصيل حول عملية المساهمة في المشروع.

## الترخيص

هذا المشروع مرخص تحت [رخصة MIT](LICENSE).
