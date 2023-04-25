from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.text import slugify
from datetime import datetime, date, time, timedelta
from .forms import *
from .models import *
from .filters import ItemFilter
import django_tables2 as tables
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import CharField, Value

def landing(request):
    recent_posts = TourItem.objects.order_by('-pk')[:3]
    # model = TourItem
    # ordering = '-pk'
    # queryset = TourItem.objects.all() # ListView Overriding
    # template_name = "tour/tour_item_list_3.html"
    # form_class = NameForm
    
    # def get_context_data()
    # def dispatch()
    # def form_valid()

    return render(
        request,
        'single_pages/landing.html',
        {
            'recent_posts': recent_posts,
        }
    )


def about_me(request):
    return render(
        request,
        'single_pages/about_me.html'
    )


class TourItemTable(tables.Table):
    class Meta:
        model = TourItem
        
class TourItemTable(tables.SingleTableView):
    # 리스트뷰는 폼뷰X. get post 오버라이딩
    table_class = TourItemTable
    queryset = TourItem.objects.all() # ListView Overriding
    template_name = "tour/tour_item_list_3.html"
    form_class = NameForm
    initial = {'start_date':'2023-01-02', 'end_date':'2023-08-31'}
    
    
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial = self.initial)
        myFilter = ItemFilter(request.GET, queryset=self.queryset)
        items = myFilter.qs
        context = {
                'form':form,
                'table':self.queryset,
                'object_list':self.queryset,
                'myFilter':myFilter,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = NameForm(request.POST)
        # keyword = request.POST['keyword']
        if form.is_valid():
            start = form.cleaned_data['start_date'] #
            end = form.cleaned_data['end_date']
            keyword = form.cleaned_data['keyword']
            day_list2 = [(start + timedelta(days=i)) for i in range((end-start).days+1)]
            
            tour_item = TourItem.objects.annotate(xxx=Concat('basic_code__basic_code', 'air_code','suffix_code')).filter(Q(d_date1__range=[start, end]) & (Q(xxx__icontains=keyword) | Q(title__icontains=keyword)))
            # tour_item = TourItem.objects.annotate(item_code=Concat( 'air_code',Value(' '), 'suffix_code',output_field=CharField())).filter(Q(d_date1__range=[start, end]) | (Q(item_code__icontains=keyword)))
            # 'basic_code__basic_code',Value(' '),
            print(tour_item)
            context = {
                'form':form,
                'day_list2':day_list2,
                'object_list':tour_item,
                'table': tour_item,
            }
        return render(request, self.template_name, context)
    
# 한 페이지에 FORM 과 List가 함께 있고,
# 0) CBV: 폼_발리드, 인증, 믹스드인
# 1) 두잇장고 : 자바스크립트로 검색 -> 별도 뷰 작업+템플릿
# 2) 김석훈 : 한페이지에서 동일 처리 : FormView 상속 -> form_valid(form)으로 처리.
# 3) 한페이지 처리 : index 함수 뷰로, get / post 에 따라 컨텍스트 달리 처리. - 가장 간단
class TourItemList(ListView):
    # get(): 에서 return render(request, temp_name, context)
    model = TourItem
    ordering = 'd_date1'
    template_name = 'tour/tour_item_list_2.html' # 아니면, get()오버라이딩 직접 지정.

    def get_context_data(self, **kwargs):
        # context = super(PostList, self).get_context_data()
        # context['form'] = NameForm()
        
        context = super(TourItemList,self).get_context_data()
        context['basic_code'] = BasicCode.objects.all()
        context['categories'] = Category.objects.all()
        # NameForm() 은 빈폼 인스턴스를 생성하는데... () 필요한가?
        context['form'] = NameForm
        # context['tags'] = Tag.objects.all()
        # context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    
class TourItemDetail(DetailView):
    model = TourItem
    template_name = "tour/tour_item_detail.html"
    
    def get_context_data(self, **kwargs):
        context = super(TourItemDetail, self).get_context_data()
        # //TODO: 다중값 필드 리스트로.
        # touritem을 참조하는 iti 를 조회 : touritem.iti_set
        itis = self.object.iti_set.all()
        for iti in itis:
            f_list = iti.food.split(';') # 잘라서, 리스트로 변환
            iti.food = f_list #객체를 db에 save()하지 않고, context 오버라이딩용
        context['itis'] = itis
        context['iti_form'] = ItiForm
        return context


class TourItemCreate(CreateView):
    model = TourItem
    fields = '__all__'
    template_name = "tour/tour_item_new.html"

class TourItemUpdate(UpdateView):
    model = TourItem
    fields = '__all__'
    template_name = "tour/tour_item_edit.html"
    
    def form_valid(self, form):
        response = super(TourItemUpdate, self).form_valid(form)
        return response


class TourItemDelete(DeleteView):
    model = TourItem
    fields = '__all__'
    template_name = "tour/tour_item_delete.html"
    

def new_iti(request, pk):
    if request.user.is_authenticated:
        touritem = get_object_or_404(TourItem, pk=pk)

        if request.method == 'POST':
            form = ItiForm(request.POST)
            if form.is_valid():
                iti = form.save(commit=False)
                iti.touritem = touritem
                iti.author = request.user
                iti.save()
                return redirect(iti.get_absolute_url())
        else:
            return redirect(touritem.get_absolute_url())
    else:
        raise PermissionDenied


class ItiUpdate(LoginRequiredMixin, UpdateView):
    model = Iti
    form_class = ItiForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(ItiUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_iti(request, pk):
    iti = get_object_or_404(Iti, pk=pk)
    post = iti.post
    if request.user.is_authenticated and request.user == iti.author:
        iti.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied



def index(request):
    tour_item = TourItem.objects.all()
    template_name = 'tour/tour_item_list_1.html'
    if request.method == 'POST':
        form = NameForm(request.POST)
        # keyword = request.POST['keyword']
        if form.is_valid():
            start = form.cleaned_data['start_date'] #
            end = form.cleaned_data['end_date']
            keyword = form.cleaned_data['keyword']
            day_list2 = [(start + timedelta(days=i)) for i in range((end-start).days+1)]
            tour_item = TourItem.objects.filter(Q(d_date1__range=[start, end]))

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
    return render(request, template_name, context)





