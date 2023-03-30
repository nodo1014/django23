from django.db import models
#django 라이브러리, db.models 모듈 임포트 후, Model클래스 상속
#Post/title,content,created_at
class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#  __str__메서드 : 객체 자체의 내용을 출력
    def __str__(self):
        return f'[{self.pk}] {self.title}'
    
    def get_absolute_url(self):
        return f'/blog/{self.pk}'

