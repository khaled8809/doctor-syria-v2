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

## النشر

### المتطلبات
- Docker و Docker Compose
- Nginx
- Let's Encrypt Certbot
- Prometheus و Grafana للمراقبة

### خطوات النشر السريع
1. نسخ `.env.example` إلى `.env.production` وتحديث القيم
2. تشغيل سكريبت الإعداد:
   ```bash
   ./scripts/setup_production.sh
   ```
3. بدء الخدمات:
   ```bash
   docker-compose up -d
   ```

### المراقبة
- Grafana: https://monitor.doctor-syria.com
- Prometheus: https://metrics.doctor-syria.com
- التنبيهات عبر Slack في قناة #monitoring

### النسخ الاحتياطي
- يتم إجراء نسخ احتياطي تلقائي يومياً في الساعة 3 صباحاً
- موقع النسخ الاحتياطي: `/var/backups/doctor_syria`
- لاستعادة نسخة احتياطية:
  ```bash
  ./scripts/restore.sh YYYYMMDD_HHMMSS
  ```

### الأمان
- تشغيل فحص الأمان:
  ```bash
  ./scripts/security_check.sh
  ```
- مراجعة `docs/SECURITY.md` للمزيد من المعلومات

### الصيانة
راجع `docs/MAINTENANCE.md` للحصول على:
- إجراءات الصيانة الدورية
- استكشاف الأخطاء وإصلاحها
- دليل التحديث
- جهات الاتصال المهمة

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
