from django.db import models
from django.conf import settings
import stripe
from decimal import Decimal
from django.apps import apps
from django.utils import timezone

class Tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)
    
    subscription_plan = models.CharField(
        max_length=20,
        choices=[
            ('FREE', 'Free Plan'),
            ('BASIC', 'Basic Plan'),
            ('PRO', 'Professional Plan'),
            ('ENTERPRISE', 'Enterprise Plan'),
        ],
        default='FREE'
    )
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class TenantUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    is_tenant_admin = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'tenant')
        
    def __str__(self):
        return f"{self.user.email} - {self.tenant.name}"

class Feature(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField(Feature)
    max_users = models.IntegerField(default=1)
    max_storage_gb = models.IntegerField(default=1)
    stripe_price_id = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self):
        return self.name

class ResourceUsage(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    storage_used = models.BigIntegerField(default=0)
    api_calls = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('tenant', 'date')

    def __str__(self):
        return f"{self.tenant.name} - {self.date}"

class Invoice(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateTimeField(auto_now_add=True)
    date_due = models.DateTimeField()
    stripe_invoice_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('PAID', 'Paid'),
            ('OVERDUE', 'Overdue'),
            ('CANCELLED', 'Cancelled')
        ],
        default='PENDING'
    )
    
    def __str__(self):
        return f"{self.tenant.name} - {self.amount} - {self.status}"

class SupportTicket(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
            ('URGENT', 'Urgent')
        ],
        default='MEDIUM'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('OPEN', 'Open'),
            ('IN_PROGRESS', 'In Progress'),
            ('RESOLVED', 'Resolved'),
            ('CLOSED', 'Closed')
        ],
        default='OPEN'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.subject} - {self.status}"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response to {self.ticket.subject}"

class TenantNotification(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(
        max_length=20,
        choices=[
            ('BILLING', 'Billing'),
            ('SYSTEM', 'System'),
            ('USAGE', 'Usage'),
            ('SUPPORT', 'Support')
        ]
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.tenant.name} - {self.title}"

class BackupConfiguration(models.Model):
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)
    frequency = models.CharField(
        max_length=20,
        choices=[
            ('DAILY', 'Daily'),
            ('WEEKLY', 'Weekly'),
            ('MONTHLY', 'Monthly')
        ],
        default='WEEKLY'
    )
    retention_days = models.IntegerField(default=30)
    last_backup = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.tenant.name} - {self.frequency}"

class APIKey(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.tenant.name} - {self.name}"

