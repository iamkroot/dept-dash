from rest_framework import viewsets
from .serializers import (
    ProjectSerializer,
    PublicationSerializer,
)
from .models import Project, Publication
from users.mixins import NestedViewSetMixin
from users.permissions import IsFaculty, IsHoD, IsResearchScholar, IsStudent


class ProjectView(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # TODO: HOD should be able to see all
        queryset = Project.objects.filter(authors=self.request.user)

        # need to filter in case of nested view
        return super().filter_queryset_by_parents_lookups(queryset)


class PublicationView(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = PublicationSerializer

    def get_queryset(self):
        # TODO: HOD should be able to see all
        queryset = Publication.objects.filter(authors=self.request.user)

        return super().filter_queryset_by_parents_lookups(queryset)
