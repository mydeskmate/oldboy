from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    return render(request,'index.html')

def add1(request):
    a1 = int(request.POST.get('i1'))
    a2 = int(request.POST.get('i2'))
    print(a1,a2)
    return HttpResponse(a1 + a2)


def add2(request):
    if request.method == 'GET':
        # import time
        # time.sleep(10)
        i1 = int(request.GET.get('i1'))
        i2 = int(request.GET.get('i2'))
        print('add2.......')
        return HttpResponse(i1+i2)
    else:
        print(request.POST)
        return HttpResponse('....')

def autohome(request):
    return render(request,'autohome.html')

def fake_ajax(request):
    if request.method == 'GET':
        return render(request,'fake_ajax.html')
    else:
        print(request.POST)
        return HttpResponse('返回值')

import os
def upload(request):
    if request.method == "GET":
        return render(request,'upload.html')
    else:
        print(request.POST,request.FILES)
        file_obj = request.FILES.get('fafafa')
        file_path = os.path.join('static',file_obj.name)
        with open(file_path,'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return HttpResponse(file_path)