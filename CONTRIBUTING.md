# دليل المساهمة في مشروع Doctor Syria

<div dir="rtl">

نحن سعداء جداً باهتمامك بالمساهمة في مشروع Doctor Syria! هذا الدليل سيساعدك في فهم كيفية المساهمة في المشروع.

## كيف تساهم

1. **إعداد بيئة التطوير**
   - انسخ المشروع (Fork)
   - استنسخ المشروع محلياً (Clone)
   - قم بإعداد البيئة الافتراضية
   - قم بتثبيت المتطلبات

2. **إنشاء فرع جديد**
   ```bash
   git checkout -b feature/اسم-الميزة
   # أو
   git checkout -b fix/اسم-الإصلاح
   ```

3. **اتبع معايير الكود**
   - استخدم Black لتنسيق الكود
   - اتبع معايير PEP 8
   - أضف تعليقات توضيحية باللغتين العربية والإنجليزية
   - اكتب اختبارات للكود الجديد

4. **اختبر التغييرات**
   ```bash
   pytest
   flake8
   mypy .
   ```

5. **قم بإرسال التغييرات**
   ```bash
   git add .
   git commit -m "وصف التغييرات"
   git push origin اسم-الفرع
   ```

6. **افتح طلب سحب (Pull Request)**
   - اشرح التغييرات بالتفصيل
   - أضف صور للتغييرات إذا كان ممكناً
   - اربط PR بـ issue إذا كان موجوداً

## معايير الكود

- استخدم Python 3.13 أو أحدث
- اتبع معايير PEP 8
- استخدم Type Hints
- اكتب توثيق للدوال والفئات
- اكتب اختبارات للكود

## الاختبارات

- اكتب اختبارات وحدة لكل وظيفة جديدة
- تأكد من تغطية الكود بنسبة 80% على الأقل
- استخدم pytest للاختبارات

## التوثيق

- وثق جميع الدوال والفئات الجديدة
- أضف أمثلة للاستخدام
- حدث ملفات RST إذا لزم الأمر

## الإبلاغ عن المشاكل

- استخدم نظام Issues على GitHub
- اتبع قالب الإبلاغ عن المشاكل
- قدم أكبر قدر ممكن من المعلومات

## أسئلة؟

إذا كان لديك أي أسئلة:
- راجع [الأسئلة الشائعة](https://khaled8809.github.io/doctor-syria-v2/faq.html)
- افتح [issue](https://github.com/khaled8809/doctor-syria-v2/issues)
- تواصل معنا على البريد الإلكتروني: support@doctor-syria.com

</div>