#!/bin/bash

echo "بدء فحص الأمان..."

# التحقق من تحديثات النظام
echo "التحقق من تحديثات النظام..."
apt list --upgradable

# التحقق من تحديثات Docker
echo "التحقق من تحديثات Docker..."
docker images --format "{{.Repository}}:{{.Tag}}" | while read -r image; do
    docker pull "$image" 2>/dev/null
done

# التحقق من تصاريح الملفات
echo "التحقق من تصاريح الملفات..."
find /var/www/doctor_syria -type f -perm /o+w -ls
find /etc/doctor_syria -type f -perm /o+w -ls

# التحقق من شهادة SSL
echo "التحقق من شهادة SSL..."
certbot certificates

# التحقق من إعدادات Nginx
echo "التحقق من إعدادات Nginx..."
nginx -t

# التحقق من المتغيرات البيئية
echo "التحقق من المتغيرات البيئية..."
if [ -f .env.production ]; then
    if grep -q "DEBUG=True" .env.production; then
        echo "تحذير: وضع التصحيح مفعل في الإنتاج!"
    fi
    if grep -q "SECRET_KEY=" .env.production; then
        echo "تحذير: يجب تغيير مفتاح السر الافتراضي!"
    fi
fi

# التحقق من النسخ الاحتياطي
echo "التحقق من النسخ الاحتياطي..."
if [ -d "/var/backups/doctor_syria" ]; then
    find /var/backups/doctor_syria -type f -mtime -1 -name "*.sql.gz" | grep . > /dev/null
    if [ $? -ne 0 ]; then
        echo "تحذير: لم يتم العثور على نسخ احتياطية حديثة!"
    fi
fi

# التحقق من السجلات
echo "التحقق من السجلات..."
find /var/log/doctor_syria -type f -exec grep -l "ERROR\|CRITICAL\|WARNING" {} \;

# التحقق من منافذ الشبكة المفتوحة
echo "التحقق من منافذ الشبكة..."
netstat -tulpn | grep LISTEN

echo "اكتمل فحص الأمان!"
