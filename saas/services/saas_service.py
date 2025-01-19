from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone

from ..models import (
    Invoice,
    Subscription,
    SubscriptionFeature,
    SubscriptionPlan,
    Tenant,
    Usage,
)


class SaaSService:
    @staticmethod
    def create_subscription(user, plan_code, start_date=None):
        """Create a new subscription for a user."""
        plan = SubscriptionPlan.objects.get(code=plan_code, is_active=True)
        start_date = start_date or timezone.now()

        # Calculate end date based on billing cycle
        if plan.billing_cycle == "monthly":
            end_date = start_date + timedelta(days=30)
        else:  # yearly
            end_date = start_date + timedelta(days=365)

        subscription = Subscription.objects.create(
            user=user,
            plan=plan_code,
            status="active",
            start_date=start_date,
            end_date=end_date,
            price=plan.price,
            features={feature.code: True for feature in plan.features.all()},
        )

        return subscription

    @staticmethod
    def create_tenant(name, domain, subscription):
        """Create a new tenant for a subscription."""
        return Tenant.objects.create(
            name=name,
            domain=domain,
            subscription=subscription,
            settings={
                "theme": "light",
                "language": "ar",
                "timezone": "Asia/Damascus",
                "currency": "SYP",
            },
        )

    @staticmethod
    def check_feature_access(tenant, feature_code):
        """Check if a tenant has access to a specific feature."""
        if not tenant.is_active:
            return False

        subscription = tenant.subscription
        if not subscription.is_active():
            return False

        return subscription.features.get(feature_code, False)

    @staticmethod
    def track_usage(tenant, feature_code):
        """Track the usage of a feature by a tenant."""
        feature = SubscriptionFeature.objects.get(code=feature_code)
        date = timezone.now().date()

        usage, created = Usage.objects.get_or_create(
            tenant=tenant, feature=feature, date=date, defaults={"count": 0}
        )

        usage.count += 1
        usage.save()

        return usage

    @staticmethod
    def generate_invoice(subscription):
        """Generate a new invoice for a subscription."""
        return Invoice.objects.create(
            subscription=subscription,
            amount=subscription.price,
            status="pending",
            due_date=timezone.now().date() + timedelta(days=7),
            details={
                "plan": subscription.plan,
                "period_start": subscription.start_date.isoformat(),
                "period_end": subscription.end_date.isoformat(),
            },
        )

    @staticmethod
    def process_payment(invoice, payment_details):
        """Process payment for an invoice."""
        # Implement payment processing logic here
        invoice.status = "paid"
        invoice.paid_date = timezone.now().date()
        invoice.save()

        # Extend subscription if this was a renewal payment
        subscription = invoice.subscription
        if subscription.end_date <= timezone.now():
            if subscription.plan == "monthly":
                subscription.end_date = timezone.now() + timedelta(days=30)
            else:
                subscription.end_date = timezone.now() + timedelta(days=365)
            subscription.save()

        return invoice

    @staticmethod
    def check_subscription_status():
        """Check and update status of all subscriptions."""
        now = timezone.now()

        # Update expired subscriptions
        expired = Subscription.objects.filter(status="active", end_date__lt=now)
        expired.update(status="expired")

        # Generate invoices for subscriptions about to expire
        expiring_soon = Subscription.objects.filter(
            status="active",
            end_date__range=[now, now + timedelta(days=7)],
            auto_renew=True,
        )

        for subscription in expiring_soon:
            if not Invoice.objects.filter(
                subscription=subscription, status="pending"
            ).exists():
                Invoice.objects.create(
                    subscription=subscription,
                    amount=subscription.price,
                    status="pending",
                    due_date=subscription.end_date.date(),
                )

    @staticmethod
    def get_subscription_metrics(tenant):
        """Get usage metrics for a tenant's subscription."""
        now = timezone.now()
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        usage = (
            Usage.objects.filter(tenant=tenant, date__gte=month_start, date__lte=now)
            .values("feature__name")
            .annotate(total_count=Sum("count"))
        )

        return {
            "subscription_plan": tenant.subscription.plan,
            "subscription_status": tenant.subscription.status,
            "days_remaining": (tenant.subscription.end_date - now).days,
            "feature_usage": {u["feature__name"]: u["total_count"] for u in usage},
        }
