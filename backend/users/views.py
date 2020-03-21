from rest_framework import mixins, viewsets
from .filters import DeptFilterBackend
from .models import Department, Faculty, ResearchScholar, Student
from .permissions import IsHoD
from .serializers import (
    DepartmentSerializer,
    FacultySerializer,
    FacultyBasicSerializer,
    ResearchScholarSerializer,
    ResearchScholarBasicSerializer,
    StudentSerializer,
)
from .viewsets import UserViewset


class DepartmentView(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsHoD]

    def get_queryset(self):
        return self.queryset.filter(name=self.request.user.dept)


class FacultyView(UserViewset):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    filter_backends = [DeptFilterBackend]

    def get_serializer_class(self):
        if getattr(self.request.user, "is_hod", False) or self.action != "list":
            return FacultySerializer
        else:
            return FacultyBasicSerializer


class StudentView(UserViewset):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ResearchScholarView(UserViewset):
    queryset = ResearchScholar.objects.all()
    serializer_class = ResearchScholarSerializer
    filter_backends = [DeptFilterBackend]

    def get_serializer_class(self):
        if getattr(self.request.user, "is_hod", False) or self.action != "list":
            return ResearchScholarSerializer
        else:
            return ResearchScholarBasicSerializer
