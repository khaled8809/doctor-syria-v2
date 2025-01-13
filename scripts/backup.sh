#!/bin/bash

# تكوين المتغيرات
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/doctor_syria"
RETENTION_DAYS=7

# إنشاء مجلد النسخ الاحتياطي إذا لم يكن موجوداً
mkdir -p $BACKUP_DIR

# نسخ احتياطي لقاعدة البيانات
echo "بدء النسخ الاحتياطي لقاعدة البيانات..."
docker-compose exec -T db pg_dump -U doctor_syria_user doctor_syria_prod > $BACKUP_DIR/db_backup_$TIMESTAMP.sql

# ضغط النسخة الاحتياطية
gzip $BACKUP_DIR/db_backup_$TIMESTAMP.sql

# نسخ احتياطي للملفات الثابتة والوسائط
echo "نسخ الملفات الثابتة والوسائط..."
tar -czf $BACKUP_DIR/static_media_backup_$TIMESTAMP.tar.gz /var/www/doctor_syria/staticfiles /var/www/doctor_syria/media

# رفع النسخ الاحتياطية إلى S3
echo "رفع النسخ الاحتياطية إلى S3..."
aws s3 cp $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz s3://${AWS_BACKUP_BUCKET}/database/
aws s3 cp $BACKUP_DIR/static_media_backup_$TIMESTAMP.tar.gz s3://${AWS_BACKUP_BUCKET}/static_media/

# حذف النسخ الاحتياطية القديمة محلياً
echo "تنظيف النسخ الاحتياطية القديمة..."
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete

# حذف النسخ الاحتياطية القديمة من S3
echo "تنظيف النسخ الاحتياطية القديمة من S3..."
aws s3 ls s3://${AWS_BACKUP_BUCKET}/database/ | grep -v "$(date -d "$RETENTION_DAYS days ago" +%Y-%m-%d)" | awk '{print $4}' | xargs -I {} aws s3 rm s3://${AWS_BACKUP_BUCKET}/database/{}
aws s3 ls s3://${AWS_BACKUP_BUCKET}/static_media/ | grep -v "$(date -d "$RETENTION_DAYS days ago" +%Y-%m-%d)" | awk '{print $4}' | xargs -I {} aws s3 rm s3://${AWS_BACKUP_BUCKET}/static_media/{}

echo "اكتمل النسخ الاحتياطي بنجاح!"
