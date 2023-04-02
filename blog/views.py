from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import Category, Tag, Post


# 함수형: {% for p in posts %} {% endfor %} {{p.get_absolute_url }}
# 클래스형: for p in object_list

# //FIXME: tag 와 카테고리 차이. 미분류가 없다. N:N 으로..
#  태그 전부 출력시. iterator, all 등 관계는 없는 듯.
def tag_page(request, slug):
    # path('tag/<str:slug>/', views.tag_page)
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all().order_by('-pk')

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'tags': Tag.objects.all(),
            'tag': tag,
        }
    )


def category_page(request, slug):
    # path('category/<str:slug>/', views.category_page)
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None).order_by('-pk')
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category).order_by('-pk')

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )
    # 미분류는 카테고리 값이 없어서, category.post_set.count 처럼 카테고리객체를 참조하는 포린키 post로 역참조 불가.
    # no_category_post_count: Post 객체로 정방향 조회. category=None


class CategoryList(ListView):
    # path('category2/<str:slug>/', views.CategoryList.as_view())
    model = Post
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.order_by('-created_at')[:100]


class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        # context = super(PostList, self).get_context_data()
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context


# PostList(ListView)에서 model = Post 만 하면,
# get_context_data()가 post_list = Post.objects.all() 을 했었던 것.
# super(PostList, self) PostList의 부모인 ListView를 자식클래스로 불러서, 딕셔너리형태로 기능 추가.

class PostDetail(DetailView):
    model = Post
    # ordering = '-pk'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        # context = super(PostDetail, self).get_context_data()
        context = super().get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    # template_name = 'blog/single_post_page.html'
    # 함수형을 쓰더라도, 템플릿파일명은 클래스형을 가정하고 만들자.
    # template_name = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

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
