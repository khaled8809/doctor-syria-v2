#!/bin/bash

# تكوين المتغيرات
SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
EMAIL_TO="admin@doctor-syria.com"

# التحقق من حالة الخدمات
check_services() {
    # التحقق من حالة Docker
    if ! docker ps > /dev/null 2>&1; then
        send_alert "خطأ: Docker غير متاح"
    fi

    # التحقق من حالة الخدمات
    for service in web db redis celery celery-beat nginx; do
        if [ "$(docker-compose ps -q $service 2>/dev/null)" == "" ] || [ "$(docker-compose ps -q $service 2>/dev/null | xargs docker inspect -f '{{.State.Running}}')" != "true" ]; then
            send_alert "تحذير: خدمة $service متوقفة"
        fi
    done
}

# التحقق من استخدام الموارد
check_resources() {
    # استخدام CPU
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
    if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
        send_alert "تحذير: استخدام CPU مرتفع ($CPU_USAGE%)"
    fi

    # استخدام الذاكرة
    MEMORY_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    if (( $(echo "$MEMORY_USAGE > 85" | bc -l) )); then
        send_alert "تحذير: استخدام الذاكرة مرتفع ($MEMORY_USAGE%)"
    fi

    # استخدام القرص
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 85 ]; then
        send_alert "تحذير: مساحة القرص منخفضة (${DISK_USAGE}% مستخدم)"
    fi
}

# التحقق من النسخ الاحتياطي
check_backups() {
    LAST_BACKUP=$(ls -t /var/backups/doctor_syria/db_backup_*.sql.gz 2>/dev/null | head -n1)
    if [ -z "$LAST_BACKUP" ] || [ $(find "$LAST_BACKUP" -mtime +1) ]; then
        send_alert "تحذير: لم يتم إجراء نسخ احتياطي في آخر 24 ساعة"
    fi
}

# إرسال التنبيهات
send_alert() {
    MESSAGE="$1"
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # إرسال إلى Slack
    if [ ! -z "$SLACK_WEBHOOK_URL" ]; then
        curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"[$TIMESTAMP] $MESSAGE\"}" $SLACK_WEBHOOK_URL
    fi
    
    # إرسال بريد إلكتروني
    echo "[$TIMESTAMP] $MESSAGE" | mail -s "تنبيه Doctor Syria" $EMAIL_TO
    
    # تسجيل في السجلات
    logger -t "doctor_syria_monitor" "$MESSAGE"
}

# التنفيذ الرئيسي
while true; do
    check_services
    check_resources
    check_backups
    sleep 300  # انتظار 5 دقائق قبل التحقق التالي
done
