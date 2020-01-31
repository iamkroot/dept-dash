from rest_framework import serializers
from .models import Project, Publication
from users.serializers import FacultySerializer, CustomUserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    proposed_by = FacultySerializer(many=True, read_only=True)
    authors = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"
        depth = 1


class PublicationSerializer(serializers.ModelSerializer):
    authors = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Publication
        fields = "__all__"
        depth = 1
