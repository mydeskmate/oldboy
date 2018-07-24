from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        sex = request.POST.get('render')
        no_login = request.POST.get('no-login')

        # print(user,pwd,sex)
        if sex == "0":
            ret = models.Boy.objects.filter(name=user,password=pwd).first()
        else:
            ret = models.Girl.objects.filter(name=user, password=pwd).first()
        if ret:
            request.session['id'] = ret.id
            request.session['name'] = ret.name
            request.session['gender'] = sex
            return redirect('/index.html')
        else:
            return render(request,'login.html')

def auth(func):
    def wrapper(request,*args,**kwargs):
        v = request.session.get('name')
        if not v:
            return redirect('/login.html')
        res = func(request,*args,**kwargs)
        return res
    return wrapper

@auth
def index(request):
    return render(request,'index.html')
