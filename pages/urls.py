# pages/urls.py
from django.contrib import admin
from django.urls import path
from pages.views import face_recognition

urlpatterns = [
    path('admin/', admin.site.urls),
    path('face_recognition/', face_recognition, name='face_recognition'),

]