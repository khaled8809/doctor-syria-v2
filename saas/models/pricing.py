from django.contrib.auth.models import User
from django.db import models

from saas_core.models import Tenant


class PricingPlan(models.Model):
    """نموذج خطط التسعير"""

    PLAN_TYPES = [
        ("FREE", "Free Trial"),
        ("BASIC", "Basic"),
        ("PRO", "Professional"),
        ("ENTERPRISE", "Enterprise"),
    ]

    BILLING_CYCLES = [
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
        ("CUSTOM", "Custom"),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLES)
    is_active = models.BooleanField(default=True)

    # حدود الخطة
    max_doctors = models.IntegerField(help_text="عدد الأطباء المسموح به")
    max_appointments = models.IntegerField(help_text="عدد المواعيد الشهرية")
    max_patients = models.IntegerField(help_text="عدد المرضى المسموح به")

    # الميزات المضمنة
    includes_lab = models.BooleanField(default=False)
    includes_pharmacy = models.BooleanField(default=False)
    includes_radiology = models.BooleanField(default=False)
    includes_insurance = models.BooleanField(default=False)
    includes_api = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"


class PlanFeature(models.Model):
    """نموذج ميزات الخطة"""

    plan = models.ForeignKey(
        PricingPlan, on_delete=models.CASCADE, related_name="features"
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.plan.name} - {self.name}"


class PlanSubscription(models.Model):
    """نموذج اشتراكات الخطط"""

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("EXPIRED", "Expired"),
        ("CANCELLED", "Cancelled"),
        ("TRIAL", "Trial"),
    ]

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="plan_subscriptions"
    )
    plan = models.ForeignKey(PricingPlan, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    trial_end_date = models.DateTimeField(null=True, blank=True)

    # معلومات الدفع
    billing_cycle = models.CharField(max_length=20, choices=PricingPlan.BILLING_CYCLES)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    last_payment_date = models.DateTimeField(null=True)
    next_payment_date = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.plan.name}"

    def is_trial(self):
        return self.status == "TRIAL"

    def is_active(self):
        return self.status == "ACTIVE"


class PlanAddon(models.Model):
    """نموذج الإضافات للخطط"""

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubscriptionAddon(models.Model):
    """نموذج الإضافات المشتركة"""

    subscription = models.ForeignKey(
        PlanSubscription, on_delete=models.CASCADE, related_name="addons"
    )
    addon = models.ForeignKey(PlanAddon, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subscription.tenant.name} - {self.addon.name}"


class LoyaltyProgram(models.Model):
    """نموذج برنامج الولاء"""

    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="loyalty_programs"
    )
    name = models.CharField(max_length=100)
    points_per_visit = models.IntegerField(default=10)
    points_per_referral = models.IntegerField(default=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.name}"


class LoyaltyPoints(models.Model):
    """نموذج نقاط الولاء"""

    program = models.ForeignKey(
        LoyaltyProgram, on_delete=models.CASCADE, related_name="points"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="loyalty_points"
    )
    points = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} points"
