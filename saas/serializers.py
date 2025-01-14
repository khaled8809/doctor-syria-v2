from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Invoice,
    Subscription,
    SubscriptionFeature,
    SubscriptionPlan,
    Tenant,
    TenantUser,
    Usage,
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ("id", "name", "subdomain", "created_at", "is_active")


class TenantUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tenant = TenantSerializer(read_only=True)

    class Meta:
        model = TenantUser
        fields = ("id", "user", "tenant", "role", "is_active")


class SubscriptionFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionFeature
        fields = ("id", "name", "code", "description", "is_active")


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    features = SubscriptionFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = (
            "id",
            "name",
            "description",
            "price",
            "billing_cycle",
            "features",
            "is_active",
            "created_at",
            "updated_at",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    plan = SubscriptionPlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = (
            "id",
            "tenant",
            "plan",
            "start_date",
            "end_date",
            "status",
            "created_at",
            "updated_at",
        )


class UsageSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    feature = SubscriptionFeatureSerializer(read_only=True)

    class Meta:
        model = Usage
        fields = ("id", "tenant", "feature", "date", "count")


class InvoiceSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    subscription = SubscriptionSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "tenant",
            "subscription",
            "amount",
            "status",
            "due_date",
            "paid_date",
            "created_at",
            "updated_at",
        )
