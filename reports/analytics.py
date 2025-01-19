"""
خدمات التحليلات المتقدمة
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from django.db.models import Avg, Count, Max, Min
from django.utils import timezone
from scipy import stats
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from .models import HealthMetric, MedicalReport, TreatmentProgress


class AdvancedAnalytics:
    """خدمة التحليلات المتقدمة"""

    @staticmethod
    def analyze_treatment_patterns(diagnosis, min_samples=50):
        """تحليل أنماط العلاج"""
        reports = MedicalReport.objects.filter(diagnosis__icontains=diagnosis).values(
            "treatment_plan", "medications"
        )

        if reports.count() < min_samples:
            return None

        # تحويل البيانات إلى DataFrame
        df = pd.DataFrame(reports)

        # تحليل خطط العلاج
        treatment_words = " ".join(df["treatment_plan"]).split()
        treatment_freq = pd.Series(treatment_words).value_counts()

        # تحليل الأدوية
        medication_words = " ".join(df["medications"]).split()
        medication_freq = pd.Series(medication_words).value_counts()

        # تحليل الارتباطات
        common_combinations = []
        for i, med1 in enumerate(medication_freq.head(10).index):
            for med2 in medication_freq.head(10).index[i + 1 :]:
                coexistence = sum(
                    1 for meds in df["medications"] if med1 in meds and med2 in meds
                )
                if coexistence > 0:
                    common_combinations.append(
                        {"medications": [med1, med2], "count": coexistence}
                    )

        return {
            "common_treatments": treatment_freq.head(10).to_dict(),
            "common_medications": medication_freq.head(10).to_dict(),
            "medication_combinations": sorted(
                common_combinations, key=lambda x: x["count"], reverse=True
            )[:5],
        }

    @staticmethod
    def analyze_recovery_patterns(metric_type, condition):
        """تحليل أنماط التعافي"""
        metrics = (
            HealthMetric.objects.filter(
                metric_type=metric_type,
                patient__medicalreport__diagnosis__icontains=condition,
            )
            .values("patient_id", "value", "measured_at")
            .order_by("patient_id", "measured_at")
        )

        df = pd.DataFrame(metrics)
        if df.empty:
            return None

        # تحويل البيانات إلى سلاسل زمنية
        df["measured_at"] = pd.to_datetime(df["measured_at"])
        patients_data = {}

        for patient_id in df["patient_id"].unique():
            patient_metrics = df[df["patient_id"] == patient_id]
            if len(patient_metrics) >= 5:  # نحتاج على الأقل 5 قياسات
                patients_data[patient_id] = {
                    "values": patient_metrics["value"].values,
                    "times": patient_metrics["measured_at"].values,
                }

        if not patients_data:
            return None

        # تحليل النمط لكل مريض
        patterns = []
        for patient_id, data in patients_data.items():
            values = data["values"]
            times = data["times"]

            # حساب معدل التغيير
            changes = np.diff(values)
            avg_change = np.mean(changes)

            # تحديد نمط التعافي
            if avg_change < 0:
                pattern = "decreasing"  # تحسن (للقيم التي يفضل انخفاضها)
            elif avg_change > 0:
                pattern = "increasing"  # تحسن (للقيم التي يفضل ارتفاعها)
            else:
                pattern = "stable"

            # حساب سرعة التغيير
            time_diffs = np.diff(times) / np.timedelta64(1, "D")
            change_rate = np.mean(changes / time_diffs)

            patterns.append(
                {
                    "patient_id": patient_id,
                    "pattern": pattern,
                    "avg_change": float(avg_change),
                    "change_rate": float(change_rate),
                    "duration_days": (times[-1] - times[0]).days,
                }
            )

        # تحليل إحصائي للأنماط
        pattern_counts = pd.DataFrame(patterns)["pattern"].value_counts()
        avg_duration = np.mean([p["duration_days"] for p in patterns])

        return {
            "patterns_distribution": pattern_counts.to_dict(),
            "average_recovery_duration": avg_duration,
            "detailed_patterns": patterns,
            "summary": {
                "total_patients": len(patterns),
                "improving_ratio": float(
                    pattern_counts.get("decreasing", 0) / len(patterns)
                    if len(patterns) > 0
                    else 0
                ),
            },
        }

    @staticmethod
    def predict_appointment_load(days_ahead=30):
        """التنبؤ بحمل المواعيد"""
        # جمع بيانات المواعيد السابقة
        end_date = timezone.now()
        start_date = end_date - timedelta(days=90)  # 90 يوم للتحليل

        appointments = (
            Appointment.objects.filter(date__range=(start_date, end_date))
            .values("date")
            .annotate(count=Count("id"))
        )

        df = pd.DataFrame(appointments)
        if df.empty:
            return None

        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

        # إكمال الأيام المفقودة بأصفار
        idx = pd.date_range(start_date, end_date)
        df = df.reindex(idx, fill_value=0)

        # حساب المتوسطات المتحركة
        df["ma7"] = df["count"].rolling(window=7).mean()  # متوسط 7 أيام
        df["ma30"] = df["count"].rolling(window=30).mean()  # متوسط 30 يوم

        # تحليل الاتجاه
        X = np.arange(len(df)).reshape(-1, 1)
        y = df["count"].values

        from sklearn.linear_model import LinearRegression

        model = LinearRegression()
        model.fit(X, y)

        # التنبؤ للأيام القادمة
        future_dates = pd.date_range(
            end_date + timedelta(days=1), end_date + timedelta(days=days_ahead)
        )
        future_X = np.arange(len(df), len(df) + days_ahead).reshape(-1, 1)
        predictions = model.predict(future_X)

        # تحليل النمط الأسبوعي
        df["weekday"] = df.index.weekday
        weekly_pattern = df.groupby("weekday")["count"].mean()

        # تعديل التنبؤات بناءً على النمط الأسبوعي
        for i, date in enumerate(future_dates):
            weekday = date.weekday()
            predictions[i] *= weekly_pattern[weekday] / weekly_pattern.mean()

        return {
            "predictions": {
                date.strftime("%Y-%m-%d"): max(0, round(pred))
                for date, pred in zip(future_dates, predictions)
            },
            "weekly_pattern": weekly_pattern.to_dict(),
            "trend": {
                "slope": float(model.coef_[0]),
                "intercept": float(model.intercept_),
            },
            "current_load": {
                "daily_average": float(df["count"].mean()),
                "weekly_average": float(df["ma7"].iloc[-1]),
                "monthly_average": float(df["ma30"].iloc[-1]),
            },
        }

    @staticmethod
    def analyze_patient_segments(min_metrics=3):
        """تحليل شرائح المرضى"""
        # جمع البيانات
        patients_data = []
        for patient in Patient.objects.all():
            metrics = HealthMetric.objects.filter(patient=patient)
            appointments = Appointment.objects.filter(patient=patient)
            reports = MedicalReport.objects.filter(patient=patient)

            if metrics.count() >= min_metrics:
                patients_data.append(
                    {
                        "patient_id": patient.id,
                        "age": patient.age,
                        "gender": patient.gender,
                        "visit_frequency": appointments.count(),
                        "avg_visit_duration": appointments.aggregate(Avg("duration"))[
                            "duration__avg"
                        ]
                        or 0,
                        "conditions_count": reports.values("diagnosis")
                        .distinct()
                        .count(),
                        "metrics_count": metrics.count(),
                        "last_visit": appointments.aggregate(Max("date"))["date__max"],
                    }
                )

        if not patients_data:
            return None

        df = pd.DataFrame(patients_data)

        # تحضير البيانات للتحليل
        features = ["age", "visit_frequency", "avg_visit_duration", "conditions_count"]
        X = df[features]

        # تطبيع البيانات
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # تحليل المكونات الرئيسية
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)

        # التجميع
        kmeans = KMeans(n_clusters=3, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)

        # تحليل الشرائح
        segments = []
        for i in range(3):
            segment_data = df[clusters == i]
            segments.append(
                {
                    "size": len(segment_data),
                    "avg_age": float(segment_data["age"].mean()),
                    "avg_visits": float(segment_data["visit_frequency"].mean()),
                    "avg_conditions": float(segment_data["conditions_count"].mean()),
                    "characteristics": {
                        "age_range": f"{segment_data['age'].min()}-{segment_data['age'].max()}",
                        "visit_pattern": (
                            "frequent"
                            if segment_data["visit_frequency"].mean()
                            > df["visit_frequency"].mean()
                            else "infrequent"
                        ),
                        "complexity": (
                            "high"
                            if segment_data["conditions_count"].mean()
                            > df["conditions_count"].mean()
                            else "low"
                        ),
                    },
                }
            )

        return {
            "segments": segments,
            "total_patients": len(df),
            "feature_importance": dict(zip(features, abs(pca.components_[0]))),
            "visualization_data": {
                "x": X_pca[:, 0].tolist(),
                "y": X_pca[:, 1].tolist(),
                "clusters": clusters.tolist(),
            },
        }
