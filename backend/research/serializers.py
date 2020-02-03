from rest_framework import serializers
from .models import Project, Publication
from users.serializers import (
    FacultySerializer,
    StudentSerializer,
    ResearchScholarSerializer,
)


class ResearchWorkSerializer(serializers.ModelSerializer):
    faculty_authors = FacultySerializer(many=True)
    student_authors = StudentSerializer(many=True)
    scholar_authors = ResearchScholarSerializer(many=True)


class ProjectSerializer(ResearchWorkSerializer):
    proposed_by = FacultySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        depth = 1


class PublicationSerializer(ResearchWorkSerializer):
    class Meta:
        model = Publication
        fields = "__all__"
        depth = 1
