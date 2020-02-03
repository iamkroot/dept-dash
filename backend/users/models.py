from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from .managers import CustomUserManager


class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """Represents the base user model"""

    username = None
    first_name = None
    last_name = None
    email = models.EmailField("email address", unique=True, primary_key=True)
    name = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    @property
    def short_id(self):
        return self.email[:self.email.find("@")].lower()

    def __str__(self):
        return f"{self.name} ({self.short_id})"


class Faculty(CustomUser):
    PHONE_REGEX = RegexValidator(
        regex=r"^(((\+?91)|0)[\-\s]?)?[6-9]\d{9}$",
        message="Phone number is not in the correct format.",
    )
    psrn = models.PositiveSmallIntegerField("PSRN Number", primary_key=True)
    alt_email = models.EmailField("alternate email", blank=True, null=True)
    contact_num = models.CharField(max_length=15, validators=[PHONE_REGEX])
    address = models.TextField(blank=True, null=True)
    profile_img = models.ImageField("profile picture", blank=True, null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "faculty"
        verbose_name_plural = "faculties"
        default_related_name = "faculties"


class Student(CustomUser):
    # TODO: Add ID Num Regex Validator
    id_num = models.CharField("ID Number", max_length=15, primary_key=True)

    class Meta:
        verbose_name = "student"
        default_related_name = "students"


class ResearchScholar(CustomUser):
    FULL_TIMER = "FT"
    PART_TIMER = "PT"
    ASPIRANT = "AS"
    TENURE_TYPE_CHOICES = [
        (FULL_TIMER, "Full Time"),
        (PART_TIMER, "Part Time"),
        (ASPIRANT, "Aspirant"),
    ]
    NO_FELLOWSHIP = "NONE"
    INSTITUTE_FELLOWSHIP = "INST"
    INDUSTRY_FUNDED = "INDS"
    PROJECT_FUNDED = "PROJ"
    FELLOWSHIP_CHOICES = [
        (NO_FELLOWSHIP, "No Fellowship"),
        (INSTITUTE_FELLOWSHIP, "Institute Fellowship"),
        (INDUSTRY_FUNDED, "Industry Funded"),
        (PROJECT_FUNDED, "Project Funded"),
    ]
    id_num = models.CharField("ID Number", max_length=15, primary_key=True)
    tenure_type = models.CharField(max_length=2, choices=TENURE_TYPE_CHOICES)
    fellowship = models.CharField(max_length=4, choices=FELLOWSHIP_CHOICES)
    fellowship_details = models.TextField(null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    proposal_approval_date = models.DateField(null=True, blank=True)
    qualifier_passing_date = models.DateField(null=True, blank=True)
    graduation_date = models.DateField(null=True, blank=True)
    supervisor = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)
    co_supervisor = models.TextField(null=True, blank=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "research scholar"
        default_related_name = "scholars"
