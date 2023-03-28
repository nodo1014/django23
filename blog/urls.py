from django.urls import path, include
# from django.contrib import admin
from . import views

urlpatterns = [
    path('<int:pk>', views.single_post_page),
    path('', views.index),
]
