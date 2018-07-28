from django.shortcuts import render,HttpResponse,redirect
from app01 import models
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        gender = request.POST.get('gender')
        rmb = request.POST.get('rmb')

        if gender == '1':
            obj = models.Boy.objects.filter(username=user,password=pwd).first()
        else:
            obj = models.Girl.objects.filter(username=user,password=pwd).first()
        if not obj:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            request.session['user_info'] = {'user_id':obj.id,'gender':gender,'username':user,'nickname':obj.nickname}
            return redirect('/index.html')

def logout(request):
    if request.session.get('user_info'):
        # request.session.delete(request.session.session_key)
        request.session.clear()
    return redirect('/login.html')