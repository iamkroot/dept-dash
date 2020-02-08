"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from research import urls as research_urls
from users import urls as users_urls
from auth.views import exchange_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lor_tracker.urls')),
    url(r"^api/", include(research_urls)),
    url(r"^api/", include(users_urls)),
    url(r'^api/auth/(?P<backend>[^/]+)/', exchange_token),
    path('docs/', TemplateView.as_view(template_name='redoc.html'), name='docs'),
]
