from django.contrib.auth.models import User
from django.db import models

from saas_core.models import Tenant


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(
        max_length=20,
        choices=[
            ("monthly", "Monthly"),
            ("yearly", "Yearly"),
        ],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "saas"


class SubscriptionFeature(models.Model):
    plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE, related_name="features"
    )
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)
    value = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plan.name} - {self.name}"

    class Meta:
        app_label = "saas"


class Subscription(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="subscriptions"
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("active", "Active"),
            ("expired", "Expired"),
            ("cancelled", "Cancelled"),
            ("suspended", "Suspended"),
        ],
        default="active",
    )
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tenant} - {self.plan.name}"

    class Meta:
        app_label = "saas"


class Usage(models.Model):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="usage"
    )
    feature = models.ForeignKey(SubscriptionFeature, on_delete=models.CASCADE)
    value = models.JSONField()
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subscription} - {self.feature.name}"

    class Meta:
        app_label = "saas"


class Invoice(models.Model):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="invoices"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending",
    )
    due_date = models.DateTimeField()
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subscription} - {self.amount}"

    class Meta:
        app_label = "saas"


class MedicalCompany(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="medical_companies"
    )
    name = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, unique=True)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    website = models.URLField(blank=True, null=True)
    registration_date = models.DateField()
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["license_number"]),
        ]
        app_label = "saas"


class Warehouse(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="warehouses"
    )
    WAREHOUSE_TYPES = [
        ("MEDICAL_SUPPLIES", "Medical Supplies"),
        ("MEDICATIONS", "Medications"),
        ("EQUIPMENT", "Medical Equipment"),
        ("GENERAL", "General Storage"),
    ]

    name = models.CharField(max_length=200)
    warehouse_type = models.CharField(max_length=20, choices=WAREHOUSE_TYPES)
    location = models.TextField()
    capacity = models.FloatField(help_text="Capacity in cubic meters")
    temperature = models.FloatField(help_text="Temperature in Celsius")
    humidity = models.FloatField(help_text="Humidity percentage")
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="managed_warehouses"
    )
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_warehouse_type_display()})"

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["warehouse_type"]),
        ]
        app_label = "saas"


class MedicalSupply(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="medical_supplies"
    )
    SUPPLY_TYPES = [
        ("MEDICATION", "Medication"),
        ("EQUIPMENT", "Medical Equipment"),
        ("DISPOSABLE", "Disposable Supply"),
        ("INSTRUMENT", "Medical Instrument"),
    ]

    STORAGE_CONDITIONS = [
        ("NORMAL", "Normal"),
        ("REFRIGERATED", "Refrigerated"),
        ("FROZEN", "Frozen"),
        ("CONTROLLED", "Controlled Substance"),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)
    supply_type = models.CharField(max_length=20, choices=SUPPLY_TYPES)
    manufacturer = models.ForeignKey(
        MedicalCompany, on_delete=models.PROTECT, related_name="manufactured_supplies"
    )
    description = models.TextField()
    unit = models.CharField(max_length=50)
    minimum_quantity = models.IntegerField()
    storage_condition = models.CharField(max_length=20, choices=STORAGE_CONDITIONS)
    expiry_alert_days = models.IntegerField(default=90)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["supply_type"]),
        ]
        app_label = "saas"


class InventoryItem(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="inventory_items"
    )
    supply = models.ForeignKey(
        MedicalSupply, on_delete=models.CASCADE, related_name="inventory_items"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="inventory_items"
    )
    batch_number = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    location_in_warehouse = models.CharField(
        max_length=100, help_text="Shelf/Row/Section number"
    )
    is_quarantined = models.BooleanField(default=False)
    quarantine_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supply.name} - Batch: {self.batch_number}"

    class Meta:
        ordering = ["expiry_date"]
        indexes = [
            models.Index(fields=["batch_number"]),
            models.Index(fields=["expiry_date"]),
        ]
        app_label = "saas"

    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    @property
    def needs_attention(self):
        days_to_expiry = (self.expiry_date - timezone.now().date()).days
        return days_to_expiry <= self.supply.expiry_alert_days


class InventoryTransaction(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.SET_NULL,
        null=True,
        related_name="inventory_transactions",
    )
    TRANSACTION_TYPES = [
        ("RECEIVE", "Receive"),
        ("DISPENSE", "Dispense"),
        ("TRANSFER", "Transfer"),
        ("RETURN", "Return"),
        ("DISPOSE", "Dispose"),
        ("ADJUST", "Adjustment"),
    ]

    inventory_item = models.ForeignKey(
        InventoryItem, on_delete=models.CASCADE, related_name="transactions"
    )
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=100)
    source_location = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        related_name="source_transactions",
    )
    destination_location = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        related_name="destination_transactions",
    )
    performed_by = models.ForeignKey(User, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.reference_number}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["reference_number"]),
            models.Index(fields=["transaction_type"]),
        ]
        app_label = "saas"


