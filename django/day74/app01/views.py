from django.shortcuts import render,HttpResponse,redirect
from app01 import models
# Create your views here.
def test(request):
    # models.UserInfor.objects.create(username='root',email='ddddddd')
    # models.UserInfor.objects.create(username='xxx',email='xxx',ctime='2017-4-3')


    # return HttpResponse('......')
    return render(request,'test.html',{'name':'fangshaowei'})


def login(request):
    if request.method == "GET":
        return render(request,'login.html')
    else:
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        if u == 'alex' and p == '123':
            request.session['username'] = 'alex'
            request.session['email'] = 'dfd@qq.com'
            return redirect('/index/')
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误'})

def index(request):
    v = request.session.get('username')
    if v:
        return HttpResponse('登录成功')
    else:
        return redirect('/login/')