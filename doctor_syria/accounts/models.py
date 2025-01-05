from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import Avg

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', _('Patient')),
        ('doctor', _('Doctor')),
        ('pharmacy', _('Pharmacy')),
        ('laboratory', _('Laboratory')),
        ('company', _('Pharmaceutical Company')),
        ('nurse', _('Nurse')),
        ('staff', _('Staff')),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = PhoneNumberField(unique=True)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class Area(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}, {self.city}"

class Clinic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='clinics/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def average_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg'] or 0
    
    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=20)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hospitals/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def average_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg'] or 0
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.SET_NULL, null=True, blank=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    education = models.TextField(blank=True, default='')
    certifications = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, unique=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_for_online = models.BooleanField(default=False)
    
    @property
    def average_rating(self):
        return self.review_set.aggregate(Avg('rating'))['rating__avg'] or 0
    
    def __str__(self):
        return f"د. {self.user.get_full_name()}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    blood_type = models.CharField(max_length=5, blank=True)
    allergies = models.TextField(blank=True)
    chronic_diseases = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.get_full_name()

class Pharmacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacy_profile')
    license_number = models.CharField(max_length=50, unique=True)
    opening_hours = models.CharField(max_length=100)
    delivery_available = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.get_full_name()

class Laboratory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='laboratory_profile')
    license_number = models.CharField(max_length=50, unique=True)
    services = models.TextField()
    opening_hours = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.get_full_name()

class PharmaceuticalCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    license_number = models.CharField(max_length=50, unique=True)
    registration_number = models.CharField(max_length=50, unique=True)
    company_size = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.get_full_name()

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nurse_profile')
    department = models.ForeignKey('hms.Department', on_delete=models.SET_NULL, null=True)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    years_of_experience = models.IntegerField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Nurse"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.ForeignKey('hms.Department', on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50, unique=True)
    hire_date = models.DateField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"
