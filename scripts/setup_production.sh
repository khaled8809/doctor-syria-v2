#!/bin/bash

# إنشاء المجلدات اللازمة
mkdir -p /var/www/doctor_syria/{staticfiles,media}
mkdir -p /var/log/doctor_syria
mkdir -p /var/backups/doctor_syria

# نسخ ملفات التكوين
cp deployment/nginx.conf /etc/nginx/conf.d/doctor-syria.conf
cp monitoring/prometheus.yml /etc/prometheus/prometheus.yml
cp monitoring/slack_config.yml /etc/alertmanager/alertmanager.yml
cp deployment/crontab /etc/cron.d/doctor-syria

# تعيين الأذونات
chown -R www-data:www-data /var/www/doctor_syria
chmod -R 755 /var/www/doctor_syria
chmod -R 755 scripts/

# إعداد Certbot لشهادة SSL
certbot certonly --webroot -w /var/www/doctor_syria -d doctor-syria.com -d www.doctor-syria.com

# تحديث النظام وتثبيت التبعيات
apt-get update
apt-get install -y prometheus prometheus-alertmanager grafana

# تكوين Prometheus
systemctl enable prometheus
systemctl start prometheus

# تكوين Alertmanager
systemctl enable prometheus-alertmanager
systemctl start prometheus-alertmanager

# تكوين Grafana
systemctl enable grafana-server
systemctl start grafana-server

# إعادة تحميل Nginx
systemctl reload nginx

echo "تم إعداد بيئة الإنتاج بنجاح!"
