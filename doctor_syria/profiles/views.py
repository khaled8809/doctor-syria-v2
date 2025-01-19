from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    Profile,
    Education,
    Experience,
    Certification,
    Award,
    Publication,
    Contact,
    EmergencyContact,
    Insurance
)
from .serializers import (
    ProfileSerializer,
    EducationSerializer,
    ExperienceSerializer,
    CertificationSerializer,
    AwardSerializer,
    PublicationSerializer,
    ContactSerializer,
    EmergencyContactSerializer,
    InsuranceSerializer,
    ProfilePhotoSerializer
)
from .permissions import IsOwnerOrReadOnly, IsProfileOwnerOrAdmin


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet للملف الشخصي"""
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    search_fields = ['user__first_name', 'user__last_name', 'bio']
    ordering_fields = ['user__date_joined', 'updated_at']

    def get_queryset(self):
        if self.action == 'list':
            # للمشرفين فقط
            if self.request.user.is_staff:
                return Profile.objects.all()
            return Profile.objects.none()
        return Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_photo(self, request, pk=None):
        """تحميل صورة الملف الشخصي"""
        profile = self.get_object()
        serializer = ProfilePhotoSerializer(profile, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def verify_email(self, request, pk=None):
        """التحقق من البريد الإلكتروني"""
        profile = self.get_object()
        profile.is_email_verified = True
        profile.email_verified_at = timezone.now()
        profile.save()
        return Response({'status': 'تم التحقق من البريد الإلكتروني'})

    @action(detail=True, methods=['post'])
    def verify_phone(self, request, pk=None):
        """التحقق من رقم الهاتف"""
        profile = self.get_object()
        profile.is_phone_verified = True
        profile.phone_verified_at = timezone.now()
        profile.save()
        return Response({'status': 'تم التحقق من رقم الهاتف'})


class EducationViewSet(viewsets.ModelViewSet):
    """ViewSet للمؤهلات التعليمية"""
    serializer_class = EducationSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]
    filterset_fields = ['degree', 'field_of_study', 'is_verified']
    search_fields = ['institution', 'degree', 'field_of_study']
    ordering_fields = ['start_date', 'end_date']

    def get_queryset(self):
        return Education.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(profile=profile)


class ExperienceViewSet(viewsets.ModelViewSet):
    """ViewSet للخبرات المهنية"""
    serializer_class = ExperienceSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]
    filterset_fields = ['position', 'employment_type', 'is_current']
    search_fields = ['company', 'position', 'description']
    ordering_fields = ['start_date', 'end_date']

    def get_queryset(self):
        return Experience.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(profile=profile)


class CertificationViewSet(viewsets.ModelViewSet):
    """ViewSet للشهادات المهنية"""
    serializer_class = CertificationSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]
    filterset_fields = ['issuing_organization', 'is_verified']
    search_fields = ['name', 'issuing_organization']
    ordering_fields = ['issue_date', 'expiry_date']

    def get_queryset(self):
        return Certification.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(profile=profile)


class AwardViewSet(viewsets.ModelViewSet):
    """ViewSet للجوائز والتكريمات"""
    serializer_class = AwardSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]
    search_fields = ['title', 'issuer', 'description']
    ordering_fields = ['date_received']

    def get_queryset(self):
        return Award.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(profile=profile)


class PublicationViewSet(viewsets.ModelViewSet):
    """ViewSet للمنشورات العلمية"""
    serializer_class = PublicationSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]
    filterset_fields = ['type', 'is_peer_reviewed']
    search_fields = ['title', 'publisher', 'authors']
    ordering_fields = ['publication_date']

    def get_queryset(self):
        return Publication.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(profile=profile)


class ContactViewSet(viewsets.ModelViewSet):
    """ViewSet لمعلومات الاتصال"""
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]
    search_fields = ['address', 'city', 'country']

    def get_queryset(self):
        return Contact.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(profile=profile)


class EmergencyContactViewSet(viewsets.ModelViewSet):
    """ViewSet لجهات الاتصال في حالات الطوارئ"""
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]
    search_fields = ['name', 'relationship', 'phone']

    def get_queryset(self):
        return EmergencyContact.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(profile=profile)


class InsuranceViewSet(viewsets.ModelViewSet):
    """ViewSet لمعلومات التأمين"""
    serializer_class = InsuranceSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwnerOrAdmin]
    filterset_fields = ['insurance_type', 'is_active']
    search_fields = ['provider', 'policy_number']
    ordering_fields = ['start_date', 'end_date']

    def get_queryset(self):
        return Insurance.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile = get_object_or_404(Profile, user=self.request.user)
        serializer.save(profile=profile)
