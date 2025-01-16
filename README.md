# Doctor Syria - نظام إدارة العيادات الطبية

نظام متكامل لإدارة العيادات الطبية والمستشفيات، مبني باستخدام Django و Docker.

## المميزات الرئيسية

- ✨ إدارة المواعيد والحجوزات
- 👥 إدارة المرضى والسجلات الطبية
- 💊 إدارة الوصفات الطبية والأدوية
- 📊 التقارير والإحصائيات
- 🏥 إدارة العيادات والمستشفيات
- 💳 نظام الفواتير والمدفوعات
- 📱 واجهة مستخدم سهلة الاستخدام

## المتطلبات الأساسية

- Docker Desktop
- Docker Compose
- Git

## التثبيت والتشغيل

1. استنساخ المشروع:
```bash
git clone https://github.com/yourusername/doctor-syria-v2.git
cd doctor-syria-v2
```

2. إعداد ملف البيئة:
```bash
cp .env.example .env
```
قم بتعديل الإعدادات في ملف `.env` حسب بيئتك.

3. بناء وتشغيل الحاويات:
```bash
docker-compose up -d --build
```

4. تهيئة قاعدة البيانات:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## الوصول إلى التطبيق

- واجهة المستخدم: http://localhost:8000
- لوحة الإدارة: http://localhost:8000/admin

## المساهمة

نرحب بمساهماتكم! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) للمزيد من المعلومات.

## الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE).

## الدعم

إذا واجهتك أي مشكلة أو لديك أي استفسار، يرجى فتح issue جديد في صفحة المشروع على GitHub.
