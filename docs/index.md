---
layout: default
title: Doctor Syria - نظام إدارة العيادات الطبية
---

# مرحباً بكم في توثيق نظام Doctor Syria

نظام Doctor Syria هو نظام متكامل لإدارة العيادات الطبية والمستشفيات، مبني باستخدام Django و Docker.

## نظرة عامة

نظام Doctor Syria يوفر مجموعة شاملة من الأدوات والميزات لإدارة العيادات الطبية، بما في ذلك:

- ✨ إدارة المواعيد والحجوزات
- 👥 إدارة المرضى والسجلات الطبية
- 💊 إدارة الوصفات الطبية والأدوية
- 📊 التقارير والإحصائيات
- 🏥 إدارة العيادات والمستشفيات
- 💳 نظام الفواتير والمدفوعات
- 📱 واجهة مستخدم سهلة الاستخدام

## روابط سريعة

- [دليل التثبيت](installation.md)
- [دليل المستخدم](user-guide.md)
- [توثيق API](api-reference.md)
- [المساهمة في المشروع](contributing.md)

## المتطلبات الأساسية

- Docker Desktop
- Docker Compose
- Git

## البدء السريع

1. استنساخ المشروع:
```bash
git clone https://github.com/khaled8809/doctor-syria-v2.git
cd doctor-syria-v2
```

2. إعداد البيئة:
```bash
cp .env.example .env
# قم بتعديل الإعدادات في ملف .env
```

3. بناء وتشغيل المشروع:
```bash
docker-compose up -d --build
```

## المساهمة

نرحب بمساهماتكم! يرجى قراءة [دليل المساهمة](contributing.md) للمزيد من المعلومات.

## الترخيص

هذا المشروع مرخص تحت [MIT License](../LICENSE).
