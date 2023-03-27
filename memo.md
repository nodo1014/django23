python3 -V ( 3.10)
색상보기 Shift+커맨드+c

pip freeze > requirements.txt
pip install -r requirements.txt
———————————————————————————
0. 가상환경 dir 만들기
mkdir venv
users/kang/github/프로젝트/venv
0-1.venv 안에서 가상환경 생성
[kang@imac:~/venv]% python3 -m venv .
[kang@imac:~/venv/bin]% source activate
** deactivate 로 벗어남
4. MAC 가상환경 한번에 진입(vi ~/.zshrc)
:mysite 엔터
alias sshq="ssh kang@192.168.0.145"
alias mysite='cd /Users/kang/0_python_web/mysite;source /Users/kang/venvs/my
    site/bin/activate'
*파이참 가상 환경 지정 : 기존 환경 -> 맥 python3 선택
—————————————————
.gitignore
———————————
** vscode로 가상환경을 생성하더라도, 파이참에서 어차피 venv 를 인식시켜줘야하므로,
파이참에서 가상 환경을 생성하자
0 깃허브 프로젝트명(django23) 등록 후, users/kang/github/ 안에서, git clone <https://github.com/nodo1014/django23.git>

1. 파이참으로 github/django23 을  폴더 지정 후, 인터프리터 추가 django23/venv 안에 가상환경 생성

팁! 터미널에서 django23 으로 한번에 진입하기!!!
vi ~/.zshrc
alias django23='cd /Users/kang/github/django23;source /Users/kang/github/django23/venv/bin/activate'
source ~/.zshrc

—————————————————————————

1. 가상환경 진입 상태에서 장고 설치
pip install django==4.0.3  // 두잇장고 3.x // 23.3설치. 장고 4.17
2. 장고 프로젝트 생성
django-admin startproject config .
3. 실행
python3 manage.py runserver
python3 manage.py migrate
python manage.py createsuperuser

localhost:8000 접속시, 영어 -> 한글로 바꾸기.
config/settings.py ko-kr , Asia/Seoul
———————————————————————
App 생성
1 라우팅 만들기(urls.py - views.py )
2 models.py
3 Settings.py에 앱등록
4 admin.py 에 모델등록
—————————————————
django-admin startapp pybo

1 <http://localhost:8000/pybo> 접속 라우팅 만들기
: urls.py 에서 views.index 함수 호출 (views.py def index(request)

- pybo/기준으로 라우팅 만들기
path('pybo/', views.index) —> path('pybo/', include('pybo.urls')),
—————————————————

BASE_DIR :/Users/<사용자>/projects/mysite

1. models.py 작성
class Question(models.Model):
  subject = models.CharField(max_length=200) content = models.TextField()
  create_date = models.DateTimeField()

   def __str__(self):
    return self.subject

2. 테이블생성
2-1 settings.py/ INSTALLED_APPS 에 pybo.apps.PyboConfig 클래스 등록
2-2 python3 manage.py makemigrations 후, 다시 migrate

3. admin.py 에 모델 register!
from .models import Question, Answer
admin.site.register(Question)

python3 manage.py shell (그냥 python3 쉘과 다름 )
——————————————————————
<https://docs.djangoproject.com/en/4.0/topics/db/queries/>
  Question 생성
  Question 조회
  Question 수정
  Question 삭제
  Answer 작성
  Answer 조회

class 클래스(상속):
 클래스필드(클래스변수) = 값

 def __init__(self, 생성자 변수):
  return ….

레코드 삽입
 Question클래스에 ( 생성자 변수와 값 대입 ) -> 객체 q 생성. q.save()

>>> from pybo.models import Question, Answer
>>> from django.utils import timezone

>>> q = Question(subject='pybo가 머에요', content='pybo 궁금해요', create_date=timezone.now())
>>> q.save()

Question.objects.all()
Question.objects.filter(subject__contains='장고')
Question.objects.filter(id=1) —>쿼리셋 리턴
Question.objects.get(id=1) —>모델 객체 리턴. 없으면 오류

수정
q = Question.objects.get(id=2)
q.subject = 'Django Model Question'
q.save()
——————————————
삭제
q.delete()
** Answer 작성 (question: fk 이므로, Question 조회한 객체를 question 속성에 대입)
q = Question.objects.get(id=2)
from django.utils import timezone
a = Answer(question=q, content='생성', create_date=timezone.now())
a.save()

Answer 조회
a = Answer.objects.get(id=1)
a.question (Question 레코드 조회)

질문에 연결된 답변 찾기(역방향으로, 즉 question 으로 답변찾기)
q.answer_set.all()

- 템플릿 태그 문법
<https://docs.djangoproject.com/en/4.0/topics/templates/>

views.py <- url 찍으면, render (request, '템플릿.html', context객체)

from django.http import HttpResponse  # 삭제
from django.shortcuts import render
from .models import Question

def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

2. 템플릿 디렉토리 설정
settings.py : TEMPLATES 에서 'DIRS' :[BASE_DIR / 'templates']

 • 공통 - projects/mysite/templates
 • pybo  - projects/mysite/templates/pybo/question_list.html

3. list.html (템플릿 작성)
{% if question_list %}
    <ul>
    {% for question in question_list %}
        <li><a href="/pybo/{{ question.id }}/">{{ question.subject }}</a></li>
    {% endfor %}
    </ul>

{% else %}
    <p>질문이 없습니다.</p>
{% endif %}

detail.html 만들기 <http://localhost:8000/pybo/2/>
******************************************
Do it 장고로 갈아타기 ( 깃허브, 폰트어썸_ 레이아웃, 부트스트랩의 이유
<https://github.com/nodo1014/django23.git06-2>

포스트 작성 시각 수정 시각 저장 -> admin 에서 시간저장 사라짐
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
