from datetime import datetime
from typing import Any, Dict, List, Optional

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F, Q

from ..models import (
    Admission,
    CartItem,
    Department,
    Doctor,
    EmergencyCase,
    Hospital,
    Order,
    Patient,
    Product,
    PurchaseOrder,
    Supply,
    Transfer,
    Warehouse,
)
from .barcode_service import BarcodeService
from .ecommerce_service import ECommerceService
from .hospital_service import HospitalService


class CentralService:
    def __init__(self):
        self.hospital_service = HospitalService()
        self.ecommerce_service = ECommerceService()
        self.barcode_service = BarcodeService()

    @transaction.atomic
    def register_patient_with_supplies(
        self,
        barcode_data: str,
        hospital_id: int,
        department_id: int,
        doctor_id: int,
        required_supplies: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Register a patient and manage required medical supplies in one transaction.
        """
        # Register patient using barcode
        patient = self.barcode_service.register_patient_from_barcode(barcode_data)
        if not patient:
            raise ValidationError("Invalid barcode data")

        # Check hospital capacity
        hospital_stats = self.hospital_service.get_hospital_capacity(hospital_id)
        if hospital_stats["available_beds"] <= 0:
            raise ValidationError("No available beds in the hospital")

        # Check supplies availability
        for supply in required_supplies:
            product = self.ecommerce_service.get_product(supply["product_id"])
            if not product or product.quantity < supply["quantity"]:
                raise ValidationError(f"Insufficient quantity for {product.name}")

        # Admit patient
        admission = self.hospital_service.admit_patient(
            patient_id=patient.id,
            hospital_id=hospital_id,
            department_id=department_id,
            doctor_id=doctor_id,
            admission_date=datetime.now(),
            reason=supply.get("reason", ""),
            diagnosis=supply.get("diagnosis", ""),
            treatment_plan=supply.get("treatment_plan", ""),
        )

        # Create order for supplies
        order = self.ecommerce_service.create_order(
            patient_id=patient.id,
            items=required_supplies,
            is_hospital_order=True,
            admission_id=admission.id,
        )

        return {"patient": patient, "admission": admission, "order": order}

    @transaction.atomic
    def handle_emergency_with_supplies(
        self,
        patient_data: Dict[str, Any],
        hospital_id: int,
        emergency_data: Dict[str, Any],
        required_supplies: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Handle emergency case and manage required supplies.
        """
        # Register or get patient
        if "barcode_data" in patient_data:
            patient = self.barcode_service.register_patient_from_barcode(
                patient_data["barcode_data"]
            )
        else:
            patient = Patient.objects.create(**patient_data)

        # Register emergency case
        emergency = self.hospital_service.register_emergency(
            patient_id=patient.id, hospital_id=hospital_id, **emergency_data
        )

        # Handle urgent supplies
        order = self.ecommerce_service.create_urgent_order(
            patient_id=patient.id,
            items=required_supplies,
            is_emergency=True,
            emergency_case_id=emergency.id,
        )

        return {"patient": patient, "emergency": emergency, "order": order}

    def transfer_patient_with_supplies(
        self,
        admission_id: int,
        to_hospital_id: int,
        to_department_id: int,
        transfer_data: Dict[str, Any],
        transfer_supplies: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Transfer patient and manage supplies transfer between hospitals.
        """
        # Initialize transfer
        transfer = self.hospital_service.transfer_patient(
            admission_id=admission_id,
            to_hospital_id=to_hospital_id,
            to_department_id=to_department_id,
            **transfer_data,
        )

        # Transfer supplies
        supply_transfer = self.ecommerce_service.transfer_supplies(
            from_hospital_id=transfer.from_hospital.id,
            to_hospital_id=transfer.to_hospital.id,
            supplies=transfer_supplies,
            transfer_id=transfer.id,
        )

        return {"transfer": transfer, "supply_transfer": supply_transfer}

    def get_hospital_inventory_status(self, hospital_id: int) -> Dict[str, Any]:
        """
        Get comprehensive inventory status for a hospital.
        """
        hospital = Hospital.objects.get(id=hospital_id)

        # Get hospital statistics
        hospital_stats = self.hospital_service.get_hospital_statistics(
            hospital_id, datetime.now().replace(hour=0, minute=0), datetime.now()
        )

        # Get inventory status
        inventory = self.ecommerce_service.get_hospital_inventory(hospital_id)

        # Get critical supplies
        critical_supplies = self.ecommerce_service.get_critical_supplies(hospital_id)

        # Get pending orders
        pending_orders = Order.objects.filter(
            hospital_id=hospital_id, status="PENDING"
        ).count()

        return {
            "hospital_stats": hospital_stats,
            "inventory": inventory,
            "critical_supplies": critical_supplies,
            "pending_orders": pending_orders,
            "bed_capacity": {
                "total": hospital.bed_capacity,
                "available": hospital.available_beds,
                "utilization": (hospital.bed_capacity - hospital.available_beds)
                / hospital.bed_capacity
                * 100,
            },
        }

    def sync_hospital_data(self, hospital_id: int) -> Dict[str, Any]:
        """
        Synchronize all data related to a hospital.
        """
        hospital = Hospital.objects.get(id=hospital_id)

        # Sync inventory with warehouses
        self.ecommerce_service.sync_hospital_inventory(hospital_id)

        # Update bed availability
        self._update_bed_availability(hospital_id)

        # Check and update doctor schedules
        self._update_doctor_schedules(hospital_id)

        # Process pending transfers
        self._process_pending_transfers(hospital_id)

        # Update emergency status
        self._update_emergency_status(hospital_id)

        return {
            "status": "success",
            "last_sync": datetime.now(),
            "hospital": hospital.name,
        }

    def _update_bed_availability(self, hospital_id: int):
        """
        Update bed availability based on current admissions and transfers.
        """
        hospital = Hospital.objects.get(id=hospital_id)
        departments = Department.objects.filter(hospital=hospital)

        for dept in departments:
            current_admissions = Admission.objects.filter(
                department=dept, status="ADMITTED"
            ).count()

            dept.available_beds = dept.capacity - current_admissions
            dept.save()

        hospital.available_beds = sum(d.available_beds for d in departments)
        hospital.save()

    def _update_doctor_schedules(self, hospital_id: int):
        """
        Update doctor schedules based on current assignments and emergencies.
        """
        doctors = Doctor.objects.filter(hospital_id=hospital_id, is_active=True)

        for doctor in doctors:
            # Get current assignments
            assignments = Admission.objects.filter(doctor=doctor, status="ADMITTED")

            # Get emergency assignments
            emergencies = EmergencyCase.objects.filter(
                attending_doctor=doctor, outcome="ADMITTED"
            )

            # Update schedule
            doctor.schedule = self._generate_doctor_schedule(assignments, emergencies)
            doctor.save()

    def _process_pending_transfers(self, hospital_id: int):
        """
        Process pending transfers for the hospital.
        """
        pending_transfers = Transfer.objects.filter(
            Q(from_hospital_id=hospital_id) | Q(to_hospital_id=hospital_id),
            status="PENDING",
        )

        for transfer in pending_transfers:
            if self._can_process_transfer(transfer):
                transfer.status = "APPROVED"
                transfer.save()

                # Update bed availability
                self._update_bed_availability(transfer.from_hospital_id)
                self._update_bed_availability(transfer.to_hospital_id)

    def _update_emergency_status(self, hospital_id: int):
        """
        Update emergency status and required resources.
        """
        emergency_cases = EmergencyCase.objects.filter(
            hospital_id=hospital_id, outcome="ADMITTED"
        )

        required_resources = self._calculate_required_resources(emergency_cases)

        # Update hospital emergency status
        Hospital.objects.filter(id=hospital_id).update(
            emergency_unit_status=required_resources
        )

    def _generate_doctor_schedule(
        self, assignments: List[Admission], emergencies: List[EmergencyCase]
    ) -> Dict[str, Any]:
        """
        Generate a doctor's schedule based on assignments and emergencies.
        """
        schedule = {
            "regular_hours": {},
            "emergency_hours": {},
            "total_patients": len(assignments) + len(emergencies),
        }

        # Process regular assignments
        for assignment in assignments:
            day = assignment.admission_date.strftime("%A").lower()
            if day not in schedule["regular_hours"]:
                schedule["regular_hours"][day] = []
            schedule["regular_hours"][day].append(
                {
                    "patient_id": assignment.patient_id,
                    "time": assignment.admission_date.strftime("%H:%M"),
                    "department": assignment.department.name,
                }
            )

        # Process emergency assignments
        for emergency in emergencies:
            day = emergency.arrival_date.strftime("%A").lower()
            if day not in schedule["emergency_hours"]:
                schedule["emergency_hours"][day] = []
            schedule["emergency_hours"][day].append(
                {
                    "patient_id": emergency.patient_id,
                    "time": emergency.arrival_date.strftime("%H:%M"),
                    "priority": emergency.priority,
                }
            )

        return schedule

    def _can_process_transfer(self, transfer: Transfer) -> bool:
        """
        Check if a transfer can be processed.
        """
        # Check bed availability in receiving hospital
        if transfer.to_hospital.available_beds <= 0:
            return False

        # Check if receiving department has capacity
        if transfer.to_department.available_beds <= 0:
            return False

        # Check if required supplies are available
        required_supplies = PurchaseOrder.objects.filter(transfer=transfer).exists()

        if required_supplies:
            supplies_available = self.ecommerce_service.check_supplies_availability(
                transfer.to_hospital_id, transfer.id
            )
            if not supplies_available:
                return False

        return True

    def _calculate_required_resources(
        self, emergency_cases: List[EmergencyCase]
    ) -> Dict[str, Any]:
        """
        Calculate required resources for emergency cases.
        """
        resources = {
            "critical_care_beds": 0,
            "regular_beds": 0,
            "doctors_needed": 0,
            "urgent_supplies": [],
        }

        for case in emergency_cases:
            if case.priority == "CRITICAL":
                resources["critical_care_beds"] += 1
                resources["doctors_needed"] += 2
            elif case.priority == "URGENT":
                resources["regular_beds"] += 1
                resources["doctors_needed"] += 1

            # Check for urgent supplies
            urgent_supplies = Order.objects.filter(
                emergency_case=case, is_urgent=True
            ).values_list("items__product_id", flat=True)

            resources["urgent_supplies"].extend(urgent_supplies)

        return resources
