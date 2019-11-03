from rest_framework import serializers
from .models import ResearchScholar, Project, Publication


class ResearchScholarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchScholar
        fields = (
            "email",
            "name",
            "id_num",
            "tenure_type",
            "fellowship",
            "joining_date",
            "proposal_approval_date",
            "qualifier_passing_date",
            "supervisor",
            "dept",
        )
        depth = 1


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        depth = 1


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"
        depth = 1
