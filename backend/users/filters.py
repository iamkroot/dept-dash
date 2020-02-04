from rest_framework import filters


class DeptFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if not hasattr(request.user, "dept"):
            return queryset
        return queryset.filter(dept=request.user.dept)
