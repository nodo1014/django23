# import requests
# from bs4 import BeautifulSoup
# import json
# import os

# ## python파일의 위치
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# req = requests.get('https://beomi.github.io/beomi.github.io_old/')
# html = req.text
# soup = BeautifulSoup(html, 'html.parser')
# my_titles = soup.select(
#     'h3 > a'
#     )

# data = {}

# for title in my_titles:
#     data[title.text] = title.get('href')

# with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
#     json.dump(data, json_file)

# parse_blog라는 함수로 만들고, {'블로그 글 타이틀': '블로그 글 링크'}로 이루어진 딕셔너리를 반환하도록

import requests
from bs4 import BeautifulSoup
# 이 파일을 단독으로 실행하더라도 마치 manage.py로 django를 구동한 것과 같이 django환경을 사용할 수 있게 됩니다.
import os
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
django.setup()

## BlogData를 import해옵니다
from parsed_data.models import BlogData

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
if __name__=='__main__':
    blog_data_dict = parse_blog()
    for t, l in blog_data_dict.items():
        BlogData(title=t, link=l).save()