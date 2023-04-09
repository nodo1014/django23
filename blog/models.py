import os

from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown


#django 라이브러리, db.models 모듈 임포트 후, Model클래스 상속
#Post/title,content,created_at
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, allow_unicode=True)
    # category=None 카테고리 미분류, 태그 미분류는 없자낭

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}/'
        # return f'/blog/category/{self.slug}/'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/blog/category/{self.slug}/'
        # return f'/blog/category/{self.slug}/'
    class Meta:
        verbose_name_plural = 'Categories'

class Post(models.Model):
    title = models.CharField(max_length=80)
    hook_text = models.CharField(max_length=120, blank=True)
    # content = models.TextField()
    content = MarkdownxField()
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #//FIXME: ForeignKey -> User의 pk와 연결돼 있다는 말
    author = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    # 카테고리 삭제했다고, 연결된 Post까지 삭제되면 안됨 -> models.SET_NULL
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag,blank=True)

#  __str__메서드 : 객체 자체의 내용을 출력
    def __str__(self):
        return f'[{self.pk}] {self.title} :: {self.author}'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}'
    
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)
    # basename(): 파일이름만
# split(파일) : 디렉토리와 파일 분리, splitext():확장자만, dirname: 디렉토리만 ,   isdir(): 디렉토리인지?
    def get_file_ext(self):

        return self.get_file_name().split('.')[-1]
        # return os.path.splitext(self.file_upload.name)

    def get_content_markdown(self):
        return markdown(self.content)

