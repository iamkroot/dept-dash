from django.db import models

from users.models import Faculty, Student


class ResearchScholar(Student):
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
    tenure_type = models.CharField(max_length=2, choices=TENURE_TYPE_CHOICES)
    fellowship = models.CharField(max_length=4, choices=FELLOWSHIP_CHOICES)
    joining_date = models.DateField(null=True, blank=True)
    proposal_approval_date = models.DateField(null=True, blank=True)
    qualifier_passing_date = models.DateField(null=True, blank=True)
    supervisor = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "research scholar"
        default_related_name = "scholars"
