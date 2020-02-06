from rest_framework import viewsets
from users.mixins import NestedViewSetMixin
from users.models import Faculty
from users.permissions import IsFaculty

from .models import Project, Publication
from .permissions import IsAuthor
from .serializers import ProjectSerializer, PublicationSerializer


class ResearchWorkView(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthor]

    def get_permissions(self):
        permission_classes = self.permission_classes
        if self.action not in ("list", "retrieve"):
            permission_classes = [IsFaculty | IsAuthor]
        return [perm() for perm in permission_classes]


class ProjectView(ResearchWorkView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(self.request.user, "is_hod"):
            queryset = self.queryset
        else:
            queryset = user.projects.all()
            if isinstance(user, Faculty):
                queryset |= self.queryset.filter(proposed_by=user)
                queryset |= self.queryset.filter(
                    scholar_authors__in=user.scholars.all()
                )
                queryset = queryset.distinct()

        # need to filter in case of nested view (faculties/123/projects/)
        return super().filter_queryset_by_parents_lookups(queryset)


class PublicationView(ResearchWorkView):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def get_queryset(self):
        user = self.request.user
        if getattr(self.request.user, "is_hod"):
            queryset = self.queryset
        else:
            queryset = user.publications.all()
            if isinstance(user, Faculty):
                queryset |= self.queryset.filter(
                    scholar_authors__in=user.scholars.all()
                )
                queryset = queryset.distinct()

        # need to filter in case of nested view (faculties/123/publications/)
        return super().filter_queryset_by_parents_lookups(queryset)
