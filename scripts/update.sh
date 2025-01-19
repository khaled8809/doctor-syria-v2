#!/bin/bash

# تكوين المتغيرات
SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
BACKUP_BEFORE_UPDATE=true

# وظيفة النسخ الاحتياطي
backup() {
    echo "إجراء نسخ احتياطي قبل التحديث..."
    ./backup.sh
    if [ $? -ne 0 ]; then
        send_alert "فشل: فشل النسخ الاحتياطي قبل التحديث"
        exit 1
    fi
}

# وظيفة التحديث
update() {
    echo "بدء عملية التحديث..."
    
    # تحديث الكود من Git
    git pull
    if [ $? -ne 0 ]; then
        send_alert "فشل: فشل تحديث الكود من Git"
        exit 1
    fi
    
    # إعادة بناء الصور
    docker-compose build
    if [ $? -ne 0 ]; then
        send_alert "فشل: فشل إعادة بناء الصور"
        exit 1
    fi
    
    # تحديث قاعدة البيانات
    docker-compose run --rm web python manage.py migrate
    if [ $? -ne 0 ]; then
        send_alert "فشل: فشل تحديث قاعدة البيانات"
        exit 1
    fi
    
    # جمع الملفات الثابتة
    docker-compose run --rm web python manage.py collectstatic --noinput
    if [ $? -ne 0 ]; then
        send_alert "فشل: فشل جمع الملفات الثابتة"
        exit 1
    }
    
    # إعادة تشغيل الخدمات
    docker-compose down
    docker-compose up -d
    if [ $? -ne 0 ]; then
        send_alert "فشل: فشل إعادة تشغيل الخدمات"
        exit 1
    fi
}

# التحقق من الصحة بعد التحديث
verify() {
    echo "التحقق من الصحة بعد التحديث..."
    
    # انتظار بدء تشغيل الخدمات
    sleep 30
    
    # تشغيل فحص الصحة
    ./healthcheck.sh
    if [ $? -ne 0 ]; then
        send_alert "فشل: فشل التحقق من الصحة بعد التحديث"
        return 1
    fi
    
    return 0
}

# إرسال التنبيهات
send_alert() {
    MESSAGE="$1"
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # إرسال إلى Slack
    if [ ! -z "$SLACK_WEBHOOK_URL" ]; then
        curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"[$TIMESTAMP] $MESSAGE\"}" $SLACK_WEBHOOK_URL
    fi
    
    # تسجيل في السجلات
    logger -t "doctor_syria_update" "$MESSAGE"
}

# التنفيذ الرئيسي
main() {
    # النسخ الاحتياطي إذا تم تمكينه
    if [ "$BACKUP_BEFORE_UPDATE" = true ]; then
        backup
    fi
    
    # تنفيذ التحديث
    update
    
    # التحقق من الصحة
    if verify; then
        send_alert "نجاح: اكتمل التحديث بنجاح"
        exit 0
    else
        send_alert "فشل: فشل التحقق من الصحة بعد التحديث"
        exit 1
    fi
}

# تشغيل التحديث
main
