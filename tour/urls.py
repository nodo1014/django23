from django.urls import path, include
# from django.contrib import admin
from . import views

app_name = 'tour'
urlpatterns = [

    path('index1', views.index, name='index1'),
    path('index2', views.TourItemList.as_view(), name='index2'),
    # table2
    path('index3', views.TourItemTable.as_view(), name='index3'),
    path('name/', views.index, name='index'),

    path('create_tour_item/', views.TourItemCreate.as_view()),

]
