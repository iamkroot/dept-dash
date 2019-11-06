from rest_framework import permissions
from users.models import Faculty, Student
from research.models import ResearchScholar


class IsHoD(permissions.BasePermission):
    """
    Custom permission to only allow HoD to access.
    """

    def has_permission(self, request, view):
        return request.user.groups.filter(name='hod').exists()


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

