# Generated by Django 5.1.4 on 2025-01-05 14:19

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0004_alter_user_options_alter_user_managers_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Allergy",
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
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="تاريخ الإنشاء"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="محذوف"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاريخ الحذف"
                    ),
                ),
                (
                    "allergy_type",
                    models.CharField(
                        choices=[
                            ("food", "طعام"),
                            ("medication", "دواء"),
                            ("environmental", "بيئية"),
                            ("insect", "حشرات"),
                            ("latex", "لاتكس"),
                            ("other", "أخرى"),
                        ],
                        max_length=20,
                        verbose_name="نوع الحساسية",
                    ),
                ),
                ("allergen", models.CharField(max_length=200, verbose_name="المسبب")),
                (
                    "reaction",
                    models.CharField(
                        choices=[
                            ("mild", "خفيفة"),
                            ("moderate", "متوسطة"),
                            ("severe", "شديدة"),
                            ("anaphylaxis", "صدمة تأقية"),
                        ],
                        max_length=20,
                        verbose_name="رد الفعل",
                    ),
                ),
                ("diagnosis_date", models.DateField(verbose_name="تاريخ التشخيص")),
                ("notes", models.TextField(blank=True, verbose_name="ملاحظات")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الإنشاء بواسطة",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الحذف بواسطة",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        limit_choices_to={"user_type": "patient"},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="patient_allergies",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="المريض",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم التحديث بواسطة",
                    ),
                ),
            ],
            options={
                "verbose_name": "حساسية",
                "verbose_name_plural": "الحساسيات",
                "ordering": ["-diagnosis_date"],
                "unique_together": {("patient", "allergen")},
            },
        ),
        migrations.CreateModel(
            name="AllergyReaction",
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
                ("reaction", models.CharField(max_length=200, verbose_name="رد الفعل")),
                ("notes", models.TextField(blank=True, verbose_name="ملاحظات")),
                (
                    "allergy",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reactions",
                        to="medical_records.allergy",
                        verbose_name="الحساسية",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="HealthGoal",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("weight", "الوزن"),
                            ("exercise", "التمارين"),
                            ("diet", "النظام الغذائي"),
                            ("blood_pressure", "ضغط الدم"),
                            ("blood_sugar", "سكر الدم"),
                            ("other", "أخرى"),
                        ],
                        max_length=20,
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                (
                    "target_value",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=8, null=True
                    ),
                ),
                ("start_date", models.DateField()),
                ("target_date", models.DateField()),
                ("achieved", models.BooleanField(default=False)),
                ("achieved_date", models.DateField(blank=True, null=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.patient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="LabResult",
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
                ("test_name", models.CharField(max_length=200)),
                ("test_date", models.DateField()),
                ("result_value", models.CharField(max_length=100)),
                ("normal_range", models.CharField(max_length=100)),
                ("is_normal", models.BooleanField()),
                ("lab_name", models.CharField(max_length=200)),
                (
                    "file",
                    models.FileField(blank=True, null=True, upload_to="lab_results/"),
                ),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "doctor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="accounts.doctor",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.patient",
                    ),
                ),
            ],
            options={
                "ordering": ["-test_date"],
            },
        ),
        migrations.CreateModel(
            name="MedicalRecord",
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
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="محذوف"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاريخ الحذف"
                    ),
                ),
                (
                    "blood_type",
                    models.CharField(
                        choices=[
                            ("A+", "A+"),
                            ("A-", "A-"),
                            ("B+", "B+"),
                            ("B-", "B-"),
                            ("O+", "O+"),
                            ("O-", "O-"),
                            ("AB+", "AB+"),
                            ("AB-", "AB-"),
                        ],
                        max_length=5,
                    ),
                ),
                (
                    "height",
                    models.DecimalField(
                        decimal_places=2, help_text="بالسنتيمتر", max_digits=5
                    ),
                ),
                (
                    "weight",
                    models.DecimalField(
                        decimal_places=2, help_text="بالكيلوغرام", max_digits=5
                    ),
                ),
                ("allergies", models.TextField(blank=True)),
                ("chronic_conditions", models.TextField(blank=True)),
                ("family_history", models.TextField(blank=True)),
                ("emergency_contact", models.CharField(max_length=100)),
                ("emergency_phone", models.CharField(max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "record_type",
                    models.CharField(
                        choices=[
                            ("diagnosis", "تشخيص"),
                            ("prescription", "وصفة طبية"),
                            ("lab_test", "تحليل مخبري"),
                            ("radiology", "صورة شعاعية"),
                            ("surgery", "عملية جراحية"),
                            ("vaccination", "تطعيم"),
                            ("allergy", "حساسية"),
                            ("chronic_condition", "حالة مزمنة"),
                        ],
                        max_length=20,
                        verbose_name="نوع السجل",
                    ),
                ),
                ("title", models.CharField(max_length=200, verbose_name="العنوان")),
                ("description", models.TextField(verbose_name="الوصف")),
                (
                    "date",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="التاريخ"
                    ),
                ),
                (
                    "severity",
                    models.CharField(
                        choices=[
                            ("low", "منخفضة"),
                            ("medium", "متوسطة"),
                            ("high", "عالية"),
                            ("critical", "حرجة"),
                        ],
                        default="low",
                        max_length=10,
                        verbose_name="مستوى الخطورة",
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="ملاحظات")),
                (
                    "attachments",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="medical_records/",
                        verbose_name="المرفقات",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الإنشاء بواسطة",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الحذف بواسطة",
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="doctor_records",
                        to="accounts.doctor",
                        verbose_name="الطبيب",
                    ),
                ),
                (
                    "patient",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.patient",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم التحديث بواسطة",
                    ),
                ),
            ],
            options={
                "verbose_name": "سجل طبي",
                "verbose_name_plural": "السجلات الطبية",
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Medication",
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
                ("name", models.CharField(max_length=200)),
                ("dosage", models.CharField(max_length=100)),
                (
                    "frequency",
                    models.CharField(
                        choices=[
                            ("daily", "يومياً"),
                            ("twice_daily", "مرتين يومياً"),
                            ("three_times", "ثلاث مرات يومياً"),
                            ("four_times", "أربع مرات يومياً"),
                            ("weekly", "أسبوعياً"),
                            ("monthly", "شهرياً"),
                            ("as_needed", "عند الحاجة"),
                        ],
                        max_length=20,
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "نشط"),
                            ("completed", "مكتمل"),
                            ("discontinued", "متوقف"),
                        ],
                        default="active",
                        max_length=20,
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.patient",
                    ),
                ),
                (
                    "prescribing_doctor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="accounts.doctor",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MedicationReminder",
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
                ("time", models.TimeField()),
                ("is_taken", models.BooleanField(default=False)),
                ("taken_at", models.DateTimeField(blank=True, null=True)),
                ("skipped", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                (
                    "medication",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical_records.medication",
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
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="تاريخ الإنشاء"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="محذوف"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاريخ الحذف"
                    ),
                ),
                (
                    "medicine_name",
                    models.CharField(max_length=200, verbose_name="اسم الدواء"),
                ),
                ("dosage", models.CharField(max_length=100, verbose_name="الجرعة")),
                (
                    "frequency",
                    models.CharField(max_length=100, verbose_name="عدد مرات الأخذ"),
                ),
                (
                    "duration",
                    models.CharField(max_length=100, verbose_name="مدة العلاج"),
                ),
                ("instructions", models.TextField(blank=True, verbose_name="تعليمات")),
                (
                    "is_chronic",
                    models.BooleanField(default=False, verbose_name="دواء مزمن"),
                ),
                (
                    "refills",
                    models.PositiveIntegerField(
                        default=0, verbose_name="عدد مرات إعادة الصرف"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="ملاحظات")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الإنشاء بواسطة",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الحذف بواسطة",
                    ),
                ),
                (
                    "medical_record",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="prescriptions",
                        to="medical_records.medicalrecord",
                        verbose_name="السجل الطبي",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم التحديث بواسطة",
                    ),
                ),
            ],
            options={
                "verbose_name": "وصفة طبية",
                "verbose_name_plural": "الوصفات الطبية",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ProgressUpdate",
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
                ("date", models.DateField()),
                ("value", models.DecimalField(decimal_places=2, max_digits=8)),
                ("notes", models.TextField(blank=True)),
                (
                    "goal",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="medical_records.healthgoal",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="VitalSigns",
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
                ("date", models.DateTimeField()),
                (
                    "blood_pressure_systolic",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(300),
                        ]
                    ),
                ),
                (
                    "blood_pressure_diastolic",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(200),
                        ]
                    ),
                ),
                (
                    "heart_rate",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(250),
                        ]
                    ),
                ),
                ("temperature", models.DecimalField(decimal_places=1, max_digits=4)),
                (
                    "blood_sugar",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(1000),
                        ]
                    ),
                ),
                (
                    "oxygen_saturation",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ]
                    ),
                ),
                ("notes", models.TextField(blank=True)),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.patient",
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Appointment",
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
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="محذوف"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاريخ الحذف"
                    ),
                ),
                (
                    "appointment_type",
                    models.CharField(
                        choices=[
                            ("consultation", "استشارة"),
                            ("follow_up", "متابعة"),
                            ("emergency", "طوارئ"),
                            ("routine_check", "فحص روتيني"),
                            ("procedure", "إجراء طبي"),
                        ],
                        max_length=20,
                        verbose_name="نوع الموعد",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "قيد الانتظار"),
                            ("confirmed", "مؤكد"),
                            ("completed", "مكتمل"),
                            ("cancelled", "ملغي"),
                            ("no_show", "لم يحضر"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="حالة الموعد",
                    ),
                ),
                ("scheduled_time", models.DateTimeField(verbose_name="وقت الموعد")),
                (
                    "duration",
                    models.PositiveIntegerField(
                        default=30,
                        validators=[
                            django.core.validators.MinValueValidator(15),
                            django.core.validators.MaxValueValidator(180),
                        ],
                        verbose_name="المدة (بالدقائق)",
                    ),
                ),
                ("reason", models.TextField(verbose_name="سبب الزيارة")),
                ("notes", models.TextField(blank=True, verbose_name="ملاحظات")),
                (
                    "cancellation_reason",
                    models.TextField(blank=True, verbose_name="سبب الإلغاء"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الإنشاء بواسطة",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الحذف بواسطة",
                    ),
                ),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.doctor",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.patient",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم التحديث بواسطة",
                    ),
                ),
            ],
            options={
                "verbose_name": "موعد",
                "verbose_name_plural": "المواعيد",
                "ordering": ["-scheduled_time"],
                "indexes": [
                    models.Index(
                        fields=["doctor", "scheduled_time"],
                        name="medical_rec_doctor__59bb8d_idx",
                    ),
                    models.Index(
                        fields=["patient", "scheduled_time"],
                        name="medical_rec_patient_eed79c_idx",
                    ),
                    models.Index(
                        fields=["status", "scheduled_time"],
                        name="medical_rec_status_664a2c_idx",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="Vaccination",
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
                (
                    "created_at",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="تاريخ الإنشاء"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث"),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="محذوف"),
                ),
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="تاريخ الحذف"
                    ),
                ),
                (
                    "vaccine_type",
                    models.CharField(
                        choices=[
                            ("routine", "روتيني"),
                            ("seasonal", "موسمي"),
                            ("travel", "سفر"),
                            ("covid19", "كوفيد-19"),
                            ("other", "أخرى"),
                        ],
                        max_length=20,
                        verbose_name="نوع التطعيم",
                    ),
                ),
                (
                    "vaccine_name",
                    models.CharField(max_length=200, verbose_name="اسم التطعيم"),
                ),
                (
                    "dose_number",
                    models.PositiveIntegerField(default=1, verbose_name="رقم الجرعة"),
                ),
                ("date_given", models.DateField(verbose_name="تاريخ الأخذ")),
                (
                    "next_dose_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="تاريخ الجرعة القادمة"
                    ),
                ),
                (
                    "batch_number",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="رقم التشغيلة"
                    ),
                ),
                (
                    "manufacturer",
                    models.CharField(
                        blank=True, max_length=200, verbose_name="الشركة المصنعة"
                    ),
                ),
                ("notes", models.TextField(blank=True, verbose_name="ملاحظات")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الإنشاء بواسطة",
                    ),
                ),
                (
                    "deleted_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_deleted",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم الحذف بواسطة",
                    ),
                ),
                (
                    "given_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="administered_vaccinations",
                        to="accounts.doctor",
                        verbose_name="الطبيب المعطي",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        limit_choices_to={"user_type": "patient"},
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="patient_vaccinations",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="المريض",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="تم التحديث بواسطة",
                    ),
                ),
            ],
            options={
                "verbose_name": "تطعيم",
                "verbose_name_plural": "التطعيمات",
                "ordering": ["-date_given"],
                "unique_together": {("patient", "vaccine_type", "dose_number")},
            },
        ),
    ]