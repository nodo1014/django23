from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages


# 원형: 템플릿 없이, 반환
# def index(request):
#     return HttpResponse('<head>헤드</head><body>바디</body>')

def index(request):
    qs = [i for i in range(9) if i%2 == 0]
    dict = {k:v for k,v in enumerate(qs)}
    messages.add_message(request, messages.INFO, '나의 체육관에 온 것을 환영해.')
    return render(request, "blog1/index.html", {
        'qs': qs,
        'dict': dict
    })