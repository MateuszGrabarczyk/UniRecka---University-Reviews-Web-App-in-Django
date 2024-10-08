"""
URL configuration for unirecka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf.urls.i18n import i18n_patterns, set_language
from django.contrib import admin
from django.urls import include, path

urlpatterns = i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("account/", include("account.urls")),
    path("university/", include("universities.urls")),
    path("set_language/", set_language, name="set_language"),
)
