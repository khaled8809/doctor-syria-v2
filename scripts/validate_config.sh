#!/bin/bash

# تكوين الألوان للإخراج
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# وظيفة للتحقق من المتغيرات البيئية
check_env_var() {
    local var_name=$1
    local var_value=${!var_name}
    if [ -z "$var_value" ]; then
        echo -e "${RED}خطأ: المتغير $var_name غير محدد${NC}"
        return 1
    fi
    if [[ $var_value == *"please_change"* || $var_value == *"your-"* ]]; then
        echo -e "${YELLOW}تحذير: المتغير $var_name يحتوي على قيمة افتراضية${NC}"
        return 1
    fi
    echo -e "${GREEN}✓ المتغير $var_name محدد بشكل صحيح${NC}"
    return 0
}

# التحقق من وجود الملفات المطلوبة
echo "التحقق من الملفات الأساسية..."
required_files=(
    "docker-compose.yml"
    "deployment/nginx.conf"
    "monitoring/prometheus.yml"
    "monitoring/slack_config.yml"
    ".env.production"
)

errors=0
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}خطأ: الملف $file غير موجود${NC}"
        ((errors++))
    else
        echo -e "${GREEN}✓ الملف $file موجود${NC}"
    fi
done

# التحقق من المتغيرات البيئية
echo -e "\nالتحقق من المتغيرات البيئية..."
source .env.production

env_vars=(
    "DJANGO_SECRET_KEY"
    "DB_PASSWORD"
    "REDIS_PASSWORD"
    "EMAIL_HOST_PASSWORD"
    "AWS_ACCESS_KEY_ID"
    "AWS_SECRET_ACCESS_KEY"
    "STRIPE_SECRET_KEY"
    "SENTRY_DSN"
    "GRAFANA_ADMIN_PASSWORD"
)

for var in "${env_vars[@]}"; do
    check_env_var "$var" || ((errors++))
done

# التحقق من تكوين Docker Compose
echo -e "\nالتحقق من تكوين Docker Compose..."
if ! docker-compose config > /dev/null 2>&1; then
    echo -e "${RED}خطأ: تكوين Docker Compose غير صحيح${NC}"
    ((errors++))
else
    echo -e "${GREEN}✓ تكوين Docker Compose صحيح${NC}"
fi

# التحقق من تكوين Nginx
echo -e "\nالتحقق من تكوين Nginx..."
if ! nginx -t -c deployment/nginx.conf > /dev/null 2>&1; then
    echo -e "${RED}خطأ: تكوين Nginx غير صحيح${NC}"
    ((errors++))
else
    echo -e "${GREEN}✓ تكوين Nginx صحيح${NC}"
fi

# النتيجة النهائية
echo -e "\nنتيجة التحقق:"
if [ $errors -eq 0 ]; then
    echo -e "${GREEN}✓ جميع التحققات ناجحة${NC}"
    exit 0
else
    echo -e "${RED}✗ يوجد $errors أخطاء تحتاج إلى معالجة${NC}"
    exit 1
fi
