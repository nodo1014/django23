from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView

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


class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    def form_valid(self, form):

        '''
        1. self.request.user 가 로그인(LoginRequired) 했고
        2. 권한(UserPassesTest)이 있는지? is_authenticated and (cu.is_staff or cu.is_superuser):

        - 참이면, form.instance.author 에 current_user 값을 넣은 후,
         super().form_valid 에 저장 후, response

        - 거짓이면, redirect('/blog/')
        '''
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super().form_valid(form)

            # tags_str = self.request.POST.get('tags_str')
            # if tags_str:
            #     tags_str = tags_str.strip()
            #
            #     tags_str = tags_str.replace(',', ';')
            #     tags_list = tags_str.split(';')
            #
            #     for t in tags_list:
            #         t = t.strip()
            #         tag, is_tag_created = Tag.objects.get_or_create(name=t)
            #         if is_tag_created:
            #             tag.slug = slugify(t, allow_unicode=True)
            #             tag.save()
            #         self.object.tags.add(tag)

            return response

        else:
            return redirect('/blog/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_update_form.html'
    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            # tags_str_list = []
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context

    def dispatch(self, request, *args, **kwargs):
        # 로그인&작성자가 같으면,
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()
            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    from django.template.defaultfilters import slugify
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response

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