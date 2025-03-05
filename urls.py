"""
URL configuration for library_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from library.views import *     # import viewa from library app


# Provide paths from the views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', seat, name='seat'),
    path('registration/', registration, name='registration'),
    path("library-registration/", library_registration, name="library_registration"),
    path("library/", library, name="library"),
    path("verify/<int:library_id>/<str:action>/", verify_action, name="verify_action"),
    path("update-library/<int:library_id>/", update_library, name="update_library"),
    path("delete-library/<int:library_id>/", delete_library, name="delete_library"),
    path('student-details/<int:student_id>/', student_details, name='student_details'),
]
