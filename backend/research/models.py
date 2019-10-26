from django.db import models

from users.models import Faculty, Student, CustomUser


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


class Publication(models.Model):
    CONFERENCE = "CNF"
    JOURNAL = "JRN"
    PUB_TYPE_CHOICES = [(CONFERENCE, "conference"), (JOURNAL, "journal")]
    COMMUNICATED = "COM"
    REJECTED = "REJ"
    ACCEPTED = "ACT"
    STATUS_CHOICES = [
        (COMMUNICATED, "communicated"),
        (REJECTED, "rejected"),
        (ACCEPTED, "accepted"),
    ]
    author = models.ManyToManyField(CustomUser)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)
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


class Project(models.Model):
    proposed_by = models.ManyToManyField(Faculty)
    author = models.ManyToManyField(ResearchScholar)
    agency = models.CharField(max_length=100)
    title = models.CharField(max_length=300)
    pi_copi = models.CharField(
        "Principal Investigator/Co-Principal Investigator", max_length=100
    )
    send_date = models.DateField("date of sending", null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "project"
        default_related_name = "projects"
        ordering = ["-send_date", "-start_date"]
