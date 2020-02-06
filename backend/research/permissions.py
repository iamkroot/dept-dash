from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        pk = request.user.pk
        return (
            obj.faculty_authors.filter(pk=pk).exists()
            or obj.scholar_authors.filter(pk=pk).exists()
            or obj.student_authors.filter(pk=pk).exists()
            or (hasattr(obj, "proposed_by") and obj.proposed_by.filter(pk=pk).exists())
        )
