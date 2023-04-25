from datetime import date, time, timedelta
from django.db import models
import os
from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdown
from tinymce.models import HTMLField


# //FIXME: ForeignKey -> User의 pk와 연결돼 있다는 말
# django 라이브러리, db.models 모듈 임포트 후, Model클래스 상속
# Tour/title,content,created_at
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, allow_unicode=True)

    # category=None 카테고리 미분류, 태그 미분류는 없자낭

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tour/tag/{self.slug}/'
        # return f'/tour/category/{self.slug}/'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, null=True, blank=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tour/category/{self.slug}/'
        # return f'/tour/category/{self.slug}/'

    class Meta:
        verbose_name_plural = 'Categories'


# Post에서 변경
class BasicCode(models.Model):
    basic_code = models.CharField('기초코드',max_length=6, unique=True, help_text="예)ATP101")
    title = models.CharField('기초 상품 제목', max_length=80, help_text="방콕/파타야 빠빠빠 상품")
    hook_text = models.CharField('상품설명',max_length=120, blank=True)
    # content = models.TextField()
    content = MarkdownxField()
    head_image = models.ImageField(upload_to='tour/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='tour/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, null=True,blank=True, on_delete=models.SET_NULL)
    # 카테고리 지워지면, 연결된 Tour까지 삭제되면 안됨 -> models.SET_NULL
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
   
    tags = models.ManyToManyField(Tag, blank=True)

    #  __str__메서드 : 객체 자체의 내용을 출력
    def __str__(self):
        return f'{self.basic_code}'

    def get_absolute_url(self):
        return f'/tour/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    # basename(): 파일이름만
    # split(파일) : 디렉토리와 파일 분리, splitext():확장자만, dirname: 디렉토리만 ,   isdir(): 디렉토리인지?
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]
        # return os.path.splitext(self.file_upload.name)

    def get_content_markdown(self):
        return markdown(self.content)

# class DetailCode(models.Model):
#     basic_code = models.ForeignKey(BasicCode, null=True, blank=True, on_delete=models.SET_NULL)
#     detail_code = models.CharField('상세코드',max_length=4, unique=True, help_text="예)KE00 항공+숫자로 작성... 이건...TourItem에서 입력하는게 맞을 듯")
#     title = models.CharField('의미없음-메모용', max_length=50, blank=True)
#     # slug = models.SlugField(max_length=50, unique=True, null=True, blank=True, allow_unicode=True)

#     def __str__(self):
#         return f'{self.basic_code}{self.detail_code} : {self.title}'

#     def get_absolute_url(self):
#         return f'/tour/detailcode/{self.detail_code}/'
#         # return f'/tour/category/{self.slug}/'
# 출발일별 상품
class TourItem(models.Model):
    # Comment클래스는 Tour보다 아래 있어야 한다!!
    # TODO: 날짜+deatil_code+code_suffix 는 유일해야한다.
    # detail_code = models.ForeignKey(DetailCode, null=True, blank=True, on_delete=models.SET_NULL, related_name = 'code')
    basic_code = models.ForeignKey(BasicCode, null=True, blank=True, on_delete=models.SET_NULL, related_name = 'tour_item')
    air_code = models.CharField(max_length=2)
    suffix_code = models.CharField(max_length=2, blank=True)
    #item_code, item_no 구현..? zfill 이용. 나중에
    title = models.CharField(max_length=50, blank=True)
    etc = models.CharField(max_length=50, blank=True)
    airline = models.CharField(max_length=20, blank=True)
    price = models.IntegerField("숫자", default = 0, help_text="미입력시 0. 문의")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    air_sync = models.BooleanField(default = True, blank=True, null=True)
    d_city1 = models.CharField(max_length=3, blank=True)
    d_city2 = models.CharField(max_length=3, blank=True)
    d_date1 = models.DateField(default=date(2000,1,1))
    # d_date2 = models.DateField(default=date(2000,1,2))
    d_daychange = models.IntegerField(default=1)
    stay = models.IntegerField(default=5)
    r_daychange = models.IntegerField(default=1)
    d_time1 = models.TimeField(default=time(19,00))
    d_time2 = models.TimeField(default=time(23,30))
    r_city1 = models.CharField(max_length=3, blank=True)
    r_city2 = models.CharField(max_length=3, blank=True)
    r_time1 = models.TimeField(default=time(23, 30))
    r_time2 = models.TimeField(default=time(6, 00))
    # datetime.datetime.now() <-naive
    # django.utils.timezone.now() <--time-zone-aware
    # 날짜객체로 date.fromisoformat('2020-01-31')
    # 날짜객체->iso date.isoformat(d1)
    # content = MarkdownxField() # 일정표 상세
    content = HTMLField(blank=True)
    notice = HTMLField(blank=True) # 일정표 상세
    created_at = models.DateTimeField(auto_now_add=True)
    # DateTimeField(default=timezone.now())
    # DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]-{self.item_code}'
    
    @property
    def item_code(self):
        day_code = self.d_date1.strftime("%Y%m%d")
        basic_code = self.basic_code.basic_code
        air_code = self.air_code
        code_suffix = self.suffix_code
        full_code = (day_code+basic_code+air_code+code_suffix)
        return full_code

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
        return f'/tour/{self.pk}/'

    def get_content_markdown(self):
        return markdown(self.content)


class Iti(models.Model):
    touritem = models.ForeignKey(TourItem, null=True, blank=True, on_delete=models.CASCADE)
    day = models.IntegerField(blank=True)
    city = models.CharField(max_length=100,blank=True)
    trans = models.CharField(max_length=100,blank=True)
    content = HTMLField(blank=True)
    food = models.CharField(max_length=100,default="조식: 호텔식;중식: 현지식;석식: 현지식")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # Iti의 인스턴스인 self 는  self.pk, self.item_code 등 변수를 갖고 있다.
    # def get_absolute_url(self):
    #     return f'/tour/{self.pk}/iti'
    # self.pk 를 일정표에서 받아서...pk 에 해당하는 일정표

    def __str__(self):
        return f'{self.touritem}:{self.day} 일차 {self.food}'

    def get_absolute_url(self):
        return f'{self.touritem.get_absolute_url()}#iti-{self.pk}'

