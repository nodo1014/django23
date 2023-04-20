from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.text import slugify
from datetime import datetime, date, time, timedelta
from .forms import CommentForm, NameForm, ContactForm
from .models import Category, Tag, TourItem, BasicCode

import django_tables2 as tables

class TourItemTable(tables.Table):
    class Meta:
        model = TourItem
        
class TourItemTable(tables.SingleTableView):
    # 리스트뷰는 폼뷰X. get post 오버라이딩
    table_class = TourItemTable
    queryset = TourItem.objects.all() # ListView Overriding
    template_name = "tour/tour_item_list.html"
    form_class = NameForm
    initial = {'start_date':'2023-01-02', 'end_date':'2023-08-31'}
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial = self.initial)
        context = {
                'form':form,
                'table':self.queryset,
                'object_list':self.queryset,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = NameForm(request.POST)
        # your_name = request.POST['your_name']
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            start = form.cleaned_data['start_date'] #
            end = form.cleaned_data['end_date']
            day_list2 = [(start + timedelta(days=i)) for i in range((end-start).days+1)]
            
            tour_item = TourItem.objects.filter(d_date1__range=[start, end])
            
            context = {
                'form':form,
                'day_list2':day_list2,
                'object_list':tour_item,
                'table': tour_item,
            }
        return render(request, 'tour/tour_item_list.html', context)
    
# 한 페이지에 FORM 과 List가 함께 있고,
# 0) CBV: 폼_발리드, 인증, 믹스드인
# 1) 두잇장고 : 자바스크립트로 검색 -> 별도 뷰 작업+템플릿
# 2) 김석훈 : 한페이지에서 동일 처리 : FormView 상속 -> form_valid(form)으로 처리.
# 3) 한페이지 처리 : index 함수 뷰로, get / post 에 따라 컨텍스트 달리 처리. - 가장 간단
class TourItemList(ListView):
    model = TourItem
    ordering = 'd_date1'
    template_name = 'tour/tour_item_list.html'

    def get_context_data(self, **kwargs):
        form = NameForm()
        # context = super(PostList, self).get_context_data()
        context = super(TourItemList,self).get_context_data()
        context['basic_code'] = BasicCode.objects.all()
        context['categories'] = Category.objects.all()
        context['form'] = form
        # context['tags'] = Tag.objects.all()
        # context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

class TourItemCreate(CreateView):
    model = TourItem
    fields = '__all__'

def index(request):
    tour_item = TourItem.objects.all()
    if request.method == 'POST':
        form = NameForm(request.POST)
        # your_name = request.POST['your_name']
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            start = form.cleaned_data['start_date'] #
            end = form.cleaned_data['end_date']
            day_list2 = [(start + timedelta(days=i)) for i in range((end-start).days+1)]
            
            tour_item = TourItem.objects.filter(d_date1__range=[start, end])
            
            context = {
                'form':form,
                'day_list2':day_list2,
                'object_list':tour_item,
            }

    else:
        form = NameForm()
        context = {
            'form':form,
            'object_list':tour_item,
        }

    # return render(request, 'tour/name.html', context)
    return render(request, 'tour/tour_item_list.html', context)




