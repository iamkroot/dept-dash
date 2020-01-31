from rest_framework import serializers
from .models import CustomUser, Department, Faculty, Student, ResearchScholar
from auth.auth import downcast_user_type


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ("id",)
        depth = 1


class FacultySerializer(serializers.ModelSerializer):
    dept = DepartmentSerializer(read_only=True)

    class Meta:
        model = Faculty
        fields = ("email", "name", "psrn", "alt_email", "contact_num", "dept")
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("email", "name", "id_num")
        depth = 1


class ResearchScholarSerializer(serializers.ModelSerializer):
    supervisor = FacultySerializer(read_only=True)
    dept = DepartmentSerializer(read_only=True)

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


class CustomUserSerializer(serializers.ModelSerializer):
    user_serializers = (FacultySerializer, ResearchScholarSerializer, StudentSerializer)

    def to_representation(self, value):
        user = downcast_user_type(value)
        for UserSerializer in self.user_serializers:
            if isinstance(user, UserSerializer.Meta.model):
                data = UserSerializer(user).data
                data["type"] = user._meta.verbose_name
                return data
        return super().to_representation(value)

    class Meta:
        model = CustomUser
        exclude = ("password",)
        depth = 1
