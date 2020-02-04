from rest_framework import viewsets

from .filters import DeptFilterBackend
from .models import Department, Faculty, ResearchScholar, Student
from .serializers import (
    DepartmentSerializer,
    FacultySerializer,
    ResearchScholarSerializer,
    StudentSerializer,
)


class DepartmentView(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.all()


class FacultyView(viewsets.ModelViewSet):
    serializer_class = FacultySerializer
    filter_backends = [DeptFilterBackend]

    def get_queryset(self):
        return Faculty.objects.all()


class StudentView(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_queryset(self):
        return Student.objects.all()


class ResearchScholarView(viewsets.ModelViewSet):
    serializer_class = ResearchScholarSerializer
    filter_backends = [DeptFilterBackend]

    def get_queryset(self):
        return ResearchScholar.objects.all()
