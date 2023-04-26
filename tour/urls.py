from django.urls import path, include
# from django.contrib import admin
from . import views

app_name = 'tour'
urlpatterns = [
    path('index1/', views.index, name='index1'),
    path('index2/', views.TourItemList.as_view(), name='index2'),
    # 상품 상세 보기 : tour/9/
    path('<int:pk>/', views.TourItemDetail.as_view(), name='tour_detail'),
    path('new/', views.TourItemCreate.as_view(), name='tour_new'),
    path('edit/<int:pk>/', views.TourItemUpdate.as_view(), name='tour_edit'),
    path('delete/<int:pk>/', views.TourItemDelete.as_view(), name='tour_delete'),
    # 일정표 tour/9/save_iti/
    path('<int:pk>/save_iti/', views.save_iti, name='save_iti'),
    path('<int:pk>/new_iti/', views.new_iti, name='new_iti'),
    # path('edit_iti/<int:pk>/', views.update_iti, name='edit_iti'),
    # path('delete_iti/<int:pk>/', views.delete_iti, name='delete_iti'),

    # table2
    path('index3/', views.TourItemTable.as_view(), name='index3'),
    path('name/', views.index, name='index'),

    
    
    # path('iti/', views.ItiDetail.as_view()),

]
