from .models import TourItem
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = TourItem
        fields = ('content',)


#  그냥 Form 은 필드 정의를 별도로 작성-> 화면 렌더링, 값 받아오기 처리.
# Form 인스턴스는 is_valid()를 갖고 있다. 유효성검사
# 참이면 cleaned_data에 저장
# class DateInput(forms.DateInput):
#     input_type = 'date'
class NameForm(forms.Form):
    start_date = forms.DateField(label='시작일')
    end_date = forms.DateField(label='종료일')
    keyword = forms.CharField(label='상품코드', max_length=7, required=False)
    # yoil = forms.IntegerField(label='요일 체크박스')
    # form 디자인 필요한건, 폼 트윅
    # class Meta:
    #     widgets = {
    #         'start_date': DateInput(),
    #         'end_date': DateInput(),
    #     }

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)