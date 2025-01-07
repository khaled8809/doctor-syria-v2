# واجهة المستخدم لنظام Doctor Syria

## التقنيات المستخدمة
- React 18
- TypeScript
- Material-UI v5
- Redux Toolkit
- React Query
- React Router v6
- i18next للترجمة
- Jest للاختبارات

## هيكل المشروع
```
frontend/
├── src/
│   ├── components/      # المكونات القابلة لإعادة الاستخدام
│   ├── pages/          # صفحات التطبيق
│   ├── features/       # مميزات التطبيق (Redux Slices)
│   ├── hooks/          # Hooks مخصصة
│   ├── api/            # خدمات API
│   ├── utils/          # أدوات مساعدة
│   ├── types/          # أنواع TypeScript
│   ├── locales/        # ملفات الترجمة
│   └── theme/          # تخصيص المظهر
```

## المميزات
- تصميم متجاوب
- دعم اللغة العربية والإنجليزية
- الوضع الليلي/النهاري
- لوحة تحكم تفاعلية
- تقارير ورسوم بيانية
- تنبيهات في الوقت الفعلي
- دعم الأجهزة المحمولة
