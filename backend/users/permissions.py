from rest_framework import permissions
from users.models import Faculty, Student, ResearchScholar


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsHoD(permissions.BasePermission):
    """
    Custom permission to only allow HoD to access.
    """

    def has_permission(self, request, view):
        return getattr(request.user, "is_hod", False)


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsHoDOrIsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(request.user, "is_hod", False) or request.user == obj


class IsFaculty(permissions.BasePermission):
    """
    Custom permission to only allow faculty to access.
    """

    def has_permission(self, request, view):
        return isinstance(request.user, Faculty)


class IsResearchScholar(permissions.BasePermission):
    """
    Custom permission to only allow research scholar to access.
    """

    def has_permission(self, request, view):
        return isinstance(request.user, ResearchScholar)


class IsStudent(permissions.BasePermission):
    """
    Custom permission to only allow student to access.
    """

    def has_permission(self, request, view):
        return isinstance(request.user, Student)
