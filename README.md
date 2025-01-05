# Doctor Syria Platform v2

## نظام إدارة المستشفيات والرعاية الصحية المتكامل

نظام شامل لإدارة المستشفيات والرعاية الصحية في سوريا، يربط بين المرضى والأطباء والصيدليات والمختبرات وشركات الأدوية.

### المميزات الرئيسية

- 👥 **إدارة المستخدمين**
  - المرضى
  - الأطباء
  - الصيدليات
  - المختبرات
  - شركات الأدوية
  - الممرضين
  - الموظفين

- 🏥 **إدارة المستشفيات**
  - إدارة الأقسام
  - إدارة الغرف والأسرّة
  - جدولة المواعيد
  - إدارة الطوارئ

- 🤖 **الذكاء الاصطناعي**
  - التشخيص الطبي
  - تحليل الصور الطبية
  - التحقق من تفاعلات الأدوية

- 📋 **السجلات والمتابعة**
  - السجلات الطبية الإلكترونية
  - إدارة الوصفات الطبية
  - التحاليل المخبرية
  - الأشعة

- 💊 **الصيدلية والمختبر**
  - إدارة المخزون
  - طلب الأدوية
  - إدارة التحاليل المخبرية

### التقنيات المستخدمة

- 🐍 **Backend**: Django + Django REST Framework
- 💾 **Database**: PostgreSQL
- 🔄 **Cache**: Redis
- 📋 **Task Queue**: Celery
- 🔌 **Real-time**: Django Channels
- 🔒 **Authentication**: JWT
- 💳 **Payment**: Stripe

### المتطلبات

- Python 3.8+
- PostgreSQL
- Redis
- Node.js (للتطوير الأمامي)

### التثبيت

1. استنساخ المستودع:
```bash
git clone https://github.com/yourusername/doctor-syria-v2.git
cd doctor-syria-v2
```

2. إنشاء وتفعيل البيئة الافتراضية:
```bash
python -m venv venv
source venv/bin/activate  # على Windows: venv\Scripts\activate
```

3. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

4. إعداد ملف البيئة:
- قم بنسخ ملف `.env.example` إلى `.env`
- قم بتعديل المتغيرات حسب إعداداتك

5. تهيئة قاعدة البيانات:
```bash
python manage.py migrate
```

6. تشغيل الخادم:
```bash
python manage.py runserver
```

### المساهمة

نرحب بمساهماتكم! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) للمزيد من المعلومات.

### الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE).
