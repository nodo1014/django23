from django.urls import path, include
# from django.contrib import admin
from . import views
#langding, about_me
urlpatterns = [
    path('about_me/', views.about_me),
    path('layout_admin/', views.about_me),
    path('', views.landing),
]

# def about_me(request):
#     return render()
# def landing(request):
#     return render()