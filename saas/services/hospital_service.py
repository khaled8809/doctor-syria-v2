from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from django.core.exceptions import ValidationError
from django.db.models import Count, F, Q

from ..models import (
    Admission,
    Department,
    Doctor,
    EmergencyCase,
    Hospital,
    Patient,
    Transfer,
)


class HospitalService:
    @staticmethod
    def get_available_hospitals(
        specialty: Optional[str] = None, city: Optional[str] = None
    ) -> List[Hospital]:
        """
        Get list of hospitals with available beds, optionally filtered by specialty and city.
        """
        query = Hospital.objects.filter(available_beds__gt=0)

        if specialty:
            query = query.filter(specialties__contains=[specialty])
        if city:
            query = query.filter(city=city)

        return query.all()

    @staticmethod
    def get_hospital_capacity(hospital_id: int) -> Dict[str, Any]:
        """
        Get detailed capacity information for a hospital.
        """
        hospital = Hospital.objects.get(id=hospital_id)
        departments = Department.objects.filter(hospital=hospital)

        return {
            "total_capacity": hospital.bed_capacity,
            "available_beds": hospital.available_beds,
            "icu_units": hospital.icu_units,
            "operating_rooms": hospital.operating_rooms,
            "departments": [
                {
                    "name": dept.name,
                    "capacity": dept.capacity,
                    "available": dept.available_beds,
                }
                for dept in departments
            ],
        }

    @staticmethod
    def get_doctor_schedule(
        doctor_id: int, date: datetime
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get a doctor's schedule for a specific date.
        """
        doctor = Doctor.objects.get(id=doctor_id)
        week_day = date.strftime("%A").lower()

        return {
            "regular_hours": doctor.schedule.get(week_day, []),
            "appointments": Admission.objects.filter(
                doctor=doctor, admission_date__date=date.date()
            ).values("admission_date", "patient__name", "reason"),
        }

    @staticmethod
    def admit_patient(
        patient_id: int,
        hospital_id: int,
        department_id: int,
        doctor_id: int,
        admission_date: datetime,
        reason: str,
        diagnosis: str,
        treatment_plan: str,
    ) -> Admission:
        """
        Admit a patient to a hospital.
        """
        hospital = Hospital.objects.get(id=hospital_id)
        department = Department.objects.get(id=department_id)

        if hospital.available_beds <= 0:
            raise ValidationError("No available beds in the hospital")

        if department.available_beds <= 0:
            raise ValidationError("No available beds in the department")

        # Find available room and bed
        # This is a simplified version - in reality, you'd have a more complex room/bed management system
        room_number = f"R{department.floor}-{department.available_beds}"
        bed_number = str(department.available_beds)

        admission = Admission.objects.create(
            patient_id=patient_id,
            hospital=hospital,
            department=department,
            doctor_id=doctor_id,
            admission_date=admission_date,
            reason=reason,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan,
            room_number=room_number,
            bed_number=bed_number,
            status="ADMITTED",
        )

        # Update available beds
        hospital.available_beds = F("available_beds") - 1
        department.available_beds = F("available_beds") - 1
        hospital.save()
        department.save()

        return admission

    @staticmethod
    def discharge_patient(
        admission_id: int, discharge_date: datetime, notes: str = ""
    ) -> Admission:
        """
        Discharge a patient from the hospital.
        """
        admission = Admission.objects.get(id=admission_id)

        if admission.status != "ADMITTED":
            raise ValidationError("Patient is not currently admitted")

        admission.discharge_date = discharge_date
        admission.status = "DISCHARGED"
        admission.notes = notes
        admission.save()

        # Update available beds
        admission.hospital.available_beds = F("available_beds") + 1
        admission.department.available_beds = F("available_beds") + 1
        admission.hospital.save()
        admission.department.save()

        return admission

    @staticmethod
    def transfer_patient(
        admission_id: int,
        to_hospital_id: int,
        to_department_id: int,
        transfer_date: datetime,
        reason: str,
        approved_by_id: int,
    ) -> Transfer:
        """
        Transfer a patient to another hospital.
        """
        admission = Admission.objects.get(id=admission_id)
        to_hospital = Hospital.objects.get(id=to_hospital_id)
        to_department = Department.objects.get(id=to_department_id)

        if admission.status != "ADMITTED":
            raise ValidationError("Patient is not currently admitted")

        if to_hospital.available_beds <= 0:
            raise ValidationError("No available beds in the target hospital")

        if to_department.available_beds <= 0:
            raise ValidationError("No available beds in the target department")

        transfer = Transfer.objects.create(
            admission=admission,
            from_hospital=admission.hospital,
            to_hospital=to_hospital,
            from_department=admission.department,
            to_department=to_department,
            transfer_date=transfer_date,
            reason=reason,
            status="APPROVED",
            approved_by_id=approved_by_id,
        )

        # Update admission
        admission.status = "TRANSFERRED"
        admission.discharge_date = transfer_date
        admission.save()

        # Update beds in both hospitals
        admission.hospital.available_beds = F("available_beds") + 1
        admission.department.available_beds = F("available_beds") + 1
        to_hospital.available_beds = F("available_beds") - 1
        to_department.available_beds = F("available_beds") - 1

        admission.hospital.save()
        admission.department.save()
        to_hospital.save()
        to_department.save()

        return transfer

    @staticmethod
    def register_emergency(
        patient_id: int,
        hospital_id: int,
        condition: str,
        priority: str,
        doctor_id: int,
        initial_diagnosis: str,
        treatment: str,
    ) -> EmergencyCase:
        """
        Register a new emergency case.
        """
        return EmergencyCase.objects.create(
            patient_id=patient_id,
            hospital_id=hospital_id,
            arrival_date=datetime.now(),
            condition=condition,
            priority=priority,
            attending_doctor_id=doctor_id,
            initial_diagnosis=initial_diagnosis,
            treatment=treatment,
            outcome="ADMITTED",
        )

    @staticmethod
    def get_hospital_statistics(
        hospital_id: int, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get statistics for a hospital within a date range.
        """
        hospital = Hospital.objects.get(id=hospital_id)
        admissions = Admission.objects.filter(
            hospital=hospital, admission_date__range=(start_date, end_date)
        )
        emergency_cases = EmergencyCase.objects.filter(
            hospital=hospital, arrival_date__range=(start_date, end_date)
        )

        return {
            "total_admissions": admissions.count(),
            "current_patients": admissions.filter(status="ADMITTED").count(),
            "discharges": admissions.filter(status="DISCHARGED").count(),
            "transfers": admissions.filter(status="TRANSFERRED").count(),
            "deaths": admissions.filter(status="DECEASED").count(),
            "emergency_cases": {
                "total": emergency_cases.count(),
                "by_priority": {
                    "critical": emergency_cases.filter(priority="CRITICAL").count(),
                    "urgent": emergency_cases.filter(priority="URGENT").count(),
                    "non_urgent": emergency_cases.filter(priority="NON_URGENT").count(),
                },
                "outcomes": {
                    "admitted": emergency_cases.filter(outcome="ADMITTED").count(),
                    "discharged": emergency_cases.filter(outcome="DISCHARGED").count(),
                    "transferred": emergency_cases.filter(
                        outcome="TRANSFERRED"
                    ).count(),
                    "deceased": emergency_cases.filter(outcome="DECEASED").count(),
                },
            },
            "bed_utilization": (hospital.bed_capacity - hospital.available_beds)
            / hospital.bed_capacity
            * 100,
            "average_stay": admissions.filter(discharge_date__isnull=False)
            .annotate(stay_duration=F("discharge_date") - F("admission_date"))
            .aggregate(avg_stay=Avg("stay_duration"))["avg_stay"],
        }
