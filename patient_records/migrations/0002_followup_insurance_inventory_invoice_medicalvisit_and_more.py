# Generated by Django 4.2.18 on 2025-01-19 10:33

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patient_records', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('priority', models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('urgent', 'Urgent')], default='medium', max_length=10, verbose_name='Priority')),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('missed', 'Missed')], default='scheduled', max_length=20, verbose_name='Status')),
                ('scheduled_date', models.DateTimeField(verbose_name='Scheduled Date')),
                ('actual_date', models.DateTimeField(blank=True, null=True, verbose_name='Actual Date')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('reminder_sent', models.BooleanField(default=False, verbose_name='Reminder Sent')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='doctor_follow_ups', to=settings.AUTH_USER_MODEL, verbose_name='Doctor')),
            ],
            options={
                'verbose_name': 'Follow Up',
                'verbose_name_plural': 'Follow Ups',
                'ordering': ['-scheduled_date'],
            },
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=100, verbose_name='Insurance Provider')),
                ('policy_number', models.CharField(max_length=50, unique=True, verbose_name='Policy Number')),
                ('coverage_type', models.CharField(choices=[('full', 'Full Coverage'), ('partial', 'Partial Coverage'), ('basic', 'Basic Coverage')], max_length=20, verbose_name='Coverage Type')),
                ('coverage_percentage', models.DecimalField(decimal_places=2, help_text='Coverage percentage (0-100)', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Coverage Percentage')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive'), ('expired', 'Expired'), ('pending', 'Pending Approval')], default='pending', max_length=20, verbose_name='Status')),
                ('deductible', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Deductible Amount')),
                ('max_coverage', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Maximum Coverage Amount')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Insurance',
                'verbose_name_plural': 'Insurances',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_number', models.CharField(max_length=100, verbose_name='Batch Number')),
                ('expiry_date', models.DateField(verbose_name='Expiry Date')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('reorder_level', models.PositiveIntegerField(verbose_name='Reorder Level')),
                ('location', models.CharField(max_length=100, verbose_name='Storage Location')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Inventory',
                'verbose_name_plural': 'Inventory Items',
                'ordering': ['medication__name'],
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=50, unique=True, verbose_name='Invoice Number')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('pending', 'Pending'), ('paid', 'Paid'), ('overdue', 'Overdue'), ('cancelled', 'Cancelled')], default='draft', max_length=20, verbose_name='Status')),
                ('issue_date', models.DateField(verbose_name='Issue Date')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('bank_transfer', 'Bank Transfer'), ('insurance', 'Insurance')], max_length=20, verbose_name='Payment Method')),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Subtotal')),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tax')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Discount')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'ordering': ['-issue_date'],
            },
        ),
        migrations.CreateModel(
            name='MedicalVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_type', models.CharField(choices=[('regular', 'Regular Check-up'), ('emergency', 'Emergency'), ('follow_up', 'Follow-up'), ('consultation', 'Consultation')], max_length=20, verbose_name='Visit Type')),
                ('visit_date', models.DateTimeField(verbose_name='Visit Date')),
                ('symptoms', models.TextField(verbose_name='Symptoms')),
                ('diagnosis', models.TextField(verbose_name='Diagnosis')),
                ('treatment', models.TextField(verbose_name='Treatment')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('follow_up_date', models.DateField(blank=True, null=True, verbose_name='Follow-up Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_visits', to=settings.AUTH_USER_MODEL, verbose_name='Doctor')),
            ],
            options={
                'verbose_name': 'Medical Visit',
                'verbose_name_plural': 'Medical Visits',
                'ordering': ['-visit_date'],
            },
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('generic_name', models.CharField(max_length=255, verbose_name='Generic Name')),
                ('manufacturer', models.CharField(max_length=255, verbose_name='Manufacturer')),
                ('description', models.TextField(verbose_name='Description')),
                ('dosage_form', models.CharField(max_length=100, verbose_name='Dosage Form')),
                ('strength', models.CharField(max_length=100, verbose_name='Strength')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('requires_prescription', models.BooleanField(default=True, verbose_name='Requires Prescription')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Medication',
                'verbose_name_plural': 'Medications',
                'ordering': ['name'],
            },
        ),
        migrations.AlterModelOptions(
            name='patient',
            options={'ordering': ['user__last_name', 'user__first_name'], 'verbose_name': 'Patient', 'verbose_name_plural': 'Patients'},
        ),
        migrations.RemoveField(
            model_name='patient',
            name='allergies',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='blood_type',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='chronic_conditions',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='emergency_contact',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='emergency_phone',
        ),
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.TextField(default='', verbose_name='Address'),
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_name',
            field=models.CharField(default='', max_length=255, verbose_name='Emergency Contact Name'),
        ),
        migrations.AddField(
            model_name='patient',
            name='emergency_contact_phone',
            field=models.CharField(default='', max_length=20, verbose_name='Emergency Contact Phone'),
        ),
        migrations.AddField(
            model_name='patient',
            name='marital_status',
            field=models.CharField(choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], default='single', max_length=10, verbose_name='Marital Status'),
        ),
        migrations.AddField(
            model_name='patient',
            name='notes',
            field=models.TextField(blank=True, verbose_name='Notes'),
        ),
        migrations.AddField(
            model_name='patient',
            name='occupation',
            field=models.CharField(blank=True, max_length=100, verbose_name='Occupation'),
        ),
        migrations.AddField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(default='', max_length=20, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created At'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1, verbose_name='Gender'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Updated At'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_profile', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='Vaccination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccine_name', models.CharField(max_length=255, verbose_name='Vaccine Name')),
                ('dose_number', models.PositiveIntegerField(verbose_name='Dose Number')),
                ('date_given', models.DateTimeField(verbose_name='Date Given')),
                ('next_due_date', models.DateField(blank=True, null=True, verbose_name='Next Due Date')),
                ('batch_number', models.CharField(max_length=100, verbose_name='Batch Number')),
                ('manufacturer', models.CharField(max_length=255, verbose_name='Manufacturer')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('administered_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='administered_vaccines', to=settings.AUTH_USER_MODEL, verbose_name='Administered By')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vaccinations', to='patient_records.patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Vaccination',
                'verbose_name_plural': 'Vaccinations',
                'ordering': ['-date_given'],
            },
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment_type', models.CharField(choices=[('medication', 'Medication'), ('therapy', 'Therapy'), ('surgery', 'Surgery'), ('procedure', 'Medical Procedure'), ('diet', 'Diet Plan'), ('exercise', 'Exercise Plan')], max_length=20, verbose_name='Treatment Type')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('frequency', models.CharField(choices=[('once', 'Once'), ('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('as_needed', 'As Needed')], max_length=20, verbose_name='Frequency')),
                ('duration', models.CharField(max_length=100, verbose_name='Duration')),
                ('instructions', models.TextField(verbose_name='Instructions')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='End Date')),
                ('is_completed', models.BooleanField(default=False, verbose_name='Is Completed')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('follow_up', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='treatments', to='patient_records.followup', verbose_name='Follow Up')),
            ],
            options={
                'verbose_name': 'Treatment',
                'verbose_name_plural': 'Treatments',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Radiology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('radiology_type', models.CharField(choices=[('xray', 'X-Ray'), ('ct', 'CT Scan'), ('mri', 'MRI'), ('ultrasound', 'Ultrasound'), ('other', 'Other')], max_length=20, verbose_name='Radiology Type')),
                ('body_part', models.CharField(max_length=100, verbose_name='Body Part')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('image', models.ImageField(upload_to='radiology/', verbose_name='Image')),
                ('report', models.TextField(blank=True, verbose_name='Report')),
                ('performed_at', models.DateTimeField(verbose_name='Performed At')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='radiology_tests', to='patient_records.medicalvisit', verbose_name='Medical Visit')),
            ],
            options={
                'verbose_name': 'Radiology',
                'verbose_name_plural': 'Radiology Tests',
                'ordering': ['-performed_at'],
            },
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Date')),
                ('status', models.TextField(verbose_name='Status')),
                ('observations', models.TextField(verbose_name='Observations')),
                ('complications', models.TextField(blank=True, verbose_name='Complications')),
                ('next_steps', models.TextField(verbose_name='Next Steps')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('recorded_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recorded_progress', to=settings.AUTH_USER_MODEL, verbose_name='Recorded By')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='progress_records', to='patient_records.treatment', verbose_name='Treatment')),
            ],
            options={
                'verbose_name': 'Progress',
                'verbose_name_plural': 'Progress Records',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication_name', models.CharField(max_length=255, verbose_name='Medication Name')),
                ('dosage', models.CharField(max_length=100, verbose_name='Dosage')),
                ('frequency', models.CharField(max_length=100, verbose_name='Frequency')),
                ('duration', models.CharField(max_length=100, verbose_name='Duration')),
                ('instructions', models.TextField(blank=True, verbose_name='Special Instructions')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('expiry_date', models.DateField(blank=True, null=True, verbose_name='Expiry Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prescriptions', to='patient_records.medicalvisit', verbose_name='Medical Visit')),
            ],
            options={
                'verbose_name': 'Prescription',
                'verbose_name_plural': 'Prescriptions',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount')),
                ('payment_method', models.CharField(choices=[('cash', 'Cash'), ('credit_card', 'Credit Card'), ('debit_card', 'Debit Card'), ('bank_transfer', 'Bank Transfer'), ('insurance', 'Insurance')], max_length=20, verbose_name='Payment Method')),
                ('transaction_id', models.CharField(blank=True, max_length=100, verbose_name='Transaction ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=20, verbose_name='Status')),
                ('payment_date', models.DateTimeField(verbose_name='Payment Date')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='patient_records.invoice', verbose_name='Invoice')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
                'ordering': ['-payment_date'],
            },
        ),
        migrations.AddField(
            model_name='medicalvisit',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_visits', to='patient_records.patient', verbose_name='Patient'),
        ),
        migrations.CreateModel(
            name='MedicalReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('general', 'General Report'), ('specialist', 'Specialist Report'), ('lab', 'Laboratory Report'), ('radiology', 'Radiology Report'), ('surgery', 'Surgery Report'), ('discharge', 'Discharge Report')], max_length=20, verbose_name='Report Type')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('content', models.TextField(verbose_name='Content')),
                ('diagnosis', models.TextField(verbose_name='Diagnosis')),
                ('recommendations', models.TextField(verbose_name='Recommendations')),
                ('is_confidential', models.BooleanField(default=False, verbose_name='Is Confidential')),
                ('attachments', models.FileField(blank=True, null=True, upload_to='reports/', verbose_name='Attachments')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authored_reports', to=settings.AUTH_USER_MODEL, verbose_name='Doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medical_reports', to='patient_records.patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Medical Report',
                'verbose_name_plural': 'Medical Reports',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MedicalRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_type', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'), ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3, verbose_name='Blood Type')),
                ('height', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(300)], verbose_name='Height (cm)')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(500)], verbose_name='Weight (kg)')),
                ('allergies', models.TextField(blank=True, verbose_name='Allergies')),
                ('chronic_conditions', models.TextField(blank=True, verbose_name='Chronic Conditions')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='medical_record', to='patient_records.patient', verbose_name='Patient')),
            ],
            options={
                'verbose_name': 'Medical Record',
                'verbose_name_plural': 'Medical Records',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='LabTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=255, verbose_name='Test Name')),
                ('description', models.TextField(verbose_name='Description')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20, verbose_name='Status')),
                ('results', models.TextField(blank=True, verbose_name='Results')),
                ('test_date', models.DateTimeField(verbose_name='Test Date')),
                ('results_date', models.DateTimeField(blank=True, null=True, verbose_name='Results Date')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('visit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab_tests', to='patient_records.medicalvisit', verbose_name='Medical Visit')),
            ],
            options={
                'verbose_name': 'Lab Test',
                'verbose_name_plural': 'Lab Tests',
                'ordering': ['-test_date'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255, verbose_name='Description')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantity')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Unit Price')),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Total')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='patient_records.invoice', verbose_name='Invoice')),
            ],
            options={
                'verbose_name': 'Invoice Item',
                'verbose_name_plural': 'Invoice Items',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='medical_invoices', to='patient_records.patient', verbose_name='Patient'),
        ),
        migrations.CreateModel(
            name='InventoryTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('in', 'Stock In'), ('out', 'Stock Out'), ('return', 'Return'), ('adjustment', 'Adjustment')], max_length=20, verbose_name='Transaction Type')),
                ('quantity', models.IntegerField(verbose_name='Quantity')),
                ('reference', models.CharField(blank=True, max_length=255, verbose_name='Reference')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='patient_records.inventory', verbose_name='Inventory')),
                ('performed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_record_transactions', to=settings.AUTH_USER_MODEL, verbose_name='Performed By')),
            ],
            options={
                'verbose_name': 'Inventory Transaction',
                'verbose_name_plural': 'Inventory Transactions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddField(
            model_name='inventory',
            name='medication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='patient_records.medication', verbose_name='Medication'),
        ),
        migrations.CreateModel(
            name='InsuranceClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_number', models.CharField(max_length=50, unique=True, verbose_name='Claim Number')),
                ('submission_date', models.DateField(verbose_name='Submission Date')),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('processing', 'Processing'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('paid', 'Paid')], default='submitted', max_length=20, verbose_name='Status')),
                ('amount_claimed', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount Claimed')),
                ('amount_approved', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount Approved')),
                ('rejection_reason', models.TextField(blank=True, verbose_name='Rejection Reason')),
                ('documents', models.FileField(blank=True, upload_to='insurance_claims/', verbose_name='Supporting Documents')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('processed_date', models.DateField(blank=True, null=True, verbose_name='Processed Date')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='Payment Date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('insurance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='claims', to='patient_records.insurance', verbose_name='Insurance')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='insurance_claims', to='patient_records.invoice', verbose_name='Invoice')),
            ],
            options={
                'verbose_name': 'Insurance Claim',
                'verbose_name_plural': 'Insurance Claims',
                'ordering': ['-submission_date'],
            },
        ),
        migrations.AddField(
            model_name='insurance',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='insurances', to='patient_records.patient', verbose_name='Patient'),
        ),
        migrations.AddField(
            model_name='followup',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follow_ups', to='patient_records.patient', verbose_name='Patient'),
        ),
    ]
