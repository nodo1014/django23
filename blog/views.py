from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.text import slugify

from .forms import CommentForm
from .models import Category, Tag, Post, Comment


# 코멘트폼 필요. forms.py 에 모델폼 상속.
def new_comment(request, pk):
    # pk ? 폼 액션을 통해서 받겠지? post.get_absolute_url/new_comment/
    if request.user.is_authenticated:
        # 포린키 저장시. post객체 필요. Comment(post = post 객체, author= request.user),
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())

    else:
        raise PermissionDenied

# def update_comment(request,pk):
#     pass
    # template_name = Comment_form.html
    # UpdateView

    # ImproperlyConfigured at Using ModelFormMixin (base class of CommentUpdate) without the 'fields' attribute is prohibited.)
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    # model 을 지정하면, 자동으로 해당 ModelForm을 상속한 CommentForm이 생성.form_class = CommentForm
    fields = ['content'] # form_class = CommentForm 로 커스텀 가능.
    # fields를 지정하면, form_class 를 생략할 수 있다.


    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post # redirect 위해, post 필요
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

# 클래스 만들 때, 모델명을 앞에 쓰는 것이 규칙! 템플릿 comment_list, _detail, form_class = CommentFomr()등
# class CommentDelete(DeleteView):
#     model = Comment
#     context_object_name = 'comment' #post, post_list
#
#     # fields
#     # template_name =
#     success_url = ('/blog/') # post pk 를 어케 받지? 인자받는 방법. reverse_lazy, args .. 등. 몰라.
#
#
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

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
        context['comment_form'] = CommentForm

        if self.object.tags.exists():
            # tags_str_list = list()
            # for t in self.object.tags.all():
            #     tags_str_list.append(t.name)
            # context['tags'] = '; '.join(tags_str_list)
            context['tags'] = self.object.tags.all()
            # self.object 가 post_list는 object_list처럼, object인데, 왜 self?? 클래스변수면 생략가능., 메서드, 객체변수니까.

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
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    # 새로 만든 포스트(self.object)의 tags 필드에 tag추가
                    self.object.tags.add(tag)

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
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = '; '.join(tags_str_list)

        return context

    def dispatch(self, request, *args, **kwargs):
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
