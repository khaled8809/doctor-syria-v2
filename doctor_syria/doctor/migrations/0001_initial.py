# Generated by Django 4.2.8 on 2025-01-08 09:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("patient_records", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Doctor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("specialization", models.CharField(max_length=100)),
                ("license_number", models.CharField(max_length=50, unique=True)),
                ("years_of_experience", models.IntegerField()),
                ("education", models.TextField()),
                ("certifications", models.TextField(blank=True)),
                ("bio", models.TextField(blank=True)),
                ("availability", models.JSONField(default=dict)),
                ("rating", models.FloatField(default=0.0)),
                ("is_verified", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doctor_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Prescription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("diagnosis", models.TextField()),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doctor.doctor"
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="patient_records.patient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PrescriptionItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("medicine_name", models.CharField(max_length=100)),
                ("dosage", models.CharField(max_length=50)),
                ("frequency", models.CharField(max_length=50)),
                ("duration", models.CharField(max_length=50)),
                ("instructions", models.TextField()),
                (
                    "prescription",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="doctor.prescription",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MedicalNote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("note_type", models.CharField(max_length=50)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doctor.doctor"
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="patient_records.patient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="DoctorSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day_of_week", models.IntegerField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                ("is_available", models.BooleanField(default=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doctor.doctor"
                    ),
                ),
            ],
            options={
                "unique_together": {("doctor", "day_of_week")},
            },
        ),
        migrations.CreateModel(
            name="DoctorReview",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rating", models.IntegerField()),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_verified", models.BooleanField(default=False)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doctor.doctor"
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="patient_records.patient",
                    ),
                ),
            ],
            options={
                "unique_together": {("doctor", "patient")},
            },
        ),
    ]