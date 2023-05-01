from django.urls import path, include
# from django.contrib import admin
from . import views

app_name = 'tour'
urlpatterns = [
    path('item/', views.TourItemList.as_view(), name='item'),
    path('code/', views.index, name='code'),
    # table2
    path('item_lv/', views.TourItemTable.as_view(), name='item_lv'),
    # 상품 상세 보기 : tour/9/
    path('<int:pk>/', views.TourItemDetail.as_view(), name='tour_detail'),
    path('new/', views.TourItemCreate.as_view(), name='tour_new'),
    path('edit/<int:pk>/', views.TourItemUpdate.as_view(), name='tour_edit'),
    path('delete/<int:pk>/', views.TourItemDelete.as_view(), name='tour_delete'),
    path('copy/<int:pk>/', views.TourItemCopy, name='tour_copy'),
    # 일정표 tour/9/save_iti/
    path('<int:pk>/save_iti/', views.save_iti, name='save_iti'),
    path('<int:pk>/new_iti/', views.new_iti, name='new_iti'),
    path('delete_iti/<int:pk>/', views.delete_iti, name='delete_iti'),
    path('edit_iti/<int:pk>/', views.ItiUpdate.as_view(), name='edit_iti'),
    # path('delete_iti/<int:pk>/', views.delete_iti, name='delete_iti'),

    path('name/', views.index, name='index'),

    
    
    # path('iti/', views.ItiDetail.as_view()),

]
