from rest_framework import viewsets
from .serializers import (
    ResearchScholarSerializer,
    ProjectSerializer,
    PublicationSerializer,
)
from .models import ResearchScholar, Project, Publication


class ResearchScholarView(viewsets.ModelViewSet):
    serializer_class = ResearchScholarSerializer

    def get_queryset(self):
        return ResearchScholar.objects.filter(dept=self.request.user.dept)


class ProjectView(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # TODO: HOD should be able to see all
        return Project.objects.filter(author__id=self.request.user)


class PublicationView(viewsets.ModelViewSet):
    serializer_class = PublicationSerializer

    def get_queryset(self):
        # TODO: HOD should be able to see all
        return Publication.objects.filter(author__id=self.request.user)
