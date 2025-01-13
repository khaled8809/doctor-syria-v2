from datetime import datetime
from typing import Any, Dict, List, Optional

from django.core.exceptions import ValidationError
from django.db import models, transaction
from geopy.distance import geodesic

from ..models import EmergencyCase, Hospital


class AmbulanceService:
    def get_nearest_ambulances(
        self, location: Dict[str, float], count: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Find nearest available ambulances to a location.
        """
        # In a real implementation, this would query a real-time ambulance tracking system
        available_ambulances = self._get_available_ambulances()

        # Calculate distances
        for ambulance in available_ambulances:
            distance = geodesic(
                (location["latitude"], location["longitude"]),
                (ambulance["location"]["latitude"], ambulance["location"]["longitude"]),
            ).kilometers
            ambulance["distance"] = distance

        # Sort by distance and return nearest
        return sorted(available_ambulances, key=lambda x: x["distance"])[:count]

    def dispatch_ambulance(
        self,
        ambulance_id: str,
        destination: Dict[str, float],
        emergency_case_id: int,
        priority: str,
    ) -> Dict[str, Any]:
        """
        Dispatch an ambulance to a location.
        """
        ambulance = self._get_ambulance(ambulance_id)
        if not ambulance["available"]:
            raise ValidationError("Ambulance is not available")

        dispatch_data = {
            "ambulance_id": ambulance_id,
            "emergency_case_id": emergency_case_id,
            "destination": destination,
            "priority": priority,
            "dispatch_time": datetime.now(),
            "estimated_arrival": self._calculate_eta(
                ambulance["location"], destination
            ),
        }

        # Update ambulance status
        self._update_ambulance_status(ambulance_id, "dispatched", dispatch_data)

        return dispatch_data

    def track_ambulance(self, ambulance_id: str) -> Dict[str, Any]:
        """
        Get real-time tracking information for an ambulance.
        """
        ambulance = self._get_ambulance(ambulance_id)

        return {
            "ambulance_id": ambulance_id,
            "location": ambulance["location"],
            "status": ambulance["status"],
            "current_task": ambulance.get("current_task"),
            "eta": ambulance.get("eta"),
            "last_updated": datetime.now(),
        }

    def update_ambulance_location(
        self,
        ambulance_id: str,
        location: Dict[str, float],
        status_update: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update ambulance location and status.
        """
        ambulance = self._get_ambulance(ambulance_id)

        # Update location
        ambulance["location"] = location

        # Update status if provided
        if status_update:
            ambulance["status"] = status_update.get("status", ambulance["status"])
            if "eta" in status_update:
                ambulance["eta"] = status_update["eta"]

        # Save updates
        self._update_ambulance_status(
            ambulance_id,
            ambulance["status"],
            {
                "location": location,
                "last_updated": datetime.now(),
                **(status_update or {}),
            },
        )

        return ambulance

    def complete_ambulance_task(
        self, ambulance_id: str, task_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Mark an ambulance task as complete.
        """
        ambulance = self._get_ambulance(ambulance_id)

        completion_data = {
            "ambulance_id": ambulance_id,
            "task_id": task_data["task_id"],
            "completion_time": datetime.now(),
            "status": "completed",
            "notes": task_data.get("notes", ""),
            "patient_condition": task_data.get("patient_condition"),
            "hospital_id": task_data.get("hospital_id"),
        }

        # Update ambulance status to available
        self._update_ambulance_status(ambulance_id, "available", completion_data)

        return completion_data

    def get_ambulance_statistics(
        self, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get statistics about ambulance operations.
        """
        # This would query your ambulance tracking system's database
        return {
            "total_dispatches": 150,
            "average_response_time": "8.5 minutes",
            "completed_tasks": 142,
            "cancelled_tasks": 8,
            "by_priority": {"critical": 45, "urgent": 67, "non_urgent": 38},
            "by_hospital": [
                {
                    "hospital_id": 1,
                    "hospital_name": "Central Hospital",
                    "dispatches": 50,
                },
                # ... more hospitals
            ],
            "average_distance": "12.3 km",
            "busiest_hours": [
                {"hour": 9, "dispatches": 15},
                # ... more hours
            ],
        }

    def _get_available_ambulances(self) -> List[Dict[str, Any]]:
        """
        Get list of available ambulances with their current locations.
        This is a mock implementation - in reality, this would query your
        ambulance tracking system.
        """
        return [
            {
                "id": "AMB001",
                "type": "advanced_life_support",
                "available": True,
                "location": {"latitude": 33.5138, "longitude": 36.2765},
                "last_maintenance": "2025-01-01",
            },
            {
                "id": "AMB002",
                "type": "basic_life_support",
                "available": True,
                "location": {"latitude": 33.5235, "longitude": 36.2895},
                "last_maintenance": "2025-01-05",
            },
            # ... more ambulances
        ]

    def _get_ambulance(self, ambulance_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific ambulance.
        This is a mock implementation.
        """
        # This would query your ambulance tracking system
        return {
            "id": ambulance_id,
            "type": "advanced_life_support",
            "available": True,
            "location": {"latitude": 33.5138, "longitude": 36.2765},
            "status": "available",
            "last_maintenance": "2025-01-01",
        }

    def _calculate_eta(
        self, current_location: Dict[str, float], destination: Dict[str, float]
    ) -> datetime:
        """
        Calculate estimated time of arrival.
        This is a simplified implementation.
        """
        # Calculate distance
        distance = geodesic(
            (current_location["latitude"], current_location["longitude"]),
            (destination["latitude"], destination["longitude"]),
        ).kilometers

        # Assume average speed of 50 km/h
        hours = distance / 50

        return datetime.now() + timedelta(hours=hours)

    def _update_ambulance_status(
        self, ambulance_id: str, status: str, data: Dict[str, Any]
    ):
        """
        Update ambulance status in the tracking system.
        This is a mock implementation.
        """
        # In reality, this would update your ambulance tracking system
        pass
