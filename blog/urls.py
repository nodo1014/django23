from django.urls import path, include
# from django.contrib import admin
from . import views

app_name = 'blog'
urlpatterns = [
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    # path('<int:pk>/', views.single_post_page),
    path('create_post/', views.PostCreate.as_view()),
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/', views.delete_comment, name='comment_delete'),
    # path('delete_comment/<int:pk>/', views.CommentDelete.as_view(), name='comment_delete'),


]
# class PostList(ListView):


# urlpatterns = [
#     path('<int:pk>', views.single_post_page),
#     path('', views.index),
# ]
# def index(request):
#     return render()
# def single_post_page(request, pk):
#     return render()