from django.db import models


class UserType(models.TextChoices):
    ADMIN = "admin", "مدير النظام"
    DOCTOR = "doctor", "طبيب"
    PATIENT = "patient", "مريض"
    PHARMACY = "pharmacy", "صيدلية"
    LAB = "lab", "مختبر"
    HOSPITAL = "hospital", "مستشفى"
    INSURANCE = "insurance", "شركة تأمين"
    STAFF = "staff", "موظف"
    NURSE = "nurse", "ممرض/ة"


class GenderType(models.TextChoices):
    MALE = "M", "ذكر"
    FEMALE = "F", "أنثى"


class MaritalStatus(models.TextChoices):
    SINGLE = "single", "أعزب/عزباء"
    MARRIED = "married", "متزوج/ة"
    DIVORCED = "divorced", "مطلق/ة"
    WIDOWED = "widowed", "أرمل/ة"


class BloodType(models.TextChoices):
    A_POSITIVE = "A+", "A+"
    A_NEGATIVE = "A-", "A-"
    B_POSITIVE = "B+", "B+"
    B_NEGATIVE = "B-", "B-"
    O_POSITIVE = "O+", "O+"
    O_NEGATIVE = "O-", "O-"
    AB_POSITIVE = "AB+", "AB+"
    AB_NEGATIVE = "AB-", "AB-"


class SpecialtyType(models.TextChoices):
    GENERAL = "general", "طب عام"
    CARDIOLOGY = "cardiology", "قلبية"
    DERMATOLOGY = "dermatology", "جلدية"
    NEUROLOGY = "neurology", "عصبية"
    ORTHOPEDICS = "orthopedics", "عظمية"
    PEDIATRICS = "pediatrics", "أطفال"
    PSYCHIATRY = "psychiatry", "نفسية"
    OPHTHALMOLOGY = "ophthalmology", "عيون"
    DENTISTRY = "dentistry", "أسنان"
    SURGERY = "surgery", "جراحة عامة"
    GYNECOLOGY = "gynecology", "نسائية وتوليد"
    UROLOGY = "urology", "بولية"
    ENT = "ent", "أنف وأذن وحنجرة"
    INTERNAL = "internal", "داخلية"


class IdentificationType(models.TextChoices):
    NATIONAL_ID = "national_id", "الهوية الوطنية"
    PASSPORT = "passport", "جواز سفر"
    MILITARY_ID = "military_id", "الهوية العسكرية"
    RESIDENCE = "residence", "إقامة"
