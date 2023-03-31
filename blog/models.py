import os

from django.contrib.auth.models import User
from django.db import models
#django 라이브러리, db.models 모듈 임포트 후, Model클래스 상속
#Post/title,content,created_at
class Post(models.Model):
    title = models.CharField(max_length=80)
    hook_text = models.CharField(max_length=120, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #//FIXME: ForeignKey -> User의 pk와 연결돼 있다는 말
    author = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)

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

