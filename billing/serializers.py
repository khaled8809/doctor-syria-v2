from rest_framework import serializers

from .models import InsuranceClaim, InsuranceProvider, Invoice, InvoiceItem, Payment


class InvoiceItemSerializer(serializers.ModelSerializer):
    """Serializer لعناصر الفاتورة"""

    class Meta:
        model = InvoiceItem
        fields = ["id", "description", "quantity", "unit_price", "total_price"]


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer للفواتير"""

    items = InvoiceItemSerializer(many=True, read_only=True)
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_method_display = serializers.CharField(
        source="get_payment_method_display", read_only=True
    )

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "patient",
            "patient_name",
            "doctor",
            "doctor_name",
            "appointment",
            "status",
            "status_display",
            "payment_method",
            "payment_method_display",
            "subtotal",
            "tax",
            "discount",
            "total",
            "notes",
            "created_at",
            "updated_at",
            "due_date",
            "paid_at",
            "items",
        ]
        read_only_fields = ["invoice_number", "created_at", "updated_at", "paid_at"]

    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()

    def get_doctor_name(self, obj):
        return obj.doctor.user.get_full_name()


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer للمدفوعات"""

    invoice_number = serializers.CharField(
        source="invoice.invoice_number", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    payment_method_display = serializers.CharField(
        source="get_payment_method_display", read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "invoice",
            "invoice_number",
            "amount",
            "payment_method",
            "payment_method_display",
            "transaction_id",
            "status",
            "status_display",
            "created_at",
            "updated_at",
            "notes",
        ]
        read_only_fields = ["created_at", "updated_at"]


class InsuranceProviderSerializer(serializers.ModelSerializer):
    """Serializer لشركات التأمين"""

    class Meta:
        model = InsuranceProvider
        fields = [
            "id",
            "name",
            "code",
            "contact_person",
            "email",
            "phone",
            "address",
            "active",
            "notes",
        ]


class InsuranceClaimSerializer(serializers.ModelSerializer):
    """Serializer لمطالبات التأمين"""

    invoice_number = serializers.CharField(
        source="invoice.invoice_number", read_only=True
    )
    insurance_provider_name = serializers.CharField(
        source="insurance_provider.name", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = InsuranceClaim
        fields = [
            "id",
            "invoice",
            "invoice_number",
            "insurance_provider",
            "insurance_provider_name",
            "claim_number",
            "status",
            "status_display",
            "amount_claimed",
            "amount_approved",
            "submitted_at",
            "processed_at",
            "notes",
        ]
        read_only_fields = ["claim_number", "submitted_at", "processed_at"]


class InvoicePDFSerializer(serializers.ModelSerializer):
    """Serializer لإنشاء PDF للفواتير"""

    items = InvoiceItemSerializer(many=True, read_only=True)
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    hospital_info = serializers.SerializerMethodField()

    class Meta:
        model = Invoice
        fields = [
            "invoice_number",
            "patient_name",
            "doctor_name",
            "hospital_info",
            "created_at",
            "due_date",
            "items",
            "subtotal",
            "tax",
            "discount",
            "total",
            "notes",
            "status",
            "payment_method",
        ]

    def get_patient_name(self, obj):
        return obj.patient.user.get_full_name()

    def get_doctor_name(self, obj):
        return obj.doctor.user.get_full_name()

    def get_hospital_info(self, obj):
        # يمكن تخصيص هذا حسب إعدادات المستشفى
        return {
            "name": "مستشفى سوريا",
            "address": "دمشق، سوريا",
            "phone": "+963 11 123 4567",
            "email": "info@hospital.com",
        }
