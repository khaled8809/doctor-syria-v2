# Doctor Syria - نظام إدارة المستشفيات والعيادات الطبية

<div dir="rtl">

## نظرة عامة

Doctor Syria هو نظام متكامل لإدارة المستشفيات والعيادات الطبية في سوريا. يوفر النظام مجموعة شاملة من الأدوات لإدارة جميع جوانب المؤسسات الطبية.

## الميزات الرئيسية

- ✨ إدارة المرضى والمواعيد
- 🏥 إدارة المستشفيات والعيادات
- 👨‍⚕️ إدارة الأطباء والموظفين
- 💊 نظام الصيدلية والمخزون الطبي
- 📊 التقارير والإحصائيات
- 💳 نظام الفوترة والمحاسبة
- 🔔 نظام التنبيهات والإشعارات
- 📱 تطبيق موبايل للمرضى والأطباء

## المتطلبات التقنية

- Python 3.13 أو أحدث
- PostgreSQL 13 أو أحدث
- Redis 6 أو أحدث
- Node.js 18 أو أحدث (للواجهة الأمامية)

## التثبيت السريع

```bash
# استنساخ المشروع
git clone https://github.com/khaled8809/doctor-syria-v2.git
cd doctor-syria-v2

# إنشاء البيئة الافتراضية
python -m venv venv
source venv/bin/activate  # على Linux/Mac
# أو
venv\Scripts\activate  # على Windows

# تثبيت المتطلبات
pip install -r requirements.txt

# إعداد قاعدة البيانات
python manage.py migrate

# تشغيل الخادم
python manage.py runserver
```

## الوثائق

- [دليل التثبيت](https://khaled8809.github.io/doctor-syria-v2/installation.html)
- [دليل المستخدم](https://khaled8809.github.io/doctor-syria-v2/user-guide.html)
- [دليل المطور](https://khaled8809.github.io/doctor-syria-v2/developer-guide.html)
- [توثيق API](https://khaled8809.github.io/doctor-syria-v2/api/)

## المساهمة

نرحب بمساهماتكم! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) للحصول على التفاصيل حول عملية التطوير وإرسال التحسينات.

## الترخيص

هذا المشروع مرخص تحت رخصة BSD. انظر ملف [LICENSE](LICENSE) للحصول على التفاصيل.

## الدعم

إذا واجهت أي مشاكل أو لديك أسئلة:
- راجع [الأسئلة الشائعة](https://khaled8809.github.io/doctor-syria-v2/faq.html)
- افتح [issue](https://github.com/khaled8809/doctor-syria-v2/issues)
- تواصل معنا على البريد الإلكتروني: support@doctor-syria.com

</div>
