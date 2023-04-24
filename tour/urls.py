from django.urls import path, include
# from django.contrib import admin
from . import views

app_name = 'tour'
urlpatterns = [
    path('index1/', views.index, name='index1'),
    path('index2/', views.TourItemList.as_view(), name='index2'),
    
    path('<int:pk>/', views.TourItemDetail.as_view(), name='tour_detail'),
    path('edit/<int:pk>/', views.TourItemUpdate.as_view(), name='tour_edit'),
    path('delete/<int:pk>/', views.TourItemDelete.as_view(), name='tour_delete'),
    
    path('new/', views.TourItemCreate.as_view(), name='tour_new'),
    # path('iti/del/<int:pk>/', views.TourItemDel.as_view(), name='tour_del'),
    # table2
    path('index3/', views.TourItemTable.as_view(), name='index3'),
    path('name/', views.index, name='index'),

    path('create_tour_item/', views.TourItemCreate.as_view(), name='create_tour_item'),
    
    # path('iti/', views.ItiDetail.as_view()),

]
