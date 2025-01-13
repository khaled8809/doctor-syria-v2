from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
from django.db import models
from django.db.models import Avg, Count, F, Q
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from ..models import (
    Admission,
    Department,
    Doctor,
    EmergencyCase,
    Hospital,
    Order,
    Patient,
    Product,
)


class AnalyticsService:
    def get_admission_predictions(
        self, hospital_id: int, days_ahead: int = 7
    ) -> Dict[str, Any]:
        """
        Predict admission rates for the next period.
        """
        # Get historical data
        historical_data = (
            Admission.objects.filter(
                hospital_id=hospital_id,
                admission_date__gte=datetime.now() - timedelta(days=90),
            )
            .values("admission_date")
            .annotate(count=Count("id"))
            .order_by("admission_date")
        )

        # Convert to pandas DataFrame
        df = pd.DataFrame(historical_data)

        # Prepare features (you might want to add more features)
        df["day_of_week"] = pd.to_datetime(df["admission_date"]).dt.dayofweek
        df["month"] = pd.to_datetime(df["admission_date"]).dt.month

        # Train model
        model = LinearRegression()
        X = df[["day_of_week", "month"]]
        y = df["count"]
        model.fit(X, y)

        # Generate predictions
        future_dates = pd.date_range(start=datetime.now(), periods=days_ahead, freq="D")
        future_features = pd.DataFrame(
            {"day_of_week": future_dates.dayofweek, "month": future_dates.month}
        )
        predictions = model.predict(future_features)

        return {
            "dates": future_dates.strftime("%Y-%m-%d").tolist(),
            "predictions": predictions.tolist(),
            "confidence_interval": self._calculate_confidence_interval(predictions),
        }

    def predict_resource_needs(
        self, hospital_id: int, days_ahead: int = 30
    ) -> Dict[str, Any]:
        """
        Predict future resource needs based on historical data and trends.
        """
        # Get historical resource usage
        resource_usage = (
            Order.objects.filter(
                hospital_id=hospital_id,
                created_at__gte=datetime.now() - timedelta(days=90),
            )
            .values("created_at", "items__product_id")
            .annotate(quantity=Sum("items__quantity"))
        )

        # Group by product
        df = pd.DataFrame(resource_usage)
        product_predictions = {}

        for product_id in df["items__product_id"].unique():
            product_data = df[df["items__product_id"] == product_id]

            # Calculate trend
            trend = self._calculate_trend(
                product_data["created_at"], product_data["quantity"]
            )

            # Predict future needs
            predicted_quantity = self._extrapolate_usage(trend, days_ahead)

            product_predictions[product_id] = {
                "predicted_quantity": predicted_quantity,
                "confidence": self._calculate_prediction_confidence(trend),
            }

        return product_predictions

    def analyze_emergency_patterns(self, hospital_id: int) -> Dict[str, Any]:
        """
        Analyze emergency case patterns to identify trends and correlations.
        """
        emergencies = EmergencyCase.objects.filter(
            hospital_id=hospital_id,
            arrival_date__gte=datetime.now() - timedelta(days=90),
        )

        # Time-based analysis
        hourly_distribution = (
            emergencies.annotate(hour=ExtractHour("arrival_date"))
            .values("hour")
            .annotate(count=Count("id"))
            .order_by("hour")
        )

        # Priority distribution
        priority_distribution = emergencies.values("priority").annotate(
            count=Count("id")
        )

        # Outcome analysis
        outcome_analysis = emergencies.values("outcome").annotate(
            count=Count("id"),
            avg_treatment_time=Avg(F("discharge_date") - F("arrival_date")),
        )

        return {
            "hourly_distribution": list(hourly_distribution),
            "priority_distribution": list(priority_distribution),
            "outcome_analysis": list(outcome_analysis),
            "patterns": self._identify_emergency_patterns(emergencies),
        }

    def get_efficiency_metrics(self, hospital_id: int) -> Dict[str, Any]:
        """
        Calculate various efficiency metrics for the hospital.
        """
        admissions = Admission.objects.filter(hospital_id=hospital_id)

        # Calculate metrics
        bed_turnover = self._calculate_bed_turnover(admissions)
        avg_length_of_stay = self._calculate_average_stay(admissions)
        resource_utilization = self._calculate_resource_utilization(hospital_id)
        staff_efficiency = self._calculate_staff_efficiency(hospital_id)

        return {
            "bed_turnover": bed_turnover,
            "average_length_of_stay": avg_length_of_stay,
            "resource_utilization": resource_utilization,
            "staff_efficiency": staff_efficiency,
            "recommendations": self._generate_efficiency_recommendations(
                bed_turnover, avg_length_of_stay, resource_utilization, staff_efficiency
            ),
        }

    def get_patient_flow_analysis(self, hospital_id: int) -> Dict[str, Any]:
        """
        Analyze patient flow through different departments.
        """
        admissions = Admission.objects.filter(hospital_id=hospital_id)

        # Department flow
        department_flow = admissions.values("department__name").annotate(
            patient_count=Count("id"),
            avg_stay=Avg(F("discharge_date") - F("admission_date")),
            transfer_rate=Count("transfers") * 100.0 / Count("id"),
        )

        # Bottleneck analysis
        bottlenecks = self._identify_bottlenecks(admissions)

        # Wait time analysis
        wait_times = self._analyze_wait_times(admissions)

        return {
            "department_flow": list(department_flow),
            "bottlenecks": bottlenecks,
            "wait_times": wait_times,
            "recommendations": self._generate_flow_recommendations(
                department_flow, bottlenecks, wait_times
            ),
        }

    def _calculate_confidence_interval(
        self, predictions: np.ndarray, confidence: float = 0.95
    ) -> List[Dict[str, float]]:
        """
        Calculate confidence intervals for predictions.
        """
        std_dev = np.std(predictions)
        z_score = 1.96  # 95% confidence interval

        return [
            {"lower": pred - (z_score * std_dev), "upper": pred + (z_score * std_dev)}
            for pred in predictions
        ]

    def _calculate_trend(self, dates: pd.Series, values: pd.Series) -> Dict[str, float]:
        """
        Calculate trend from time series data.
        """
        X = np.arange(len(dates)).reshape(-1, 1)
        y = values.values

        model = LinearRegression()
        model.fit(X, y)

        return {
            "slope": model.coef_[0],
            "intercept": model.intercept_,
            "r2_score": model.score(X, y),
        }

    def _extrapolate_usage(
        self, trend: Dict[str, float], days_ahead: int
    ) -> List[float]:
        """
        Extrapolate future usage based on trend.
        """
        X_future = np.arange(days_ahead).reshape(-1, 1)

        return trend["slope"] * X_future + trend["intercept"]

    def _calculate_prediction_confidence(self, trend: Dict[str, float]) -> float:
        """
        Calculate confidence score for predictions.
        """
        # Use R² score as base for confidence
        base_confidence = trend["r2_score"]

        # Adjust based on data quality (you'd want to add more factors)
        return min(base_confidence * 100, 100)

    def _identify_emergency_patterns(
        self, emergencies: models.QuerySet
    ) -> List[Dict[str, Any]]:
        """
        Identify patterns in emergency cases.
        """
        patterns = []

        # Time-based patterns
        time_patterns = self._analyze_time_patterns(emergencies)
        patterns.extend(time_patterns)

        # Condition patterns
        condition_patterns = self._analyze_condition_patterns(emergencies)
        patterns.extend(condition_patterns)

        return patterns

    def _calculate_bed_turnover(self, admissions: models.QuerySet) -> float:
        """
        Calculate bed turnover rate.
        """
        total_admissions = admissions.count()
        total_beds = admissions.first().hospital.bed_capacity

        return total_admissions / total_beds if total_beds > 0 else 0

    def _calculate_average_stay(self, admissions: models.QuerySet) -> float:
        """
        Calculate average length of stay.
        """
        return admissions.filter(discharge_date__isnull=False).aggregate(
            avg_stay=Avg(F("discharge_date") - F("admission_date"))
        )["avg_stay"]

    def _calculate_resource_utilization(self, hospital_id: int) -> Dict[str, float]:
        """
        Calculate resource utilization rates.
        """
        return {
            "beds": self._calculate_bed_utilization(hospital_id),
            "staff": self._calculate_staff_utilization(hospital_id),
            "equipment": self._calculate_equipment_utilization(hospital_id),
        }

    def _generate_efficiency_recommendations(
        self,
        bed_turnover: float,
        avg_length_of_stay: float,
        resource_utilization: Dict[str, float],
        staff_efficiency: Dict[str, float],
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations for improving efficiency.
        """
        recommendations = []

        # Analyze metrics and generate specific recommendations
        if bed_turnover < 0.7:
            recommendations.append(
                {
                    "type": "bed_turnover",
                    "severity": "high",
                    "message": "Bed turnover rate is below optimal levels",
                    "suggestions": [
                        "Review discharge procedures",
                        "Optimize bed allocation process",
                        "Implement better bed tracking system",
                    ],
                }
            )

        # Add more recommendations based on other metrics

        return recommendations

    def _identify_bottlenecks(
        self, admissions: models.QuerySet
    ) -> List[Dict[str, Any]]:
        """
        Identify bottlenecks in patient flow.
        """
        bottlenecks = []

        # Analyze different aspects of patient flow
        admission_bottlenecks = self._analyze_admission_bottlenecks(admissions)
        transfer_bottlenecks = self._analyze_transfer_bottlenecks(admissions)
        discharge_bottlenecks = self._analyze_discharge_bottlenecks(admissions)

        bottlenecks.extend(admission_bottlenecks)
        bottlenecks.extend(transfer_bottlenecks)
        bottlenecks.extend(discharge_bottlenecks)

        return bottlenecks
