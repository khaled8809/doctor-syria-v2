from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg, Count
from django.utils import timezone

from ..models import AdminSetting, AuditLog, FeatureFlag, SystemMetric, UserActivity


class AdminService:
    @staticmethod
    def log_audit(
        user, action, instance, changes=None, ip_address=None, user_agent=None
    ):
        """Create an audit log entry."""
        try:
            content_type = ContentType.objects.get_for_model(instance)
            AuditLog.objects.create(
                user=user,
                action=action,
                model_name=content_type.model,
                object_id=str(instance.id),
                object_repr=str(instance),
                changes=changes,
                ip_address=ip_address,
                user_agent=user_agent,
            )
        except Exception as e:
            print(f"Error creating audit log: {str(e)}")

    @staticmethod
    def log_user_activity(user, activity_type, ip_address, user_agent, **kwargs):
        """Log user activity."""
        try:
            UserActivity.objects.create(
                user=user,
                activity_type=activity_type,
                ip_address=ip_address,
                user_agent=user_agent,
                page_url=kwargs.get("page_url"),
                feature_name=kwargs.get("feature_name"),
                api_endpoint=kwargs.get("api_endpoint"),
                error_message=kwargs.get("error_message"),
                metadata=kwargs.get("metadata"),
            )
        except Exception as e:
            print(f"Error logging user activity: {str(e)}")

    @staticmethod
    def record_metric(metric_type, value, unit, tenant):
        """Record a system metric."""
        try:
            SystemMetric.objects.create(
                metric_type=metric_type, value=value, unit=unit, tenant=tenant
            )
        except Exception as e:
            print(f"Error recording metric: {str(e)}")

    @staticmethod
    def get_system_metrics(tenant, metric_type=None, days=7):
        """Get system metrics for the specified period."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        metrics = SystemMetric.objects.filter(tenant=tenant, timestamp__gte=cutoff_date)

        if metric_type:
            metrics = metrics.filter(metric_type=metric_type)

        return metrics.order_by("timestamp")

    @staticmethod
    def get_metric_average(tenant, metric_type, hours=24):
        """Get average value for a metric over the specified period."""
        cutoff_date = timezone.now() - timezone.timedelta(hours=hours)
        return SystemMetric.objects.filter(
            tenant=tenant, metric_type=metric_type, timestamp__gte=cutoff_date
        ).aggregate(avg_value=Avg("value"))["avg_value"]

    @staticmethod
    def get_user_activity_summary(days=7):
        """Get summary of user activity."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return (
            UserActivity.objects.filter(timestamp__gte=cutoff_date)
            .values("activity_type")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

    @staticmethod
    def get_audit_logs(user=None, action=None, model_name=None, days=7):
        """Get filtered audit logs."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        logs = AuditLog.objects.filter(timestamp__gte=cutoff_date)

        if user:
            logs = logs.filter(user=user)
        if action:
            logs = logs.filter(action=action)
        if model_name:
            logs = logs.filter(model_name=model_name)

        return logs.order_by("-timestamp")

    @staticmethod
    def get_setting(key, default=None):
        """Get an admin setting value."""
        try:
            setting = AdminSetting.objects.get(key=key)
            return setting.value
        except AdminSetting.DoesNotExist:
            return default

    @staticmethod
    def set_setting(key, value, setting_type, description, is_public=False):
        """Set an admin setting value."""
        setting, created = AdminSetting.objects.update_or_create(
            key=key,
            defaults={
                "value": value,
                "setting_type": setting_type,
                "description": description,
                "is_public": is_public,
            },
        )
        return setting

    @staticmethod
    def get_feature_flags(tenant=None):
        """Get all feature flags, optionally filtered by tenant."""
        flags = FeatureFlag.objects.all()
        if tenant:
            return [flag for flag in flags if flag.is_enabled_for_tenant(tenant)]
        return flags

    @staticmethod
    def is_feature_enabled(feature_name, tenant=None, user=None):
        """Check if a feature is enabled."""
        try:
            flag = FeatureFlag.objects.get(name=feature_name)
            if tenant and not flag.is_enabled_for_tenant(tenant):
                return False
            if user and not flag.is_enabled_for_user(user):
                return False
            return flag.is_enabled
        except FeatureFlag.DoesNotExist:
            return False

    @staticmethod
    def set_feature_flag(
        name, enabled, description=None, tenant_specific=False, conditions=None
    ):
        """Create or update a feature flag."""
        flag, created = FeatureFlag.objects.update_or_create(
            name=name,
            defaults={
                "is_enabled": enabled,
                "description": description or "",
                "tenant_specific": tenant_specific,
                "conditions": conditions,
            },
        )
        return flag

    @staticmethod
    def get_active_users(hours=24):
        """Get count of active users in the last specified hours."""
        cutoff_date = timezone.now() - timezone.timedelta(hours=hours)
        return (
            UserActivity.objects.filter(timestamp__gte=cutoff_date)
            .values("user")
            .distinct()
            .count()
        )

    @staticmethod
    def get_error_rate(hours=24):
        """Calculate error rate in the last specified hours."""
        cutoff_date = timezone.now() - timezone.timedelta(hours=hours)
        total_activities = UserActivity.objects.filter(
            timestamp__gte=cutoff_date
        ).count()

        error_count = UserActivity.objects.filter(
            timestamp__gte=cutoff_date, activity_type="ERROR"
        ).count()

        if total_activities == 0:
            return 0

        return (error_count / total_activities) * 100

    @staticmethod
    def get_popular_features(days=7):
        """Get most used features in the last specified days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return (
            UserActivity.objects.filter(
                timestamp__gte=cutoff_date, activity_type="FEATURE_USE"
            )
            .values("feature_name")
            .annotate(usage_count=Count("id"))
            .order_by("-usage_count")
        )
