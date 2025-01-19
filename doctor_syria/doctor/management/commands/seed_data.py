from datetime import time, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from faker import Faker

from doctor_syria.doctor.models import Doctor, Schedule, Specialty


class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **kwargs):
        # إنشاء التخصصات
        specialties = [
            "جراحة عامة",
            "أمراض باطنية",
            "أطفال",
            "نسائية وتوليد",
            "عظام",
            "أنف وأذن وحنجرة",
            "عيون",
            "جلدية",
            "قلب وأوعية دموية",
        ]

        for specialty_name in specialties:
            Specialty.objects.get_or_create(name=specialty_name)

        # إنشاء الأطباء
        doctors_data = [
            {
                "username": "dr.ahmad",
                "first_name": "أحمد",
                "last_name": "محمد",
                "specialty": "جراحة عامة",
                "rating": 4.8,
            },
            {
                "username": "dr.sara",
                "first_name": "سارة",
                "last_name": "خالد",
                "specialty": "أطفال",
                "rating": 4.9,
            },
            {
                "username": "dr.omar",
                "first_name": "عمر",
                "last_name": "أحمد",
                "specialty": "قلب وأوعية دموية",
                "rating": 4.7,
            },
            {
                "username": "dr.layla",
                "first_name": "ليلى",
                "last_name": "علي",
                "specialty": "نسائية وتوليد",
                "rating": 4.9,
            },
            {
                "username": "dr.khaled",
                "first_name": "خالد",
                "last_name": "محمود",
                "specialty": "عظام",
                "rating": 4.6,
            },
        ]

        for doctor_data in doctors_data:
            specialty = Specialty.objects.get(name=doctor_data["specialty"])
            user, _ = User.objects.get_or_create(
                username=doctor_data["username"],
                defaults={
                    "first_name": doctor_data["first_name"],
                    "last_name": doctor_data["last_name"],
                    "email": f"{doctor_data['username']}@doctor-syria.com",
                },
            )
            user.set_password("password123")
            user.save()

            doctor, created = Doctor.objects.get_or_create(
                user=user,
                defaults={
                    "specialty": specialty,
                    "rating": doctor_data["rating"],
                    "is_active": True,
                },
            )

            if created:
                # إنشاء جدول المواعيد
                days = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس"]
                for day in days:
                    Schedule.objects.create(
                        doctor=doctor,
                        day=day,
                        start_time=time(9, 0),  # 9:00 AM
                        end_time=time(17, 0),  # 5:00 PM
                        slot_duration=timedelta(minutes=30),
                    )

        self.stdout.write(self.style.SUCCESS("تم إضافة البيانات التجريبية بنجاح!"))
