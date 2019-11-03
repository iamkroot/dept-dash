from rest_framework import serializers
from .models import Department, Faculty, Student


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ("email", "name", "psrn", "alt_email", "contact_num", "dept")
        depth = 1


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ("email", "name", "id_num")
        depth = 1
