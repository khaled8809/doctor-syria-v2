from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from accounts.models import Doctor, Patient


class NutritionProfile(models.Model):
    """الملف التغذوي"""

    ACTIVITY_LEVELS = [
        ("sedentary", "خامل"),
        ("lightly_active", "قليل النشاط"),
        ("moderately_active", "متوسط النشاط"),
        ("very_active", "نشيط جداً"),
        ("extra_active", "نشيط للغاية"),
    ]

    GOAL_CHOICES = [
        ("weight_loss", "إنقاص الوزن"),
        ("weight_gain", "زيادة الوزن"),
        ("maintenance", "المحافظة على الوزن"),
        ("muscle_gain", "بناء العضلات"),
        ("health_improvement", "تحسين الصحة"),
    ]

    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
    nutritionist = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    height = models.FloatField(help_text="الطول بالسنتيمتر")
    current_weight = models.FloatField(help_text="الوزن بالكيلوغرام")
    target_weight = models.FloatField(help_text="الوزن المستهدف بالكيلوغرام")
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVELS)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    dietary_restrictions = models.JSONField(default=list)
    allergies = models.JSONField(default=list)
    medical_conditions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ملف تغذية - {self.patient.user.get_full_name()}"

    @property
    def bmi(self):
        """حساب مؤشر كتلة الجسم"""
        height_in_meters = self.height / 100
        return self.current_weight / (height_in_meters**2)


class DietPlan(models.Model):
    """خطة الحمية الغذائية"""

    STATUS_CHOICES = [
        ("active", "نشطة"),
        ("completed", "مكتملة"),
        ("paused", "موقوفة"),
        ("discontinued", "متوقفة"),
    ]

    profile = models.ForeignKey(NutritionProfile, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    daily_calories = models.IntegerField()
    macronutrients = models.JSONField()  # نسب البروتين والكربوهيدرات والدهون
    meal_distribution = models.JSONField()  # توزيع السعرات على الوجبات
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"خطة حمية - {self.profile.patient.user.get_full_name()}"


class Meal(models.Model):
    """الوجبات الغذائية"""

    MEAL_TYPES = [
        ("breakfast", "فطور"),
        ("morning_snack", "وجبة خفيفة صباحية"),
        ("lunch", "غداء"),
        ("afternoon_snack", "وجبة خفيفة مسائية"),
        ("dinner", "عشاء"),
        ("evening_snack", "وجبة خفيفة ليلية"),
    ]

    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    calories = models.IntegerField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()
    ingredients = models.JSONField()
    preparation_instructions = models.TextField()
    alternatives = models.JSONField(default=list)

    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.name}"


class FoodItem(models.Model):
    """العناصر الغذائية"""

    FOOD_CATEGORIES = [
        ("fruits", "فواكه"),
        ("vegetables", "خضروات"),
        ("grains", "حبوب"),
        ("proteins", "بروتينات"),
        ("dairy", "منتجات الألبان"),
        ("fats", "دهون"),
        ("beverages", "مشروبات"),
        ("snacks", "وجبات خفيفة"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=FOOD_CATEGORIES)
    calories_per_100g = models.IntegerField()
    protein_per_100g = models.FloatField()
    carbs_per_100g = models.FloatField()
    fats_per_100g = models.FloatField()
    fiber_per_100g = models.FloatField()
    vitamins = models.JSONField(default=dict)
    minerals = models.JSONField(default=dict)
    serving_size = models.CharField(max_length=100)
    image = models.ImageField(upload_to="food_items/", null=True, blank=True)

    def __str__(self):
        return self.name


class NutritionLog(models.Model):
    """سجل التغذية"""

    profile = models.ForeignKey(NutritionProfile, on_delete=models.CASCADE)
    date = models.DateField()
    meals = models.JSONField()
    total_calories = models.IntegerField()
    total_protein = models.FloatField()
    total_carbs = models.FloatField()
    total_fats = models.FloatField()
    water_intake = models.FloatField(help_text="كمية الماء باللتر")
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"سجل تغذية - {self.profile.patient.user.get_full_name()} - {self.date}"


class WeightLog(models.Model):
    """سجل الوزن"""

    profile = models.ForeignKey(NutritionProfile, on_delete=models.CASCADE)
    weight = models.FloatField()
    date = models.DateField()
    body_fat_percentage = models.FloatField(null=True, blank=True)
    muscle_mass = models.FloatField(null=True, blank=True)
    waist_circumference = models.FloatField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"سجل وزن - {self.profile.patient.user.get_full_name()} - {self.date}"


class Recipe(models.Model):
    """الوصفات الصحية"""

    name = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.JSONField()
    instructions = models.TextField()
    preparation_time = models.DurationField()
    cooking_time = models.DurationField()
    servings = models.PositiveIntegerField()
    calories_per_serving = models.IntegerField()
    protein_per_serving = models.FloatField()
    carbs_per_serving = models.FloatField()
    fats_per_serving = models.FloatField()
    image = models.ImageField(upload_to="recipes/", null=True, blank=True)
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class NutritionGoal(models.Model):
    """الأهداف التغذوية"""

    STATUS_CHOICES = [
        ("pending", "قيد الانتظار"),
        ("in_progress", "قيد التنفيذ"),
        ("achieved", "محقق"),
        ("failed", "غير محقق"),
    ]

    profile = models.ForeignKey(NutritionProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_value = models.FloatField()
    current_value = models.FloatField()
    start_date = models.DateField()
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    progress_notes = models.TextField(blank=True)

    def __str__(self):
        return f"هدف - {self.title} - {self.profile.patient.user.get_full_name()}"