class PurchaseOrder(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="purchase_orders"
    )
    ORDER_STATUS = [
        ("DRAFT", "Draft"),
        ("PENDING", "Pending Approval"),
        ("APPROVED", "Approved"),
        ("ORDERED", "Ordered"),
        ("RECEIVED", "Received"),
        ("CANCELLED", "Cancelled"),
    ]

    order_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(
        MedicalCompany, on_delete=models.PROTECT, related_name="purchase_orders"
    )
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="DRAFT")
    expected_delivery_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="created_purchase_orders"
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="approved_purchase_orders",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO: {self.order_number} - {self.supplier.name}"

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["-created_at"]),
        ]
        app_label = "saas"


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, related_name="items"
    )
    supply = models.ForeignKey(MedicalSupply, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    received_quantity = models.IntegerField(default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.supply.name} - {self.quantity} {self.supply.unit}"

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    class Meta:
        indexes = [
            models.Index(fields=["purchase_order", "supply"]),
        ]
        app_label = "saas"


class Hospital(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="hospitals"
    )
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    type = models.CharField(
        max_length=50,
        choices=[
            ("GENERAL", "General Hospital"),
            ("SPECIALIZED", "Specialized Hospital"),
            ("TEACHING", "Teaching Hospital"),
            ("MILITARY", "Military Hospital"),
        ],
    )
    specialties = models.JSONField(default=list)
    bed_capacity = models.IntegerField()
    available_beds = models.IntegerField()
    emergency_unit = models.BooleanField(default=True)
    icu_units = models.IntegerField(default=0)
    operating_rooms = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
            models.Index(fields=["city"]),
        ]
        app_label = "saas"


class Department(models.Model):
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="departments"
    )
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100)
    head_doctor = models.ForeignKey(
        "Doctor",
        on_delete=models.SET_NULL,
        null=True,
        related_name="headed_departments",
    )
    capacity = models.IntegerField()
    available_beds = models.IntegerField()
    floor = models.CharField(max_length=50)
    phone_extension = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"

    class Meta:
        app_label = "saas"


class Doctor(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="doctors"
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        indexes = [
            models.Index(fields=["license_number"]),
            models.Index(fields=["specialization"]),
        ]
        app_label = "saas"


class Patient(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="patients"
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    condition = models.TextField()
    medical_history = models.JSONField(default=list)
    last_visit = models.DateTimeField(null=True)
    next_appointment = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["gender"]),
        ]
        app_label = "saas"


class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication} for {self.patient.name}"

    class Meta:
        app_label = "saas"


class Clinic(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="clinics"
    )
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    doctors = models.ManyToManyField(Doctor, related_name="clinics")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "saas"


class ClinicService(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="clinic_services"
    )
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # in minutes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} at {self.clinic.name}"

    class Meta:
        app_label = "saas"


class ClinicEquipment(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="clinic_equipment"
    )
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    last_maintenance = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} at {self.clinic.name}"

    class Meta:
        app_label = "saas"


class Medicine(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="medicines"
    )
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    minimum_stock = models.IntegerField()
    expiry_date = models.DateField()
    description = models.TextField()
    prescription_required = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "saas"


class PharmacyOrder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    items = models.JSONField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    prescription_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.patient.name}"

    class Meta:
        app_label = "saas"


class Manufacturer(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="manufacturers"
    )
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    contact = models.JSONField()
    reliability = models.FloatField()
    last_delivery = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "saas"


class Product(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    minimum_stock = models.IntegerField()
    description = models.TextField()
    image = models.URLField()
    rating = models.FloatField(default=0)
    reviews = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "saas"


class CommerceOrder(models.Model):
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, related_name="commerce_orders"
    )
    customer_name = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=20)
    items = models.JSONField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    payment_status = models.CharField(max_length=20)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"

    class Meta:
        app_label = "saas"


class Admission(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="admissions"
    )
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="admissions"
    )
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="admissions"
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="patient_admissions"
    )
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    room_number = models.CharField(max_length=50)
    bed_number = models.CharField(max_length=50)
    status = models.CharField(
        max_length=50,
        choices=[
            ("ADMITTED", "Admitted"),
            ("DISCHARGED", "Discharged"),
            ("TRANSFERRED", "Transferred"),
            ("DECEASED", "Deceased"),
        ],
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.name} - {self.hospital.name}"

    class Meta:
        app_label = "saas"


class Transfer(models.Model):
    admission = models.ForeignKey(
        Admission, on_delete=models.CASCADE, related_name="transfers"
    )
    from_hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="transfers_from"
    )
    to_hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="transfers_to"
    )
    from_department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="transfers_from"
    )
    to_department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name="transfers_to"
    )
    transfer_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ("PENDING", "Pending"),
            ("APPROVED", "Approved"),
            ("REJECTED", "Rejected"),
            ("COMPLETED", "Completed"),
            ("CANCELLED", "Cancelled"),
        ],
    )
    approved_by = models.ForeignKey(
        Doctor, on_delete=models.SET_NULL, null=True, related_name="approved_transfers"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admission.patient.name} - {self.from_hospital.name} to {self.to_hospital.name}"

    class Meta:
        app_label = "saas"


class EmergencyCase(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="emergency_cases"
    )
    hospital = models.ForeignKey(
        Hospital, on_delete=models.CASCADE, related_name="emergency_cases"
    )
    arrival_date = models.DateTimeField()
    condition = models.TextField()
    priority = models.CharField(
        max_length=50,
        choices=[
            ("CRITICAL", "Critical"),
            ("URGENT", "Urgent"),
            ("NON_URGENT", "Non-Urgent"),
        ],
    )
    attending_doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="emergency_cases"
    )
    initial_diagnosis = models.TextField()
    treatment = models.TextField()
    outcome = models.CharField(
        max_length=50,
        choices=[
            ("ADMITTED", "Admitted"),
            ("DISCHARGED", "Discharged"),
            ("TRANSFERRED", "Transferred"),
            ("DECEASED", "Deceased"),
        ],
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.name} - {self.hospital.name} - {self.priority}"

    class Meta:
        app_label = "saas"
