from datetime import datetime
from typing import Any, Dict, List, Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.exceptions import ValidationError
from django.db import models

from ..models import Doctor, EmergencyCase, Hospital


class CommunicationService:
    def __init__(self):
        self.channel_layer = get_channel_layer()

    def broadcast_emergency_alert(
        self,
        hospital_id: int,
        message: str,
        severity: str,
        required_resources: Dict[str, Any],
    ):
        """
        Broadcast emergency alert to nearby hospitals.
        """
        hospital = Hospital.objects.get(id=hospital_id)
        nearby_hospitals = Hospital.objects.filter(city=hospital.city).exclude(
            id=hospital_id
        )

        alert_data = {
            "type": "emergency_alert",
            "hospital_name": hospital.name,
            "message": message,
            "severity": severity,
            "required_resources": required_resources,
            "timestamp": datetime.now().isoformat(),
        }

        # Broadcast to all nearby hospitals
        async_to_sync(self.channel_layer.group_send)(
            f"hospital_{hospital.city}",
            {"type": "emergency_alert", "message": alert_data},
        )

        return alert_data

    def send_resource_request(
        self,
        from_hospital_id: int,
        to_hospital_id: int,
        resources: List[Dict[str, Any]],
        priority: str,
    ):
        """
        Send resource request to another hospital.
        """
        from_hospital = Hospital.objects.get(id=from_hospital_id)
        to_hospital = Hospital.objects.get(id=to_hospital_id)

        request_data = {
            "type": "resource_request",
            "from_hospital": from_hospital.name,
            "resources": resources,
            "priority": priority,
            "timestamp": datetime.now().isoformat(),
        }

        # Send to specific hospital
        async_to_sync(self.channel_layer.group_send)(
            f"hospital_{to_hospital_id}",
            {"type": "resource_request", "message": request_data},
        )

        return request_data

    def start_emergency_conference(
        self, hospital_id: int, emergency_case_id: int, participant_ids: List[int]
    ):
        """
        Start video conference for emergency consultation.
        """
        emergency = EmergencyCase.objects.get(id=emergency_case_id)
        participants = Doctor.objects.filter(id__in=participant_ids)

        conference_data = {
            "type": "emergency_conference",
            "emergency_id": emergency_case_id,
            "hospital_id": hospital_id,
            "patient_condition": emergency.condition,
            "priority": emergency.priority,
            "participants": [
                {
                    "id": doc.id,
                    "name": doc.name,
                    "specialty": doc.specialty,
                    "hospital": doc.hospital.name,
                }
                for doc in participants
            ],
            "timestamp": datetime.now().isoformat(),
        }

        # Create conference room
        room_id = f"emergency_{emergency_case_id}"

        # Notify all participants
        for doctor in participants:
            async_to_sync(self.channel_layer.group_send)(
                f"doctor_{doctor.id}",
                {
                    "type": "conference_invitation",
                    "message": {**conference_data, "room_id": room_id},
                },
            )

        return {"room_id": room_id, "conference_data": conference_data}

    def send_status_update(
        self, hospital_id: int, update_type: str, data: Dict[str, Any]
    ):
        """
        Send real-time status update to central system.
        """
        hospital = Hospital.objects.get(id=hospital_id)

        update_data = {
            "type": update_type,
            "hospital_id": hospital_id,
            "hospital_name": hospital.name,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }

        # Send to central monitoring
        async_to_sync(self.channel_layer.group_send)(
            "central_monitoring", {"type": "status_update", "message": update_data}
        )

        return update_data

    def request_ambulance_dispatch(
        self,
        hospital_id: int,
        location: Dict[str, float],
        priority: str,
        patient_condition: str,
    ):
        """
        Request ambulance dispatch to location.
        """
        hospital = Hospital.objects.get(id=hospital_id)

        dispatch_data = {
            "type": "ambulance_dispatch",
            "hospital_id": hospital_id,
            "hospital_name": hospital.name,
            "location": location,
            "priority": priority,
            "patient_condition": patient_condition,
            "timestamp": datetime.now().isoformat(),
        }

        # Send to ambulance dispatch center
        async_to_sync(self.channel_layer.group_send)(
            "ambulance_dispatch", {"type": "dispatch_request", "message": dispatch_data}
        )

        return dispatch_data
