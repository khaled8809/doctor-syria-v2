from io import BytesIO
from typing import Optional, Tuple

import barcode
import qrcode
from barcode.writer import ImageWriter
from django.core.files.base import ContentFile

from ..models import Patient


class BarcodeService:
    @staticmethod
    def generate_barcode(data: str, barcode_type: str = "code128") -> Tuple[bytes, str]:
        """
        Generate a barcode for the given data.
        Returns the barcode image as bytes and the barcode value.
        """
        # Create barcode instance
        barcode_class = barcode.get_barcode_class(barcode_type)
        barcode_instance = barcode_class(data, writer=ImageWriter())

        # Generate barcode
        buffer = BytesIO()
        barcode_instance.write(buffer)

        return buffer.getvalue(), data

    @staticmethod
    def generate_qr_code(data: str) -> bytes:
        """
        Generate a QR code for the given data.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        buffer = BytesIO()
        qr.make_image(fill_color="black", back_color="white").save(buffer, "PNG")

        return buffer.getvalue()

    @staticmethod
    def scan_national_id(barcode_data: str) -> Optional[dict]:
        """
        Parse national ID barcode data and return patient information.
        """
        try:
            # Example format: ID|NAME|DOB|GENDER|NATIONALITY
            parts = barcode_data.split("|")
            if len(parts) >= 5:
                return {
                    "national_id": parts[0],
                    "name": parts[1],
                    "date_of_birth": parts[2],
                    "gender": parts[3],
                    "nationality": parts[4],
                }
            return None
        except Exception:
            return None

    @staticmethod
    def register_patient_from_barcode(
        barcode_data: str, tenant_id: int
    ) -> Optional[Patient]:
        """
        Register or update a patient from barcode data.
        """
        patient_info = BarcodeService.scan_national_id(barcode_data)
        if not patient_info:
            return None

        # Try to find existing patient
        patient, created = Patient.objects.get_or_create(
            tenant_id=tenant_id,
            national_id=patient_info["national_id"],
            defaults={
                "name": patient_info["name"],
                "date_of_birth": patient_info["date_of_birth"],
                "gender": patient_info["gender"],
                "nationality": patient_info["nationality"],
            },
        )

        if not created:
            # Update existing patient information
            patient.name = patient_info["name"]
            patient.date_of_birth = patient_info["date_of_birth"]
            patient.gender = patient_info["gender"]
            patient.nationality = patient_info["nationality"]
            patient.save()

        return patient

    @staticmethod
    def generate_patient_card(patient: Patient) -> bytes:
        """
        Generate a patient card with QR code.
        """
        # Create patient data string
        patient_data = f"{patient.id}|{patient.national_id}|{patient.name}"

        # Generate QR code
        return BarcodeService.generate_qr_code(patient_data)
