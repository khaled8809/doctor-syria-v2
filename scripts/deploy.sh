#!/bin/bash

# تحديث النظام
apt-get update
apt-get upgrade -y

# تثبيت المتطلبات الأساسية
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    git \
    ufw

# تثبيت Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

# تثبيت Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# إعداد جدار الحماية
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable

# إنشاء مستخدم للتطبيق
useradd -m -s /bin/bash doctor_syria
usermod -aG docker doctor_syria

# إنشاء المجلدات اللازمة
mkdir -p /var/www/doctor-syria
chown -R doctor_syria:doctor_syria /var/www/doctor-syria

# تثبيت Certbot للحصول على شهادة SSL
apt-get install -y certbot python3-certbot-nginx

# إعداد Nginx
apt-get install -y nginx
systemctl enable nginx
systemctl start nginx

# تنزيل المشروع
cd /var/www/doctor-syria
git clone https://github.com/khaled8809/doctor-syria-v2.git .
chown -R doctor_syria:doctor_syria .

# إنشاء المجلدات للبيانات المستمرة
mkdir -p /var/www/doctor-syria/data/{postgres,redis,media,static}
chown -R doctor_syria:doctor_syria /var/www/doctor-syria/data

# إعداد النسخ الاحتياطي التلقائي
mkdir -p /var/www/doctor-syria/backups
chown -R doctor_syria:doctor_syria /var/www/doctor-syria/backups

# تثبيت أدوات المراقبة
apt-get install -y prometheus node-exporter