class TenantAnalytics(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    date = models.DateField()
    page_views = models.IntegerField(default=0)
    unique_visitors = models.IntegerField(default=0)
    average_response_time = models.FloatField(default=0.0)
    error_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('tenant', 'date')
    
    def __str__(self):
        return f"{self.tenant.name} - {self.date}"

# نظام التقارير المتقدمة
class Report(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    report_type = models.CharField(
        max_length=50,
        choices=[
            ('FINANCIAL', 'Financial Report'),
            ('PERFORMANCE', 'Performance Report'),
            ('SATISFACTION', 'Patient Satisfaction'),
            ('ANALYTICS', 'Analytics Report')
        ]
    )
    date_range_start = models.DateTimeField()
    date_range_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.JSONField()
    export_format = models.CharField(
        max_length=20,
        choices=[
            ('PDF', 'PDF Format'),
            ('EXCEL', 'Excel Format'),
            ('CSV', 'CSV Format')
        ],
        default='PDF'
    )
    
    def __str__(self):
        return f"{self.title} - {self.report_type}"

# نظام التكامل مع الأجهزة الطبية
class MedicalDevice(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    device_type = models.CharField(
        max_length=50,
        choices=[
            ('IMAGING', 'Imaging Device'),
            ('LAB', 'Laboratory Device'),
            ('VITAL_SIGNS', 'Vital Signs Monitor'),
            ('OTHER', 'Other Device')
        ]
    )
    model_number = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    api_key = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_maintenance = models.DateTimeField(null=True, blank=True)
    next_maintenance = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.device_type}"

class DeviceReading(models.Model):
    device = models.ForeignKey(MedicalDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    reading_type = models.CharField(max_length=100)
    value = models.JSONField()
    patient = models.ForeignKey('medical_records.Patient', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"{self.device.name} - {self.reading_type} - {self.timestamp}"

# نظام الذكاء الاصطناعي
class AIModel(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    model_type = models.CharField(
        max_length=50,
        choices=[
            ('PREDICTION', 'Patient Condition Prediction'),
            ('DIAGNOSIS', 'Diagnosis Assistant'),
            ('PATTERN', 'Pattern Recognition'),
            ('RECOMMENDATION', 'Treatment Recommendation')
        ]
    )
    version = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    accuracy = models.FloatField(default=0.0)
    last_trained = models.DateTimeField(null=True, blank=True)
    model_parameters = models.JSONField(default=dict)
    
    def __str__(self):
        return f"{self.name} - {self.model_type}"

class AIPrediction(models.Model):
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE)
    patient = models.ForeignKey('medical_records.Patient', on_delete=models.CASCADE)
    prediction_type = models.CharField(max_length=100)
    prediction_result = models.JSONField()
    confidence_score = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    is_accurate = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.model.name} - {self.prediction_type} - {self.confidence_score}"

# نظام إدارة الموارد المتقدم
class Resource(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    resource_type = models.CharField(
        max_length=50,
        choices=[
            ('HUMAN', 'Human Resource'),
            ('EQUIPMENT', 'Medical Equipment'),
            ('INVENTORY', 'Medical Inventory'),
            ('ROOM', 'Room/Facility')
        ]
    )
    status = models.CharField(
        max_length=50,
        choices=[
            ('AVAILABLE', 'Available'),
            ('IN_USE', 'In Use'),
            ('MAINTENANCE', 'Under Maintenance'),
            ('UNAVAILABLE', 'Unavailable')
        ],
        default='AVAILABLE'
    )
    capacity = models.IntegerField(default=1)
    current_usage = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} - {self.resource_type}"

class ResourceSchedule(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    purpose = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('SCHEDULED', 'Scheduled'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('CANCELLED', 'Cancelled')
        ],
        default='SCHEDULED'
    )
    
    def __str__(self):
        return f"{self.resource.name} - {self.start_time}"

# نظام التواصل والمراسلات
class ChatRoom(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chat_rooms')
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.tenant.name}"

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    message_type = models.CharField(
        max_length=50,
        choices=[
            ('TEXT', 'Text Message'),
            ('FILE', 'File Attachment'),
            ('VIDEO_CALL', 'Video Call'),
            ('VOICE_CALL', 'Voice Call')
        ],
        default='TEXT'
    )
    attachment_url = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username} - {self.message_type} - {self.created_at}"

class VideoCall(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('INITIATED', 'Call Initiated'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('MISSED', 'Missed')
        ],
        default='INITIATED'
    )
    recording_url = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.initiator.username} - {self.start_time}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('APPOINTMENT', 'Appointment Reminder'),
        ('MAINTENANCE', 'Equipment Maintenance'),
        ('TASK', 'Task Assignment'),
        ('REPORT', 'Report Generated'),
        ('ALERT', 'System Alert'),
        ('MESSAGE', 'New Message'),
        ('AI_PREDICTION', 'AI Prediction Result'),
    ]

    PRIORITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='MEDIUM')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    related_object_type = models.CharField(max_length=100, blank=True, null=True)
    related_object_id = models.IntegerField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.notification_type}: {self.title}"

    @property
    def related_object(self):
        """Get the related object instance."""
        if self.related_object_type and self.related_object_id:
            model = apps.get_model(self.related_object_type)
            return model.objects.get(id=self.related_object_id)
        return None

    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        self.save()

    def archive(self):
        """Archive the notification."""
        self.is_archived = True
        self.save()

class NotificationPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preferences')
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    appointment_reminders = models.BooleanField(default=True)
    maintenance_alerts = models.BooleanField(default=True)
    task_notifications = models.BooleanField(default=True)
    report_notifications = models.BooleanField(default=True)
    system_alerts = models.BooleanField(default=True)
    message_notifications = models.BooleanField(default=True)
    ai_prediction_notifications = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(default='22:00')
    quiet_hours_end = models.TimeField(default='07:00')

    def __str__(self):
        return f"Notification Preferences for {self.user.username}"

    def can_send_notification(self, notification_type):
        """Check if notification can be sent based on preferences."""
        current_time = timezone.localtime().time()
        if current_time > self.quiet_hours_start or current_time < self.quiet_hours_end:
            return False
            
        notification_mapping = {
            'APPOINTMENT': self.appointment_reminders,
            'MAINTENANCE': self.maintenance_alerts,
            'TASK': self.task_notifications,
            'REPORT': self.report_notifications,
            'ALERT': self.system_alerts,
            'MESSAGE': self.message_notifications,
            'AI_PREDICTION': self.ai_prediction_notifications,
        }
        return notification_mapping.get(notification_type, True)

class AuditLog(models.Model):
    ACTION_TYPES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('OTHER', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=200)
    changes = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=500, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"

