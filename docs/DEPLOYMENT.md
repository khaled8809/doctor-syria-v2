# دليل النشر

## المتطلبات الأساسية

- Docker و Docker Compose
- شهادة SSL صالحة
- اسم نطاق مسجل
- حساب AWS (للتخزين)
- حساب Stripe (للمدفوعات)

## خطوات النشر

### 1. إعداد البيئة

```bash
# نسخ ملف البيئة
cp .env.example .env

# تحديث المتغيرات البيئية
nano .env
```

### 2. إعداد SSL

```bash
# تثبيت Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# الحصول على شهادة SSL
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 3. تحديث إعدادات Nginx

```bash
# تحديث domain في ملف nginx.conf
sudo nano deployment/nginx.conf

# نسخ الملف إلى موقعه
sudo cp deployment/nginx.conf /etc/nginx/sites-available/doctor_syria
sudo ln -s /etc/nginx/sites-available/doctor_syria /etc/nginx/sites-enabled/
```

### 4. بناء وتشغيل الخدمات

```bash
# بناء الصور
docker-compose build

# تشغيل الخدمات
docker-compose up -d

# التحقق من الحالة
docker-compose ps
```

### 5. إعداد قاعدة البيانات

```bash
# تشغيل الترحيلات
docker-compose exec web python manage.py migrate

# جمع الملفات الثابتة
docker-compose exec web python manage.py collectstatic --no-input

# إنشاء مستخدم مشرف
docker-compose exec web python manage.py createsuperuser
```

### 6. التحقق من النشر

- التحقق من عمل HTTPS
- التحقق من تحميل الملفات الثابتة
- التحقق من اتصال قاعدة البيانات
- التحقق من عمل Celery
- التحقق من تكامل Stripe

## المراقبة

- مراقبة السجلات: `docker-compose logs -f`
- مراقبة الأداء: Prometheus/Grafana
- تتبع الأخطاء: Sentry

## النسخ الاحتياطي

```bash
# نسخ احتياطي لقاعدة البيانات
docker-compose exec db pg_dump -U postgres doctor_syria > backup.sql

# نسخ احتياطي للملفات الثابتة والوسائط
aws s3 sync staticfiles/ s3://your-bucket/static/
aws s3 sync media/ s3://your-bucket/media/
```

## استكشاف الأخطاء وإصلاحها

### مشاكل شائعة

1. **خطأ 502 Bad Gateway**
   - التحقق من تشغيل Gunicorn
   - التحقق من ملف سجل Nginx

2. **مشاكل الملفات الثابتة**
   - التحقق من مسارات الملفات الثابتة في Nginx
   - تشغيل collectstatic مرة أخرى

3. **مشاكل Celery**
   - التحقق من اتصال Redis
   - مراجعة سجلات Celery

## تحديث التطبيق

```bash
# سحب التغييرات الجديدة
git pull origin main

# إعادة بناء الصور
docker-compose build

# إعادة تشغيل الخدمات
docker-compose down
docker-compose up -d

# تشغيل الترحيلات
docker-compose exec web python manage.py migrate
```
