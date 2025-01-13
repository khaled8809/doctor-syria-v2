# Doctor Syria - نظام إدارة المستشفيات والعيادات

نظام شامل لإدارة المستشفيات والعيادات الطبية، مبني باستخدام Django وDocker.

## المميزات الرئيسية 

- إدارة المرضى والمواعيد
- السجلات الطبية الإلكترونية
- إدارة العيادات والمستشفيات
- نظام المختبرات والأشعة
- نظام الصيدلية
- التشخيص بمساعدة الذكاء الاصطناعي
- نظام الفوترة والمحاسبة
- تقارير وإحصائيات متقدمة
- نظام التنبيهات والإشعارات
- واجهة مستخدم سهلة وحديثة

## المتطلبات الأساسية 

- Docker و Docker Compose
- Git
- Python 3.9+
- Node.js 16+
- PostgreSQL 15+
- Redis 7+

## البدء السريع 

1. استنساخ المشروع:
```bash
git clone https://github.com/yourusername/doctor-syria-v2.git
cd doctor-syria-v2
```

2. إنشاء ملف البيئة:
```bash
cp .env.example .env.production
# قم بتعديل الإعدادات في ملف .env.production
```

3. بناء وتشغيل الخدمات:
```bash
docker-compose up -d --build
```

4. إنشاء مستخدم مدير:
```bash
docker-compose exec web python manage.py createsuperuser
```

## الهيكل التنظيمي للمشروع 

```
doctor-syria-v2/
├── accounts/          # إدارة المستخدمين والصلاحيات
├── appointments/      # نظام المواعيد
├── clinics/          # إدارة العيادات
├── doctor/           # إدارة الأطباء
├── patient_records/  # السجلات الطبية
├── pharmacy/         # نظام الصيدلية
├── laboratory/       # نظام المختبر
├── radiology/        # نظام الأشعة
├── billing/          # نظام الفوترة
└── monitoring/       # نظام المراقبة
```

## المراقبة والتتبع 

- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Flower (Celery): `http://localhost:5555`

## النسخ الاحتياطي 

يتم إجراء نسخ احتياطي تلقائي يومياً لقاعدة البيانات في المسار:
```
/var/backups/doctor-syria/
```

## المساهمة 

نرحب بمساهماتكم! يرجى قراءة [دليل المساهمة](CONTRIBUTING.md) للمزيد من المعلومات.

## الترخيص 

هذا المشروع مرخص تحت [MIT License](LICENSE).

## الدعم 

إذا واجهت أي مشكلة أو لديك أي استفسار، يرجى فتح issue في GitHub.
