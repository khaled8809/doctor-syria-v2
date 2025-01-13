from django.db import migrations


class Migration(migrations.Migration):
    """
    تحسينات قاعدة البيانات وإضافة الفهارس
    """

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            # إضافة فهارس للحقول الأكثر استخداماً
            sql="""
            -- فهارس للمرضى
            CREATE INDEX IF NOT EXISTS idx_patient_name ON core_patient(first_name, last_name);
            CREATE INDEX IF NOT EXISTS idx_patient_phone ON core_patient(phone_number);
            CREATE INDEX IF NOT EXISTS idx_patient_created ON core_patient(created_at);

            -- فهارس للمواعيد
            CREATE INDEX IF NOT EXISTS idx_appointment_date ON core_appointment(appointment_date);
            CREATE INDEX IF NOT EXISTS idx_appointment_status ON core_appointment(status);
            CREATE INDEX IF NOT EXISTS idx_appointment_doctor ON core_appointment(doctor_id);
            CREATE INDEX IF NOT EXISTS idx_appointment_patient ON core_appointment(patient_id);

            -- فهارس للتقارير الطبية
            CREATE INDEX IF NOT EXISTS idx_medical_report_date ON reports_medicalreport(created_at);
            CREATE INDEX IF NOT EXISTS idx_medical_report_patient ON reports_medicalreport(patient_id);
            CREATE INDEX IF NOT EXISTS idx_medical_report_doctor ON reports_medicalreport(doctor_id);
            CREATE INDEX IF NOT EXISTS idx_medical_report_diagnosis ON reports_medicalreport USING gin(diagnosis gin_trgm_ops);

            -- فهارس للمقاييس الصحية
            CREATE INDEX IF NOT EXISTS idx_health_metric_date ON reports_healthmetric(measured_at);
            CREATE INDEX IF NOT EXISTS idx_health_metric_type ON reports_healthmetric(metric_type);
            CREATE INDEX IF NOT EXISTS idx_health_metric_patient ON reports_healthmetric(patient_id);

            -- فهارس للإشعارات
            CREATE INDEX IF NOT EXISTS idx_notification_date ON notifications_notification(created_at);
            CREATE INDEX IF NOT EXISTS idx_notification_user ON notifications_notification(user_id);
            CREATE INDEX IF NOT EXISTS idx_notification_read ON notifications_notification(is_read);

            -- تحسين البحث النصي
            CREATE EXTENSION IF NOT EXISTS pg_trgm;
            CREATE INDEX IF NOT EXISTS idx_patient_search ON core_patient
            USING gin ((first_name || ' ' || last_name) gin_trgm_ops);

            -- تحسين الأداء للاستعلامات المتكررة
            CREATE MATERIALIZED VIEW IF NOT EXISTS mv_appointment_stats AS
            SELECT
                doctor_id,
                DATE_TRUNC('day', appointment_date) as day,
                COUNT(*) as total_appointments,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_appointments
            FROM core_appointment
            GROUP BY doctor_id, DATE_TRUNC('day', appointment_date);

            CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_appointment_stats
            ON mv_appointment_stats(doctor_id, day);

            -- تحسين استعلامات التقارير
            CREATE MATERIALIZED VIEW IF NOT EXISTS mv_patient_metrics AS
            SELECT
                patient_id,
                metric_type,
                DATE_TRUNC('day', measured_at) as day,
                AVG(value::numeric) as avg_value,
                MIN(value::numeric) as min_value,
                MAX(value::numeric) as max_value
            FROM reports_healthmetric
            GROUP BY patient_id, metric_type, DATE_TRUNC('day', measured_at);

            CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_patient_metrics
            ON mv_patient_metrics(patient_id, metric_type, day);
            """,
            # حذف الفهارس والجداول المؤقتة عند التراجع
            reverse_sql="""
            DROP INDEX IF EXISTS idx_patient_name;
            DROP INDEX IF EXISTS idx_patient_phone;
            DROP INDEX IF EXISTS idx_patient_created;
            DROP INDEX IF EXISTS idx_appointment_date;
            DROP INDEX IF EXISTS idx_appointment_status;
            DROP INDEX IF EXISTS idx_appointment_doctor;
            DROP INDEX IF EXISTS idx_appointment_patient;
            DROP INDEX IF EXISTS idx_medical_report_date;
            DROP INDEX IF EXISTS idx_medical_report_patient;
            DROP INDEX IF EXISTS idx_medical_report_doctor;
            DROP INDEX IF EXISTS idx_medical_report_diagnosis;
            DROP INDEX IF EXISTS idx_health_metric_date;
            DROP INDEX IF EXISTS idx_health_metric_type;
            DROP INDEX IF EXISTS idx_health_metric_patient;
            DROP INDEX IF EXISTS idx_notification_date;
            DROP INDEX IF EXISTS idx_notification_user;
            DROP INDEX IF EXISTS idx_notification_read;
            DROP INDEX IF EXISTS idx_patient_search;
            DROP MATERIALIZED VIEW IF EXISTS mv_appointment_stats;
            DROP MATERIALIZED VIEW IF EXISTS mv_patient_metrics;
            """,
        ),
        # إضافة قيود وتحسينات
        migrations.RunSQL(
            sql="""
            -- تحسين أداء الحذف
            ALTER TABLE core_appointment
            ADD CONSTRAINT fk_appointment_patient
            FOREIGN KEY (patient_id)
            REFERENCES core_patient(id)
            ON DELETE CASCADE;

            ALTER TABLE reports_medicalreport
            ADD CONSTRAINT fk_report_patient
            FOREIGN KEY (patient_id)
            REFERENCES core_patient(id)
            ON DELETE CASCADE;

            -- إضافة قيود للتحقق
            ALTER TABLE core_appointment
            ADD CONSTRAINT check_appointment_date
            CHECK (appointment_date >= created_at);

            ALTER TABLE reports_healthmetric
            ADD CONSTRAINT check_metric_value
            CHECK (value::numeric >= 0);
            """,
            reverse_sql="""
            ALTER TABLE core_appointment
            DROP CONSTRAINT IF EXISTS fk_appointment_patient;

            ALTER TABLE reports_medicalreport
            DROP CONSTRAINT IF EXISTS fk_report_patient;

            ALTER TABLE core_appointment
            DROP CONSTRAINT IF EXISTS check_appointment_date;

            ALTER TABLE reports_healthmetric
            DROP CONSTRAINT IF EXISTS check_metric_value;
            """,
        ),
    ]
