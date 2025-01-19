from django.conf import settings as django_settings
from django.core.cache import cache
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    SystemSetting,
    EmailTemplate,
    SMSTemplate,
    NotificationSetting,
    WorkingHour,
    Holiday,
    Currency,
    Language,
    Theme,
    BackupSchedule
)
from .serializers import (
    SystemSettingSerializer,
    EmailTemplateSerializer,
    SMSTemplateSerializer,
    NotificationSettingSerializer,
    WorkingHourSerializer,
    HolidaySerializer,
    CurrencySerializer,
    LanguageSerializer,
    ThemeSerializer,
    BackupScheduleSerializer
)
from .permissions import IsAdminOrSuperUser
from .tasks import create_backup, restore_backup


class SystemSettingViewSet(viewsets.ModelViewSet):
    """ViewSet لإعدادات النظام"""
    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    search_fields = ['key', 'value', 'description']

    def perform_update(self, serializer):
        instance = serializer.save()
        # تحديث الإعدادات في الذاكرة المؤقتة
        cache.set(f'setting_{instance.key}', instance.value)

    @action(detail=False)
    def refresh_cache(self, request):
        """تحديث الذاكرة المؤقتة للإعدادات"""
        settings = SystemSetting.objects.all()
        for setting in settings:
            cache.set(f'setting_{setting.key}', setting.value)
        return Response({'status': 'تم تحديث الذاكرة المؤقتة'})


class EmailTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet لقوالب البريد الإلكتروني"""
    queryset = EmailTemplate.objects.all()
    serializer_class = EmailTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active', 'language']
    search_fields = ['name', 'subject', 'body']

    @action(detail=True)
    def preview(self, request, pk=None):
        """معاينة قالب البريد الإلكتروني"""
        template = self.get_object()
        test_data = request.query_params.dict()
        preview = template.render(test_data)
        return Response({'preview': preview})


class SMSTemplateViewSet(viewsets.ModelViewSet):
    """ViewSet لقوالب الرسائل النصية"""
    queryset = SMSTemplate.objects.all()
    serializer_class = SMSTemplateSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active', 'language']
    search_fields = ['name', 'content']

    @action(detail=True)
    def preview(self, request, pk=None):
        """معاينة قالب الرسالة النصية"""
        template = self.get_object()
        test_data = request.query_params.dict()
        preview = template.render(test_data)
        return Response({'preview': preview})


class NotificationSettingViewSet(viewsets.ModelViewSet):
    """ViewSet لإعدادات الإشعارات"""
    queryset = NotificationSetting.objects.all()
    serializer_class = NotificationSettingSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active', 'notification_type']
    search_fields = ['name', 'description']

    @action(detail=False)
    def channels(self, request):
        """قنوات الإشعارات المتاحة"""
        channels = [
            {'id': 'email', 'name': 'البريد الإلكتروني'},
            {'id': 'sms', 'name': 'الرسائل النصية'},
            {'id': 'push', 'name': 'إشعارات الجوال'},
            {'id': 'in_app', 'name': 'إشعارات التطبيق'}
        ]
        return Response(channels)


class WorkingHourViewSet(viewsets.ModelViewSet):
    """ViewSet لساعات العمل"""
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active', 'day_of_week']
    ordering_fields = ['day_of_week', 'start_time']

    @action(detail=False)
    def current_status(self, request):
        """حالة العمل الحالية"""
        is_open = WorkingHour.is_working_now()
        next_open = WorkingHour.next_working_time()
        return Response({
            'is_open': is_open,
            'next_open': next_open
        })


class HolidayViewSet(viewsets.ModelViewSet):
    """ViewSet للعطل والإجازات"""
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active', 'holiday_type']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date']

    @action(detail=False)
    def upcoming(self, request):
        """العطل القادمة"""
        upcoming = Holiday.get_upcoming_holidays()
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)


class CurrencyViewSet(viewsets.ModelViewSet):
    """ViewSet للعملات"""
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active']
    search_fields = ['code', 'name', 'symbol']

    @action(detail=False)
    def exchange_rates(self, request):
        """أسعار الصرف"""
        base_currency = request.query_params.get('base', 'USD')
        rates = Currency.get_exchange_rates(base_currency)
        return Response(rates)


class LanguageViewSet(viewsets.ModelViewSet):
    """ViewSet للغات"""
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active']
    search_fields = ['code', 'name', 'native_name']

    @action(detail=True)
    def translations(self, request, pk=None):
        """ترجمات اللغة"""
        language = self.get_object()
        translations = language.get_translations()
        return Response(translations)


class ThemeViewSet(viewsets.ModelViewSet):
    """ViewSet للمظهر"""
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active', 'is_dark']
    search_fields = ['name', 'description']

    @action(detail=True)
    def preview(self, request, pk=None):
        """معاينة المظهر"""
        theme = self.get_object()
        preview = theme.get_preview()
        return Response(preview)


class BackupScheduleViewSet(viewsets.ModelViewSet):
    """ViewSet لجدولة النسخ الاحتياطي"""
    queryset = BackupSchedule.objects.all()
    serializer_class = BackupScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    filterset_fields = ['is_active', 'backup_type']
    search_fields = ['name', 'description']

    @action(detail=False, methods=['post'])
    def create_backup(self, request):
        """إنشاء نسخة احتياطية يدوياً"""
        backup_type = request.data.get('backup_type', 'full')
        task = create_backup.delay(backup_type=backup_type)
        return Response({
            'task_id': task.id,
            'status': 'تم بدء عملية النسخ الاحتياطي'
        })

    @action(detail=False, methods=['post'])
    def restore_backup(self, request):
        """استعادة نسخة احتياطية"""
        backup_file = request.data.get('backup_file')
        if not backup_file:
            return Response(
                {'error': 'يجب تحديد ملف النسخة الاحتياطية'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task = restore_backup.delay(backup_file=backup_file)
        return Response({
            'task_id': task.id,
            'status': 'تم بدء عملية استعادة النسخة الاحتياطية'
        })
