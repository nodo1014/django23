from django.shortcuts import render
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from .models import Post


# 함수형: {% for p in posts %} {% endfor %} {{p.get_absolute_url }}
# 클래스형: for p in object_list
class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'blog/post_list.html'

class PostDetail(DetailView):
    model = Post
    # template_name = 'blog/single_post_page.html'
    #함수형을 쓰더라도, 템플릿파일명은 클래스형을 가정하고 만들자.
    #template_name = 'blog/post_detail.html'

# def index(request):
#     # posts = Post.objects.all()
#     posts = Post.objects.all().order_by('-pk');
#
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'posts': posts,
#         }
#         )

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )
