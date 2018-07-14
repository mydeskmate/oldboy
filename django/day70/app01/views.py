from django.shortcuts import render,HttpResponse,render
from app01 import models

def test(request):
    models.UserType.objects.create(title='普通用户')
    models.UserType.objects.create(title='二笔用户')
    models.UserType.objects.create(title='牛逼用户')

    return HttpResponse('........')
# Create your views here.
def index(request):
    user_list = [
        1,2,3
    ]
    return render(request,'index.html',{'user_list':user_list})

def edit(request,a1):
    print(a1)
    return HttpResponse('....')





from django.views import View
class Login(View):
    def get(self,request):
        # return HttpResponse('login.get')
        return render(request,'login.html')

    def post(self,request):
        return HttpResponse('Login.post')
# def edit(request,*args,**kwargs):
#     print(args,**kwargs)
#     return HttpResponse('...')