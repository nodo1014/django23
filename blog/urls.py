from django.urls import path, include
# from django.contrib import admin
from . import views


urlpatterns = [
    path('category/<str:slug>/', views.category_page),
    path('category2/<str:slug>/', views.CategoryList.as_view()),
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view())
    # path('<int:pk>/', views.single_post_page),

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