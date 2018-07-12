from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.urls import reverse

# Create your views here.
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == 'han' and pwd == '123':
            obj = redirect('/app01/classes.html')
            print(obj)
            # obj.set_cookie('ticket','adfasdfsdfdsfd')
            obj.set_signed_cookie('ticket','123123',salt='jjjjjj')
            return obj
        else:
            return render(request,'login.html')

def auth(func):
    def wrapper(request,*args,**kwargs):
        tk = request.get_signed_cookie('ticket', salt='jjjjjj')
        if not tk:
            return redirect('/login.html')
        res = func(request,*args,**kwargs)
        return res

    return wrapper

@auth
def classes(request):
    class_list = models.Class.objects.all()
    print(class_list)
    return render(request,'classes.html',{'class_list':class_list})

@auth
def add_class(request):
    if request.method == "GET":
        return render(request, 'add_class.html')
    else:
        title = request.POST.get('title')
        models.Class.objects.create(title='三班')
        return redirect('/app01/classes.html')

@auth
def del_class(request,a1):
    models.Class.objects.filter(id=a1).delete()
    return redirect('/app01/classes.html')

@auth
def edit_class(request,a1):
    if request.method == 'GET':
        obj = models.Class.objects.filter(id=a1)
        result = {'id':obj[0].id,'title':obj[0].title}
        return render(request,'edit_class.html',{'result':result})
    else:
        title = request.POST.get('title')
        models.Class.objects.filter(id=a1).update(title=title)
        return redirect(reverse('classes'))