class SystemMetric(models.Model):
    METRIC_TYPES = [
        ('CPU_USAGE', 'CPU Usage'),
        ('MEMORY_USAGE', 'Memory Usage'),
        ('DISK_USAGE', 'Disk Usage'),
        ('API_LATENCY', 'API Latency'),
        ('ERROR_RATE', 'Error Rate'),
        ('ACTIVE_USERS', 'Active Users'),
    ]

    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    tenant = models.ForeignKey('Tenant', on_delete=models.CASCADE, related_name='system_metrics')

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['metric_type', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.metric_type}: {self.value}{self.unit} - {self.timestamp}"

class AdminSetting(models.Model):
    SETTING_TYPES = [
        ('SYSTEM', 'System Setting'),
        ('SECURITY', 'Security Setting'),
        ('NOTIFICATION', 'Notification Setting'),
        ('INTEGRATION', 'Integration Setting'),
    ]

    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    setting_type = models.CharField(max_length=20, choices=SETTING_TYPES)
    description = models.TextField()
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return f"{self.key} ({self.setting_type})"

class UserActivity(models.Model):
    ACTIVITY_TYPES = [
        ('PAGE_VIEW', 'Page View'),
        ('FEATURE_USE', 'Feature Use'),
        ('API_CALL', 'API Call'),
        ('ERROR', 'Error'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    page_url = models.CharField(max_length=500, null=True, blank=True)
    feature_name = models.CharField(max_length=100, null=True, blank=True)
    api_endpoint = models.CharField(max_length=500, null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    metadata = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['activity_type']),
        ]

    def __str__(self):
        return f"{self.user} - {self.activity_type} - {self.timestamp}"

class FeatureFlag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)
    tenant_specific = models.BooleanField(default=False)
    enabled_tenants = models.ManyToManyField('Tenant', blank=True)
    conditions = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({'Enabled' if self.is_enabled else 'Disabled'})"

    def is_enabled_for_tenant(self, tenant):
        if not self.is_enabled:
            return False
        if not self.tenant_specific:
            return True
        return tenant in self.enabled_tenants.all()

    def is_enabled_for_user(self, user):
        if not self.is_enabled:
            return False
        if not self.conditions:
            return True
            
        # Example conditions checking
        conditions = self.conditions
        if 'user_roles' in conditions:
            user_roles = set(user.groups.values_list('name', flat=True))
            required_roles = set(conditions['user_roles'])
            if not required_roles.intersection(user_roles):
                return False
                
        if 'percentage_rollout' in conditions:
            user_id_hash = hash(str(user.id))
            if user_id_hash % 100 >= conditions['percentage_rollout']:
                return False
                
        return True

class MedicalCompany(models.Model):
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
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='medical_companies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['license_number']),
        ]

class Warehouse(models.Model):
    WAREHOUSE_TYPES = [
        ('MEDICAL_SUPPLIES', 'Medical Supplies'),
        ('MEDICATIONS', 'Medications'),
        ('EQUIPMENT', 'Medical Equipment'),
        ('GENERAL', 'General Storage'),
    ]

    name = models.CharField(max_length=200)
    warehouse_type = models.CharField(max_length=20, choices=WAREHOUSE_TYPES)
    location = models.TextField()
    capacity = models.FloatField(help_text='Capacity in cubic meters')
    temperature = models.FloatField(help_text='Temperature in Celsius')
    humidity = models.FloatField(help_text='Humidity percentage')
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='managed_warehouses')
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='warehouses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_warehouse_type_display()})"

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['warehouse_type']),
        ]

class MedicalSupply(models.Model):
    SUPPLY_TYPES = [
        ('MEDICATION', 'Medication'),
        ('EQUIPMENT', 'Medical Equipment'),
        ('DISPOSABLE', 'Disposable Supply'),
        ('INSTRUMENT', 'Medical Instrument'),
    ]

    STORAGE_CONDITIONS = [
        ('NORMAL', 'Normal'),
        ('REFRIGERATED', 'Refrigerated'),
        ('FROZEN', 'Frozen'),
        ('CONTROLLED', 'Controlled Substance'),
    ]

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True)
    supply_type = models.CharField(max_length=20, choices=SUPPLY_TYPES)
    manufacturer = models.ForeignKey(MedicalCompany, on_delete=models.PROTECT, related_name='manufactured_supplies')
    description = models.TextField()
    unit = models.CharField(max_length=50)
    minimum_quantity = models.IntegerField()
    storage_condition = models.CharField(max_length=20, choices=STORAGE_CONDITIONS)
    expiry_alert_days = models.IntegerField(default=90)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='medical_supplies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
            models.Index(fields=['supply_type']),
        ]

