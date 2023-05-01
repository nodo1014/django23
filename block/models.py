from datetime import date, time, timedelta
from django.db import models
import os
from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from tinymce.models import HTMLField

class Block(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/block/{self.pk}/'

class BlockItem(models.Model):
    # area_code = models.CharField(max_length=20) #초이스필드 불필요
    name_fk = models.ForeignKey(Block, null=True, blank=True, on_delete=models.CASCADE)
    # air_code = models.CharField("항공 코드", max_length=2)
    d_fltno = models.CharField("출발 편명", max_length=6, default='KE0000')
    r_fltno = models.CharField("리턴 편명", max_length=6, default='KE0000')
    airline = models.CharField("항공사", max_length=20, blank=True)
    price = models.IntegerField("숫자", default = 0, help_text="미입력시 0. 문의")
    d_city1 = models.CharField(max_length=3, blank=True, default="ICN")
    d_city2 = models.CharField(max_length=3, blank=True, default="CJU")
    d_date1 = models.DateField(default=date(2000,1,1))
    d_date2 = models.DateField(default=date(2000,1,2))
    d_daychange = models.IntegerField(default=1)
    stay = models.IntegerField(default=5)
    r_daychange = models.IntegerField(default=1)

    # datetime.datetime.now() <-naive
    # django.utils.timezone.now() <--time-zone-aware
    # 날짜객체로 date.fromisoformat('2020-01-31')
    # 날짜객체->iso date.isoformat(d1)
    # 예정 일정표
    created_at = models.DateTimeField(auto_now_add=True)
    # DateTimeField(default=timezone.now())
    # DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}'
   

    def 요일(self):
        return f'{date.strftime(self.d_date1, "%a")}'
    @property
    def r_date1(self):
        return self.d_date1 + timedelta(self.stay -2 )
        # f'{}' 스트링을 안쓰면, date 객체로 리턴.->템플릿 필터에서 format 사용가능.

    def r_date2(self):
        # return f'{self.d_date1 + timedelta(self.stay - 2 + self.r_daychange)}'
        return self.d_date1 + timedelta(self.stay - 2 + self.r_daychange)

    # success_url에도 사용되므로, urls.py 수정,삭제 후 어디로 갈지 고려
    def get_absolute_url(self):
        return f'/blockitem/{self.pk}/'