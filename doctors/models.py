from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Specialty(models.Model):
    name = models.CharField(max_length=100, verbose_name="التخصص")
    description = models.TextField(verbose_name="الوصف", blank=True)

    class Meta:
        verbose_name = "تخصص"
        verbose_name_plural = "التخصصات"

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=100, verbose_name="المنطقة")
    city = models.CharField(max_length=100, verbose_name="المدينة")

    class Meta:
        verbose_name = "منطقة"
        verbose_name_plural = "المناطق"

    def __str__(self):
        return f"{self.name} - {self.city}"

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name="المستخدم"
    )
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True, verbose_name="التخصص")
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, verbose_name="المنطقة")
    title = models.CharField(max_length=100, verbose_name="اللقب", default="د.")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    address = models.TextField(verbose_name="العنوان")
    bio = models.TextField(verbose_name="نبذة عن الطبيب")
    experience_years = models.IntegerField(verbose_name="سنوات الخبرة", default=0)
    rating = models.FloatField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name="التقييم"
    )
    is_available = models.BooleanField(default=True, verbose_name="متاح")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنضمام")

    class Meta:
        verbose_name = "طبيب"
        verbose_name_plural = "الأطباء"

    def __str__(self):
        return f"{self.title} {self.user.get_full_name()}"

class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews', verbose_name="الطبيب")
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='doctor_reviews',
        verbose_name="المريض"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="التقييم"
    )
    comment = models.TextField(verbose_name="التعليق")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التعليق")

    class Meta:
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"
        ordering = ['-created_at']

    def __str__(self):
        return f"تقييم {self.doctor} من {self.patient.get_full_name()}"

class BlogPost(models.Model):
    CATEGORIES = [
        ('general', 'صحة عامة'),
        ('technology', 'تقنيات طبية'),
        ('nutrition', 'تغذية'),
        ('pediatrics', 'طب الأطفال'),
        ('cardiology', 'طب القلب'),
    ]

    title = models.CharField(max_length=200, verbose_name="العنوان")
    content = models.TextField(verbose_name="المحتوى")
    category = models.CharField(max_length=20, choices=CATEGORIES, verbose_name="التصنيف")
    author = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, verbose_name="الكاتب")
    read_time = models.IntegerField(verbose_name="وقت القراءة بالدقائق", default=5)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ النشر")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "مقال"
        verbose_name_plural = "المقالات"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
