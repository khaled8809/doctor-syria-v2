"""
Core permissions for the project.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    السماح فقط لمالك الكائن بتعديله
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """
    السماح فقط للموظفين بالتعديل
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsSuperUserOrStaffReadOnly(permissions.BasePermission):
    """
    السماح فقط للمشرفين بالتعديل وللموظفين بالقراءة
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_staff
        return request.user and request.user.is_superuser


class IsPharmacist(permissions.BasePermission):
    """
    Custom permission to only allow pharmacists to access the view.
    """

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'pharmacist'
