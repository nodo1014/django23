<!--
[공모전 제목 / 주체기관 / 주제 / 시작일 / 마감일]
- visible fields : forms.py 의 폼클래스 정의에서, hidden 이라고 명시적으로 선언하지 않은 모든 필드
- forms.py 선언부 예시:
      contest_title = forms.CharField(
                          label="공모전 제목", 
                          max_length=100,
                          widget=forms.TextInput(
                              attrs={
                                  'placeholder': '공모전 이름을 입력하세요.',
                                  'class':'form-control',
                                  'style': ...                  
                                  }
                          ))
                        
- 객체 전달 흐름 :
    1) (views.py) ContestForm 객체 생성 (여기서 쓰이는 객체 이름 : contestform)
    2) (views.py) context 변수를 통해 해당 템플릿으로 전달.
    3) (template) context 변수 이름을 통해 사용.
    4) (template) 폼 객체는 이 페이지에서 벗어나면 소멸!

- 폼 양식 제출 후 데이터 흐름 :
    1) 사용자 입력 데이터는 request 객체 안에 담겨서 urls.py >> views.py
    2) (views.py) contest_form = ContestForm(request.POST)  # 제출된 데이터를 모두 갖는 폼 객체를 생성!
    3) (views.py) 적절하게 처리!

- 아래와 같이 변환됨
    {{ contestform.contest_title }}
    1) 글을 등록할 때 :
        <input name="contest_title" max_length="100" class='form-control' style='...' required placeholder="공모전 이름을 입력하세요">
        views.py 에서, 비어있는 폼 객체를 전달하면(폼 객체 초기값 설정 안하고!) value 값이 없음()
    2) 글을 수정할 때 :
        <input name="contest_title" max_length="100" class='form-control' style='...' required placeholder="공모전 이름을 입력하세요" value="국민은행 핀테크 공모">
        views.py 에서 수정 시에는, ContestForm 객체에 초기값을 할당해서 넘겨주기 때문.

- css 효과 주기
    1) {% load widget_tweaks %} 패키지 사용 선언
    2) render_field 태그 사용!! (위의 경우에서, 단순히 css class 만 추가한 경우를 예시로 들었음.)
        {% render_field contestform.contest_title class="form-control" %}
        #  <input class="form-control" name="contest_title" max_length="100" required placeholder="공모전 이름을 입력하세요">
-->


<!-- visible_fields (contest_cont 는 하단에!)-->
	{% for field in contestform.visible_fields %}
   		{% if not field == contestform.contest_cont %}
    		<div class="content-box">

                <!--레이블-->
                <div class="content-header">
                    <h3 class="title">
                        {{ field.label }}
                    </h3>
                </div>

                <!--입력란-->
                <div class="content-body">
                    <div class="form-group">
                        {% render_field field class="form-control" %}
                    </div>
                </div>


			</div>
    	{% endif %}
    {% endfor %}
<!-- visible_fields 끝 (contest_cont 는 하단에!)-->