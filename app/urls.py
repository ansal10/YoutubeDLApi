from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    url(r'config$', views.video_config),
    url(r'format$', views.video_format),
]