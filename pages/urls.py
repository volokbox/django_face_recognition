# pages/urls.py
from django.contrib import admin
from django.urls import path
from pages.views import face_recognition, take_photos, train_photos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('face_recognition/', face_recognition, name='face_recognition'),
    path('take_photos/', take_photos, name='take_photos'),
    path('train_photos/', train_photos, name='train_photos'),
]
