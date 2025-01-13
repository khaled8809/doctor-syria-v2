#!/bin/bash

# تكوين المتغيرات
APP_URL="https://doctor-syria.com"
ENDPOINTS=(
    "/health/"
    "/api/health/"
    "/api/doctors/"
    "/api/specialties/"
)
SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}

# التحقق من نقطة نهاية
check_endpoint() {
    local endpoint=$1
    local url="${APP_URL}${endpoint}"
    local start_time=$(date +%s.%N)
    
    response=$(curl -s -w "\n%{http_code}\n%{time_total}" "$url")
    status_code=$(echo "$response" | tail -n2 | head -n1)
    response_time=$(echo "$response" | tail -n1)
    
    if [ "$status_code" != "200" ]; then
        send_alert "فشل: $endpoint (كود الحالة: $status_code)"
        return 1
    fi
    
    # التحقق من وقت الاستجابة (> 2 ثوان يعتبر بطيء)
    if (( $(echo "$response_time > 2" | bc -l) )); then
        send_alert "تحذير: $endpoint بطيء (وقت الاستجابة: ${response_time}s)"
    fi
    
    return 0
}

# التحقق من حالة قاعدة البيانات
check_database() {
    if ! docker-compose exec -T db pg_isready -U doctor_syria_user -d doctor_syria_prod > /dev/null 2>&1; then
        send_alert "خطأ: قاعدة البيانات غير متاحة"
        return 1
    fi
    return 0
}

# التحقق من حالة Redis
check_redis() {
    if ! docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
        send_alert "خطأ: Redis غير متاح"
        return 1
    fi
    return 0
}

# التحقق من حالة Celery
check_celery() {
    if ! docker-compose exec -T celery celery -A doctor_syria inspect ping > /dev/null 2>&1; then
        send_alert "خطأ: Celery غير متاح"
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
    logger -t "doctor_syria_healthcheck" "$MESSAGE"
}

# التنفيذ الرئيسي
main() {
    errors=0
    
    # التحقق من الخدمات الأساسية
    check_database || ((errors++))
    check_redis || ((errors++))
    check_celery || ((errors++))
    
    # التحقق من نقاط النهاية
    for endpoint in "${ENDPOINTS[@]}"; do
        check_endpoint "$endpoint" || ((errors++))
    done
    
    # إخراج النتيجة النهائية
    if [ $errors -eq 0 ]; then
        echo "جميع الفحوصات ناجحة"
        exit 0
    else
        echo "فشل $errors فحص/فحوصات"
        exit 1
    fi
}

# تشغيل الفحص
main
