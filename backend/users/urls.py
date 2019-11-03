from django.urls import path, include
from rest_framework import routers
from .views import FacultyView


router = routers.DefaultRouter()
router.register(r'faculties', FacultyView, 'faculty')


urlpatterns = [
    path("", include(router.urls))
]
