# نظام إدارة العيادات الطبية

نظام متكامل لإدارة العيادات الطبية في سوريا، مبني باستخدام Django و React.

## المميزات الرئيسية

### إدارة المرضى
- تسجيل المرضى وإدارة ملفاتهم الطبية
- حجز المواعيد وإدارة الجدول
- متابعة التاريخ الطبي والتشخيصات

### إدارة الأطباء
- جدولة المواعيد والمناوبات
- إدارة الملف الشخصي والتخصصات
- متابعة الحالات والتقارير الطبية

### نظام الفواتير والمدفوعات
- إصدار الفواتير وإدارتها
- دعم متعدد لطرق الدفع:
  - نقداً
  - بطاقات ائتمان (Stripe)
  - بطاقات محلية (Fatura)
  - تحويل بنكي
  - تأمين صحي
- لوحة تحكم للمدفوعات مع تحليلات متقدمة

### التقارير والتحليلات
- تقارير مالية تفصيلية
- إحصائيات المرضى والزيارات
- تحليلات الأداء

## المتطلبات التقنية

- Python 3.8+
- Django 4.0+
- PostgreSQL
- Node.js 16+
- React 18+

## التثبيت

1. استنساخ المستودع:
```bash
git clone https://github.com/yourusername/doctor-syria-v2.git
cd doctor-syria-v2
```

2. إنشاء بيئة Python افتراضية:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. تثبيت المتطلبات:
```bash
pip install -r requirements.txt
```

4. تثبيت اعتماديات Node.js:
```bash
cd frontend
npm install
```

5. إعداد قاعدة البيانات:
```bash
python manage.py migrate
```

6. تشغيل الخادم:
```bash
python manage.py runserver
```

## الإعداد

1. قم بإنشاء ملف `.env` في المجلد الرئيسي وأضف المتغيرات التالية:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Stripe settings
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

# Fatura settings
FATURA_API_URL=https://api.fatura.sy
FATURA_MERCHANT_ID=your-merchant-id
FATURA_API_KEY=your-api-key
```

## المساهمة

نرحب بمساهماتكم! يرجى اتباع الخطوات التالية:

1. Fork المستودع
2. إنشاء فرع لميزتك (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push إلى الفرع (`git push origin feature/amazing-feature`)
5. فتح Pull Request

## الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.
