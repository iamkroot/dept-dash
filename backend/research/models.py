from django.db import models

from users.models import Faculty, Student, ResearchScholar


class ResearchWork(models.Model):
    COMMUNICATED = "COM"
    REJECTED = "REJ"
    ACCEPTED = "ACT"
    STATUS_CHOICES = [
        (COMMUNICATED, "communicated"),
        (REJECTED, "rejected"),
        (ACCEPTED, "accepted"),
    ]
    faculty_authors = models.ManyToManyField(
        Faculty, related_name="%(class)s", blank=True
    )
    student_authors = models.ManyToManyField(
        Student, related_name="%(class)s", blank=True
    )
    scholar_authors = models.ManyToManyField(
        ResearchScholar, related_name="%(class)s", blank=True
    )
    title = models.CharField(max_length=250)
    details = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title[:20] + ("..." if len(self.title) > 20 else "")


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
    scheme = models.CharField(max_length=50)
    pi_copi = models.CharField(
        "Principal Investigator/Co-Principal Investigator", max_length=100
    )
    np_form = models.ImageField("NP Form", null=True, blank=True)
    send_date = models.DateField("date of sending", null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "project"
        default_related_name = "projects"
        ordering = ["-send_date", "-start_date"]
