from rest_framework import serializers
from .models import Project, Publication
from users.models import Faculty, Student, ResearchScholar
from users.serializers import (
    FacultySerializer,
    StudentSerializer,
    ResearchScholarSerializer,
)


def populate_related(data, field, Serializer):
    """Converts (list of) pk(s) to the serialized representation"""
    Model = Serializer.Meta.model
    if isinstance(data[field], list):
        many = True
        objects = Model.objects.filter(pk__in=data[field])
    else:
        many = False
        objects = Model.objects.filter(pk=data[field])
    data[field] = Serializer(objects, many=many).data


class ResearchWorkSerializer(serializers.ModelSerializer):
    faculty_authors = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), many=True, required=False
    )
    student_authors = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), many=True, required=False
    )
    scholar_authors = serializers.PrimaryKeyRelatedField(
        queryset=ResearchScholar.objects.all(), many=True, required=False
    )

    def validate(self, data):
        author_fields = ("faculty_authors", "student_authors", "scholar_authors")
        if all(not data.get(field, True) for field in author_fields):
            raise serializers.ValidationError("At least one author is required")
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        populate_related(data, "faculty_authors", FacultySerializer)
        populate_related(data, "student_authors", StudentSerializer)
        populate_related(data, "scholar_authors", ResearchScholarSerializer)
        return data


class ProjectSerializer(ResearchWorkSerializer):
    proposed_by = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), many=True
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        populate_related(data, "proposed_by", FacultySerializer)
        return data

    class Meta:
        model = Project
        fields = "__all__"
        depth = 1


class PublicationSerializer(ResearchWorkSerializer):
    class Meta:
        model = Publication
        fields = "__all__"
        depth = 1
