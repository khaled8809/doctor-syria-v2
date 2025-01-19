from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Role, Department, Specialty, Staff
from .serializers import (
    UserSerializer,
    RoleSerializer,
    GroupSerializer,
    PermissionSerializer,
    DepartmentSerializer,
    SpecialtySerializer,
    StaffSerializer,
    UserRegistrationSerializer,
    PasswordChangeSerializer,
    EmailVerificationSerializer
)
from .permissions import (
    IsAdminOrSuperUser,
    IsDepartmentAdmin,
    IsStaffMember,
    CanManageUsers
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet للمستخدمين مع وظائف متقدمة للإدارة"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, CanManageUsers]
    filterset_fields = ['is_active', 'is_staff', 'groups']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        elif self.request.user.is_staff:
            # المشرفون يمكنهم رؤية المستخدمين في أقسامهم فقط
            departments = Department.objects.filter(
                staff__user=self.request.user
            )
            return User.objects.filter(staff__department__in=departments)
        return User.objects.none()

    @action(detail=False, methods=['post'])
    def register(self, request):
        """تسجيل مستخدم جديد"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """تغيير كلمة المرور"""
        user = self.get_object()
        serializer = PasswordChangeSerializer(data=request.data)
        
        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response(
                    {'error': 'كلمة المرور القديمة غير صحيحة'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({'status': 'تم تغيير كلمة المرور بنجاح'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def verify_email(self, request, pk=None):
        """التحقق من البريد الإلكتروني"""
        user = self.get_object()
        serializer = EmailVerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            if user.verification_code == serializer.data.get('code'):
                user.is_email_verified = True
                user.email_verified_at = timezone.now()
                user.save()
                return Response({'status': 'تم التحقق من البريد الإلكتروني'})
            return Response(
                {'error': 'رمز التحقق غير صحيح'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """تفعيل حساب المستخدم"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'تم تفعيل الحساب'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """إلغاء تفعيل حساب المستخدم"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'تم إلغاء تفعيل الحساب'})


class RoleViewSet(viewsets.ModelViewSet):
    """ViewSet للأدوار"""
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    search_fields = ['name', 'description']

    @action(detail=True)
    def users(self, request, pk=None):
        """المستخدمين في هذا الدور"""
        role = self.get_object()
        users = User.objects.filter(roles=role)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def permissions(self, request, pk=None):
        """الصلاحيات المرتبطة بهذا الدور"""
        role = self.get_object()
        permissions = role.permissions.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """ViewSet للمجموعات"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    search_fields = ['name']

    @action(detail=True)
    def users(self, request, pk=None):
        """المستخدمين في هذه المجموعة"""
        group = self.get_object()
        users = User.objects.filter(groups=group)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet للأقسام"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDepartmentAdmin]
    filterset_fields = ['is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

    @action(detail=True)
    def staff(self, request, pk=None):
        """الموظفين في هذا القسم"""
        department = self.get_object()
        staff = Staff.objects.filter(department=department)
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)

    @action(detail=True)
    def statistics(self, request, pk=None):
        """إحصائيات القسم"""
        department = self.get_object()
        total_staff = Staff.objects.filter(department=department).count()
        active_staff = Staff.objects.filter(
            department=department,
            is_active=True
        ).count()
        
        return Response({
            'total_staff': total_staff,
            'active_staff': active_staff,
            'inactive_staff': total_staff - active_staff
        })


class SpecialtyViewSet(viewsets.ModelViewSet):
    """ViewSet للتخصصات"""
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSuperUser]
    search_fields = ['name', 'description']
    ordering_fields = ['name']

    @action(detail=True)
    def doctors(self, request, pk=None):
        """الأطباء في هذا التخصص"""
        specialty = self.get_object()
        staff = Staff.objects.filter(specialty=specialty)
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)


class StaffViewSet(viewsets.ModelViewSet):
    """ViewSet للموظفين"""
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticated, IsStaffMember]
    filterset_fields = ['is_active', 'department', 'specialty']
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'employee_id'
    ]
    ordering_fields = ['joined_date', 'department__name']

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Staff.objects.all()
        elif self.request.user.is_staff:
            # المشرفون يمكنهم رؤية الموظفين في أقسامهم فقط
            departments = Department.objects.filter(
                staff__user=self.request.user
            )
            return Staff.objects.filter(department__in=departments)
        return Staff.objects.none()

    @action(detail=True)
    def schedule(self, request, pk=None):
        """جدول عمل الموظف"""
        staff = self.get_object()
        # يمكن إضافة المنطق الخاص بجدول العمل هنا
        return Response({'message': 'سيتم إضافة جدول العمل قريباً'})

    @action(detail=True)
    def performance(self, request, pk=None):
        """تقييم أداء الموظف"""
        staff = self.get_object()
        # يمكن إضافة المنطق الخاص بتقييم الأداء هنا
        return Response({'message': 'سيتم إضافة تقييم الأداء قريباً'})
