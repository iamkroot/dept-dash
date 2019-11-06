from django.urls import path, include
from rest_framework import routers
from .views import ResearchScholarView, PublicationView, ProjectView

router = routers.DefaultRouter()
router.register(r'scholars', ResearchScholarView, 'scholar')
router.register(r'publications', PublicationView, 'publications')
router.register(r'projects', ProjectView, 'projects')

urlpatterns = [
    path("", include(router.urls))
]
