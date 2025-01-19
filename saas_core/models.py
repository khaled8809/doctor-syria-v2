from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.


class Tenant(models.Model):
    name = models.CharField(max_length=100)
    subdomain = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "saas_core"

    def __str__(self):
        return self.name


class TenantUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "saas_core"
        unique_together = ("user", "tenant")

    def __str__(self):
        return f"{self.user.username} - {self.tenant.name}"


class SubscriptionFeature(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "saas_core"

    def __str__(self):
        return self.name


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=20)
    features = models.ManyToManyField(SubscriptionFeature)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "saas_core"

    def __str__(self):
        return self.name


class Subscription(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "saas_core"

    def __str__(self):
        return f"{self.tenant.name} - {self.plan.name}"

    @property
    def is_active(self):
        return self.status == "active" and self.end_date > timezone.now()


class Usage(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    feature = models.ForeignKey(SubscriptionFeature, on_delete=models.CASCADE)
    date = models.DateField()
    count = models.IntegerField(default=0)

    class Meta:
        app_label = "saas_core"
        unique_together = ("tenant", "feature", "date")

    def __str__(self):
        return f"{self.tenant.name} - {self.feature.name} - {self.date}"


class Invoice(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "saas_core"

    def __str__(self):
        return f"{self.tenant.name} - {self.amount} - {self.status}"
