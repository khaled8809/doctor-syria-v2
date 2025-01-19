#!/bin/bash

# التحقق من توفر معرف النسخة الاحتياطية
if [ -z "$1" ]; then
    echo "الرجاء تحديد معرف النسخة الاحتياطية (التاريخ والوقت بتنسيق YYYYMMDD_HHMMSS)"
    exit 1
fi

BACKUP_ID=$1
TEMP_DIR="/tmp/doctor_syria_restore"

# إنشاء مجلد مؤقت
mkdir -p $TEMP_DIR

echo "بدء عملية الاستعادة للنسخة الاحتياطية: $BACKUP_ID"

# تنزيل النسخ الاحتياطية من S3
echo "تنزيل النسخ الاحتياطية من S3..."
aws s3 cp s3://${AWS_BACKUP_BUCKET}/database/db_backup_$BACKUP_ID.sql.gz $TEMP_DIR/
aws s3 cp s3://${AWS_BACKUP_BUCKET}/static_media/static_media_backup_$BACKUP_ID.tar.gz $TEMP_DIR/

# فك ضغط ملفات النسخ الاحتياطي
echo "فك ضغط ملفات النسخ الاحتياطي..."
gunzip $TEMP_DIR/db_backup_$BACKUP_ID.sql.gz
tar -xzf $TEMP_DIR/static_media_backup_$BACKUP_ID.tar.gz -C $TEMP_DIR/

# إيقاف الخدمات
echo "إيقاف الخدمات..."
docker-compose down

# استعادة قاعدة البيانات
echo "استعادة قاعدة البيانات..."
docker-compose up -d db
sleep 10  # انتظار بدء تشغيل قاعدة البيانات
docker-compose exec -T db psql -U doctor_syria_user -d doctor_syria_prod < $TEMP_DIR/db_backup_$BACKUP_ID.sql

# استعادة الملفات الثابتة والوسائط
echo "استعادة الملفات الثابتة والوسائط..."
rm -rf /var/www/doctor_syria/staticfiles/*
rm -rf /var/www/doctor_syria/media/*
cp -r $TEMP_DIR/var/www/doctor_syria/staticfiles/* /var/www/doctor_syria/staticfiles/
cp -r $TEMP_DIR/var/www/doctor_syria/media/* /var/www/doctor_syria/media/

# إعادة تشغيل جميع الخدمات
echo "إعادة تشغيل الخدمات..."
docker-compose up -d

# تنظيف
echo "تنظيف الملفات المؤقتة..."
rm -rf $TEMP_DIR

echo "اكتملت عملية الاستعادة بنجاح!"
