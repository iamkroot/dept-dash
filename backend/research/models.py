from django.db import models

from users.models import Department, Faculty, Student
from backend import settings


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
    dept = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "research scholar"
        default_related_name = "scholars"


class ResearchWork(models.Model):
    COMMUNICATED = "COM"
    REJECTED = "REJ"
    ACCEPTED = "ACT"
    STATUS_CHOICES = [
        (COMMUNICATED, "communicated"),
        (REJECTED, "rejected"),
        (ACCEPTED, "accepted"),
    ]
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="%(class)s")
    title = models.CharField(max_length=250)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title[:20] + "..." if len(self.title) > 20 else ""


class Publication(ResearchWork):
    CONFERENCE = "CNF"
    JOURNAL = "JRN"
    PUB_TYPE_CHOICES = [(CONFERENCE, "conference"), (JOURNAL, "journal")]
    pub_type = models.CharField(max_length=3, choices=PUB_TYPE_CHOICES)
    pub_date = models.DateField(null=True, blank=True)
    doi_number = models.CharField(
        "Digital Object Indentifier Number", max_length=255, null=True, blank=True
    )
    page_number = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "publication"
        default_related_name = "publications"
        ordering = ["-pub_date"]


class Project(ResearchWork):
    proposed_by = models.ManyToManyField(Faculty)
    agency = models.CharField(max_length=100)
    pi_copi = models.CharField(
        "Principal Investigator/Co-Principal Investigator", max_length=100
    )
    send_date = models.DateField("date of sending", null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "project"
        default_related_name = "projects"
        ordering = ["-send_date", "-start_date"]
