from django.urls import path, include
from .views import FacultyView, ResearchScholarView
from rest_framework_extensions.routers import ExtendedDefaultRouter
from research.views import PublicationView, ProjectView

router = ExtendedDefaultRouter()
faculty_routes = router.register(r'faculties', FacultyView, 'faculty')
faculty_routes.register(
    r'publications',
    PublicationView,
    basename="faculty-publication",
    parents_query_lookups=["authors__or__proposed_by"]
)
faculty_routes.register(
    r'projects',
    ProjectView,
    basename="faculty-project",
    parents_query_lookups=["authors__or__proposed_by"]
)

scholar_routes = router.register(r'scholars', ResearchScholarView, 'scholar')
scholar_routes.register(
    r'publications',
    PublicationView,
    basename="scholar-publication",
    parents_query_lookups=["authors"]
)
scholar_routes.register(
    r'projects',
    ProjectView,
    basename="scholar-project",
    parents_query_lookups=["authors"]
)

urlpatterns = [
    path("", include(router.urls))
]
