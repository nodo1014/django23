from datetime import date, timedelta
from .models import TourItem, Iti
from django import forms
from django.forms import formset_factory



class ItiForm(forms.ModelForm):
    class Meta:
        model = Iti
        fields = ('iti_name', 'day', 'city', 'trans', 'content', 'food')

#  그냥 Form 은 필드 정의를 별도로 작성-> 화면 렌더링, 값 받아오기 처리.
# Form 인스턴스는 is_valid()를 갖고 있다. 유효성검사
# 참이면 cleaned_data에 저장
# class DateInput(forms.DateInput):
#     input_type = 'date'


class SearchForm(forms.Form):
    start_date = forms.DateField(label='시작일', initial=date.today())
    end_date = forms.DateField(label='종료일', initial=date.today()+timedelta(days=210))
    keyword = forms.CharField(label='상품코드 또는 상품명', max_length=10, required=False)
#     yoil = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
#     choices=((0, "월"),(1, "화"), (2, "수"), (3, "목"), (4, "금"), (5, "토"), (6, "일"),),
# )
    # yoil = forms.IntegerField(label='요일 체크박스')
    # form 디자인 필요한건, 폼 트윅
    # class Meta:
    #     widgets = {
    #         'start_date': DateInput(),
    #         'end_date': DateInput(),
    #     }

class YoilForm(forms.Form):
    # ids = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput())
    yoil = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'inline': True,}),
        choices=((0, "월"),(1, "화"), (2, "수"), (3, "목"), (4, "금"), (5, "토"), (6, "일"),),
    )
class PkForm(forms.Form):
    # ids = forms.MultipleChoiceField(widget=forms.MultipleHiddenInput())
    queryset = TourItem.objects.all()
    choice = [o.id for o in queryset]
    choice = tuple(choice)
    choice = enumerate(choice)
    print(choice)
    요일 = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            'inline': True,
        }),
        choices = choice
    )


# pk_check =(
#     ( "0","해제(0)"),
#     ( "1","사용(1)"),  
# )
# creating a form 
class ListForm(forms.Form):
    iti_check  = forms.BooleanField(initial=1, required=False)
    air_check  = forms.BooleanField(initial=1, required=False)
    chk_pk = forms.MultipleChoiceField(widget=forms.CheckboxInput)


    
class CopyForm(forms.Form):
    start_date = forms.DateField(label='시작일')
    end_date = forms.DateField(label='종료일')


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)