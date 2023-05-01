from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from main.models  import Bus
# Create your views here.

#---------예매
# def seat(request):

#     if request.method == 'POST':
#         date=request.POST['date']
#         chk_list = []
#         i=1
#         while i<10:
#             bus_number=get_object_or_404(Bus, number=i, date=date)
#             if bus_number.check==1:
#                 chk_list.append("disabled")
#             if bus_number.check!=1:
#                 chk_list.append("")
#             i=i+1
#         return render(request,'seat.html',{'list':chk_list, 'date':date})
#     return render(request,'seat.html')

#------------------예매 취소

# def seat_cancel(request):

#     chk_list = []
#     i=1
#     while i<10:
#         bus_number=get_object_or_404(Bus, number=i)
#         if bus_number.check==1:
#             chk_list.append("")
#         if bus_number.check!=1:
#             chk_list.append("disabled")
#         i=i+1

#     return render(request,'seat_cancel.html',{'list':chk_list})

#-----------------좌석 선택

def chk(request):
    #폼 입력값 가져오기
    if request.method == 'POST':
        selected = request.POST.getlist('answer[]')
        date=request.POST['date']
        user=request.POST['user']

        for select in selected:
            number=get_object_or_404(Bus, number=select, date=date)
            number.check+=1
            number.user=user
            number.save()

        return redirect('date')

    return redirect('date')

def chk_cancel(request):
    #폼 입력값 가져오기
    if request.method == 'POST':
        selected = request.POST.getlist('answer[]')
        date=request.POST['date']
        user=request.POST['user']

        for select in selected:
            number=get_object_or_404(Bus, number=select, date=date, user=user)
            number.check-=1
            number.user=""
            number.save()

        return redirect('date')

    return redirect('date')

#-------------------날짜 선택

def select_date(request):
    #폼 입력값 가져오기

    date=request.POST['date']
    user=request.POST['user']

    if Bus.objects.filter(date__contains='{}'.format(date)).count()>0:
        chk_list = []
        i=1
        while i<10:
            bus_number=get_object_or_404(Bus, number=i, date=date)
            if bus_number.check==1:
                chk_list.append("disabled")
            if bus_number.check!=1:
                chk_list.append("")
            i=i+1
        return render(request,'seat.html',{'list':chk_list, 'date':date})

    else:
        i=1
        while i<10:
            bus=Bus()
            bus.number=i
            bus.check=0
            bus.date=date
            bus.save()
            i=i+1
        
        return render(request,'seat.html',{'date':date, 'user':user})

def cancel_date(request):
    #폼 입력값 가져오기
    date=request.POST['date']
    user=request.POST['user']

    chk_list = []
    i=1
    while i<10:
        bus_number=get_object_or_404(Bus, number=i, date=date)
        if bus_number.check==1:
            chk_list.append("")
        if bus_number.check!=1:
            chk_list.append("disabled")
        i=i+1

    return render(request,'seat_cancel.html',{'list':chk_list, 'date':date, 'user':user})

def date(request):

    return render(request,'date.html')


#--------------------------로그인, 로그아웃

# Create your views here.

from django.contrib.auth.forms import User
from django.contrib.auth.views import LoginView
from django.contrib import auth
from main.forms import UserForm
from main.forms import LoginForm
from django.contrib.auth.views import LogoutView

def signup(request):
    if request.method == "POST":
        new_user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        auth.login(request, new_user)
        return redirect('date')
        
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        username=request.POST.get('username',None)
        password=request.POST.get('password',None)
        user=auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('date')
        else:
            return HttpResponse('Login failed. Try again.')
    else:
        return render(request, 'login.html')

#--------------------------마이페이지

def mypage(request):
    if request.method == "POST":
        user=request.POST['user']
        info=Bus.objects.filter(user__contains='{}'.format(user))
        return render(request,'mypage.html',{'info':info, 'user':user})