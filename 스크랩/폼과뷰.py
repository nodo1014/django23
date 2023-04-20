class ContestForm(forms.Form):
    # -------------------------------------------- 프론트엔드가 알아야 할 부분 -------------------------------------------- #
    contest_no = forms.CharField(widget=forms.HiddenInput(), required=False)  #
    contest_title = forms.CharField(label="공모전 제목", max_length=100,  #
                                    widget=forms.TextInput(attrs={'placeholder': '공모전 이름을 입력하세요.'}))  #
    contest_asso = forms.CharField(label="공모전 주체 기관", max_length=100,  #
                                   widget=forms.TextInput(attrs={'placeholder': '주체기관을 입력하세요.'}))  #
    contest_topic = forms.CharField(label="공모전 주제", max_length=500,  #
                                    widget=forms.TextInput(attrs={'placeholder': '공모전 주제를 적어주세요.'}))  #
    contest_start = forms.DateTimeField(label="공모전 시작일", widget=forms.DateInput(attrs={'type': 'date'}))  #
    contest_deadline = forms.DateTimeField(label="공모전 마감일", widget=forms.DateInput(attrs={'type': 'date'}))  #
    contest_cont = forms.CharField(label="공모전 상세 설명", widget=forms.Textarea())  #
    # -------------------------------------------- ---------------------- -------------------------------------------- #
    """
    [폼 객체 생성주기]
        1) (forms.py) 에서 클래스 정의
        2) (views.py) 에서 객체 생성 => 컨텍스트 변수에 담아 템플릿으로 넘겨줌
        3) (template) 폼 객체 멤버 변수는 각각 해당변수선언에 대응하는 input 태그로 변환됨.(밑에 예시)
        4) (template) 해당 템플릿에서 이탈하면 폼 객체 소멸.

    [ 변환 예시 ]          
     : 변수이름은 input 태그의 name 으로 들어감! 
     : models.py 에서 blank = True 설정 안하면 자동으로 required 설정됨.
     : 사용자 입력은 안받지만, db에는 값이 있으려면 null=True(models.py) required=False(forms.py) 선언해야함.

    #######################################################################################
            (forms.py)            =>                   (template)
    -------------------------------------------------------------------------------------------------------------------        
    ContestForm.contest_no        =>    <input type="hidden" name="contest_no">
    ContestForm.contest_title     =>    <input name="contest_title" max_length="100" placeholder="공모전 이름을 입력하세요." required>
    ContestForm.contest_asso      =>    <input name="contest_asso" max_length="100" placeholder="주체기관을 입력하세요." required>
    ContestForm.contest_topic     =>    <input name="contest_topic" max_length="500" placeholder="공모전 주제를 적어주세요." required>
    ContestForm.contest_start     =>    <input type="date" name="contest_start" required>
    ContestForm.contest_deadline  =>    <input type="date" name="contest_deadline" required>
    ContestForm.contest_cont      =>    <textarea name="contest_cont" required>  
    ########################################################################################

    클래스 내부 함수는 백엔드 처리 부분.
    """

    # 생성자 함수
    # 밑의 사용 예시
    # form_instance = ContestForm()  # 빈 객체 생성!
    #               = ContestForm(instance=contest)  # 공모전 게시글 정보를 갖는 폼 객체 생성, update 시에 기존 정보 보여주기 위함.
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance is not None and isinstance(instance, ContestBoard):
            super().__init__(auto_id=False, initial={
                'contest_no': instance.contest_no,
                'contest_title': instance.contest_title,
                'contest_asso': instance.contest_asso,
                'contest_topic': instance.contest_topic,
                'contest_start': instance.contest_start,
                'contest_deadline': instance.contest_deadline,
                'contest_cont': instance.contest_cont,
            })
        else:
            super().__init__(auto_id=False, *args, **kwargs)

    def save(self, contest_writer):
        return ContestBoard.objects.create(
            contest_title=self.cleaned_data.get('contest_title'),
            contest_asso=self.cleaned_data.get('contest_asso'),
            contest_topic=self.cleaned_data.get('contest_topic'),
            contest_start=self.cleaned_data.get('contest_start'),
            contest_deadline=self.cleaned_data.get('contest_deadline'),
            contest_cont=self.cleaned_data.get('contest_cont'),
            contest_writer=contest_writer
        )

    def update(self):
        contest_no = self.cleaned_data.get('contest_no')
        contest = ContestBoard.objects.get(pk=contest_no)
        contest.contest_title = self.cleaned_data.get('contest_title')
        contest.contest_cont = self.cleaned_data.get('contest_cont')
        contest.contest_start = self.cleaned_data.get('contest_start')
        contest.contest_deadline = self.cleaned_data.get('contest_deadline')
        contest.contest_topic = self.cleaned_data.get('contest_topic')
        contest.contest_asso = self.cleaned_data.get('contest_asso')

        if self.has_changed():
            contest.save()

        return contest

    # overriding
    # views.py 에서 is_valid() 호출시 내부에서 자동적으로 clean 호출
    # clean 함수는
    #       1. 템플릿 폼에서 입력받은 데이터를 적절한 파이썬 type 으로 변환시켜줌.
    #       2. 위에서 정의한 input 태그에 대한 사용자 입력 값의 validation 을 검사함. 오류 발생시 내부적으로 ValidationError 발생
    #       3. validation 검사 과정에서 발생한 모든 필드에 대한 에러들을 통째로 is_valid() 호출한 폼 객체에 반환!
    #           ( 에러가 있다면 is_valid() 는 False )
    #       4. 유효성 검사가 끝난 후, 폼 객체의 멤버변수인 errors 에 접근하여 에러를 확인할 수 있다.
    def clean(self):
        cleaned_data = super().clean()
        start_date = self.cleaned_data.get('contest_start')
        finish_date = self.cleaned_data.get('contest_deadline')

        errors = []
        if not start_date <= finish_date:
            errors.append(forms.ValidationError('공모전 시작일과 마감일을 확인해주세요!'))

        if errors:
            raise forms.ValidationError(errors)

        return cleaned_data

    # 위에서는 간단히 forms.Form 을 상속받아서 폼이 어떻게 기능하는지에 대해 알아보았습니다!
    # forms.ModelForm 을 상속받아서 좀 더 깔끔하게 코딩해보자!!
    # Meta 클래스
    #  : 필드를 정의하는 부분
    #   - model : 어떤 모델을 폼으로 변환할 것인지!
    #   - fields : 어떤 필드를 사용할 것인지. ex. fields = ('contest_no', 'contest_title',)
    #   - exclude : 어떤 필드를 사용하지 않을 것인지. ex. exclude = ('contest_writer',)
    #       (fields 와  exclude 둘 중에 하나는 무조건 명시해야함.)
    #   나머지는 뭐 보시면 이제 아시겠죠? 모르겠으면 위에랑 비교해서 보세용, 그래도 모르겠으면 레퍼런스 참고하세요

    class ContestModelForm(forms.ModelForm):
        # -------------------------------------------- 프론트엔드가 알아야 할 부분 -------------------------------------------- #
        class Meta:
            model = ContestBoard
            # fields = '__all__'
            exclude = ('contest_writer',)  # fields 또는 exclude 필수
            widgets = {
                'contest_title': forms.TextInput(attrs={'placeholder': '공모전 이름을 입력하세요.'}),
                'contest_asso': forms.TextInput(attrs={'placeholder': '주최기관을 입력하세요.'}),
                'contest_topic': forms.TextInput(attrs={'placeholder': '공모전 주제를 적어주세요.'}),
                'contest_start': forms.DateInput(attrs={'type': 'date'}),
                'contest_deadline': forms.DateInput(attrs={'type': 'date'}),
                'contest_cont': forms.Textarea(),
            }
            labels = {
                'contest_title': '공모전 제목',
                'contest_asso': '공모전 주최기관',
                'contest_topic': '공모전 주제',
                'contest_start': '공모전 시작일',
                'contest_deadline': '공모전 마감일',
                'contest_cont': '공모전 상세 설명',
            }

        # -------------------------------------------- ---------------------- -------------------------------------------- #

        # 밑에서부터는 클래스 내장 함수. 백엔드만 신경쓰면 됨.
        # ContestForm 과 다른 점은 save() 메소드 뿐! 나머지는 ContestForm 에서 복붙하면 됨.

        # overriding
        # forms.ModelForm 에는 save 메소드를 지원.
        # super().save()
        #       1) form.cleaned_data 안에 있는 값들로  모델 객체 생성
        #       2) 해당 모델 객체의 save() 메소드를 호출해서 db 에 저장
        #       3) 해당 모델 객체를 리턴.
        #       super().save(commit=False) >> 2)을 생략.
        def save(self, contest_writer):
            contest = super().save(commit=False)  # db에 아직 저장하지는 않고, 객체만 생성
            contest.contest_writer = contest_writer  # 유저정보 받고
            contest.save()  # db에 저장

            return contest

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)