class InventoryItem(models.Model):
    supply = models.ForeignKey(MedicalSupply, on_delete=models.CASCADE, related_name='inventory_items')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory_items')
    batch_number = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    location_in_warehouse = models.CharField(max_length=100, help_text='Shelf/Row/Section number')
    is_quarantined = models.BooleanField(default=False)
    quarantine_reason = models.TextField(blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='inventory_items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.supply.name} - Batch: {self.batch_number}"

    class Meta:
        ordering = ['expiry_date']
        indexes = [
            models.Index(fields=['batch_number']),
            models.Index(fields=['expiry_date']),
        ]

    @property
    def is_expired(self):
        return self.expiry_date < timezone.now().date()

    @property
    def needs_attention(self):
        days_to_expiry = (self.expiry_date - timezone.now().date()).days
        return days_to_expiry <= self.supply.expiry_alert_days

class InventoryTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('RECEIVE', 'Receive'),
        ('DISPENSE', 'Dispense'),
        ('TRANSFER', 'Transfer'),
        ('RETURN', 'Return'),
        ('DISPOSE', 'Dispose'),
        ('ADJUST', 'Adjustment'),
    ]

    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=100)
    source_location = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        related_name='source_transactions'
    )
    destination_location = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        related_name='destination_transactions'
    )
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='inventory_transactions')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.reference_number}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['reference_number']),
            models.Index(fields=['transaction_type']),
        ]

class PurchaseOrder(models.Model):
    ORDER_STATUS = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('ORDERED', 'Ordered'),
        ('RECEIVED', 'Received'),
        ('CANCELLED', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=100, unique=True)
    supplier = models.ForeignKey(MedicalCompany, on_delete=models.PROTECT, related_name='purchase_orders')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='DRAFT')
    expected_delivery_date = models.DateField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_purchase_orders'
    )
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='approved_purchase_orders'
    )
    notes = models.TextField(blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='purchase_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"PO: {self.order_number} - {self.supplier.name}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
        ]

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
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
            models.Index(fields=['purchase_order', 'supply']),
        ]

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    type = models.CharField(max_length=50, choices=[
        ('GENERAL', 'General Hospital'),
        ('SPECIALIZED', 'Specialized Hospital'),
        ('TEACHING', 'Teaching Hospital'),
        ('MILITARY', 'Military Hospital'),
    ])
    specialties = models.JSONField(default=list)  # List of medical specialties
    bed_capacity = models.IntegerField()
    available_beds = models.IntegerField()
    emergency_unit = models.BooleanField(default=True)
    icu_units = models.IntegerField(default=0)
    operating_rooms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

class Department(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=100)
    head_doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, related_name='headed_departments')
    capacity = models.IntegerField()
    available_beds = models.IntegerField()
    floor = models.CharField(max_length=50)
    phone_extension = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.hospital.name}"

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    condition = models.TextField()
    medical_history = models.JSONField(default=list)
    last_visit = models.DateTimeField(null=True)
    next_appointment = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

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

class Clinic(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    doctors = models.ManyToManyField(Doctor, related_name='clinics')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ClinicService(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()  # in minutes
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} at {self.clinic.name}"

class ClinicEquipment(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    last_maintenance = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} at {self.clinic.name}"

class Medicine(models.Model):
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

class PharmacyOrder(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    items = models.JSONField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    prescription_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.patient.name}"

class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    contact = models.JSONField()
    reliability = models.FloatField()
    last_delivery = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
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

class CommerceOrder(models.Model):
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

class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='admissions')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='admissions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_admissions')
    admission_date = models.DateTimeField()
    discharge_date = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    room_number = models.CharField(max_length=50)
    bed_number = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=[
        ('ADMITTED', 'Admitted'),
        ('DISCHARGED', 'Discharged'),
        ('TRANSFERRED', 'Transferred'),
        ('DECEASED', 'Deceased'),
    ])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.name} - {self.hospital.name}"

class Transfer(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='transfers')
    from_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='transfers_from')
    to_hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='transfers_to')
    from_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='transfers_from')
    to_department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='transfers_to')
    transfer_date = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=50, choices=[
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ])
    approved_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='approved_transfers')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.admission.patient.name} - {self.from_hospital.name} to {self.to_hospital.name}"

class EmergencyCase(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='emergency_cases')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='emergency_cases')
    arrival_date = models.DateTimeField()
    condition = models.TextField()
    priority = models.CharField(max_length=50, choices=[
        ('CRITICAL', 'Critical'),
        ('URGENT', 'Urgent'),
        ('NON_URGENT', 'Non-Urgent'),
    ])
    attending_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='emergency_cases')
    initial_diagnosis = models.TextField()
    treatment = models.TextField()
    outcome = models.CharField(max_length=50, choices=[
        ('ADMITTED', 'Admitted'),
        ('DISCHARGED', 'Discharged'),
        ('TRANSFERRED', 'Transferred'),
        ('DECEASED', 'Deceased'),
    ])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.name} - {self.hospital.name} - {self.priority}"
