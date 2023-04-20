
# 이 파일을 단독으로 실행하더라도 마치 manage.py로 django를 구동한 것과 같이 django환경을 사용할 수 있게 됩니다.
import os
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

## BlogData를 import해옵니다
from parsed_data.models import BlogData
from blog.models import Post
from tour.models import BasicCode, Category, Tag, TourItem
from datetime import datetime, date

def parse_blog():
    req = requests.get('https://beomi.github.io/beomi.github.io_old/')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    my_titles = soup.select(
        'h3 > a'
        )
    data = {}
    for title in my_titles:
        data[title.text] = title.get('href')
    # with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    #    json.dump(data, json_file)
    return data

## 이 명령어는 이 파일이 import가 아닌 python에서 직접 실행할 경우에만 아래 코드가 동작하도록 합니다.
new_title = '상품명'
# //TODO: update
# TourItem.objects.filter(d_date1__range=['2020-01-01', '2023-08-31']).update(title=new_title)

# //TODO: delete
result = TourItem.objects.filter(d_date1__range=['2000-01-01', '2020-01-11']).delete()

# 모델.save 시, 포린키 세이브는???
# TourItem(d_date1='2000-01-01',title='모델.save').save()

# get_or_create
# update_or_create
# kw = '모델'
# result = TourItem.objects.filter(title__startswith=kw)
# print (f'{kw}가 포함된 레코드는 {result.count()}개 입니다')

# obj, is_created = TourItem.objects.update_or_create(d_date1='2000-01-01', title='라오스 3박5일 - 으응', defaults={'title': '없어서 등록'})
# // TODO: 멀티레코드일 때 X.
# filter->update로 1개씩 한 개씩
# print(f'obj: {obj}, is_created: {is_created}')

# // TODO: 포린키 저장하기. 포린키 객체 불러오기.
b_code = BasicCode.objects.get(basic_code__icontains='atp')
# get대신 filter 로 조회시, 인스턴스X. 이걸로  업뎃하려했는데 실패.
# ValueError: Cannot assign "<QuerySet [<BasicCode: ATP101>]>": "TourItem.basic_code" must be a "BasicCode" instance.
# get 은 object , filter 는 쿼리셋 반환

# tour_item = TourItem.objects.filter(basic_code=None)
tour_item = TourItem.objects.filter(d_date1__gte='2023-01-01', air_code__istartswith ='7c' )
# // FIXME: 포린키의 이름으로 조회하는 방법?
for i in tour_item:
    i.basic_code = b_code
    i.air_code = 'qq'
    i.save()
print(tour_item)

# for i in result:
#     print(i.pk, i.d_date1, i.basic_code,i.air_code, i.suffix_code, i.title, i.airline, i.price, i.d_time1, i.d_city1)
# if result:
#     print (f'result : {result} {result[0]}개 작업 완료')

item = TourItem.objects.all()
for i in item:
    print(i.pk, i.d_date1, date.strftime(i.d_date1, "%Y%m%d")+i.basic_code.basic_code + i.air_code+i.suffix_code, i.basic_code, i.air_code, i.suffix_code, i.title, i.airline, i.price, i.d_time1, i.d_city1)

if __name__=='__main__':
    pass