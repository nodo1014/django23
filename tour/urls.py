from django.urls import path, include
# from django.contrib import admin
from . import views

app_name = 'tour'
urlpatterns = [
    # path('tag/<str:slug>/', views.tag_page),
    # path('category/<str:slug>/', views.category_page),
    # path('', views.TourList.as_view()),
    path('', views.TourItemList.as_view(), name='index2'),
    path('name/', views.index, name='index'),
    # path('<int:pk>/', views.TourDetail.as_view(), name='tour_detail'),
    # path('<int:pk>/', views.single_tour_page),
    path('create_tour_item/', views.TourItemCreate.as_view()),
    # path('update_tour/<int:pk>/', views.TourUpdate.as_view()),
    # path('<int:pk>/new_comment/', views.new_comment),
    # path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    # path('delete_comment/<int:pk>/', views.delete_comment, name='comment_delete'),
    # path('delete_comment/<int:pk>/', views.CommentDelete.as_view(), name='comment_delete'),


]
# class TourList(ListView):


# urlpatterns = [
#     path('<int:pk>', views.single_tour_page),
#     path('', views.index),
# ]
# def index(request):
#     return render()
# def single_tour_page(request, pk):
#     return render()