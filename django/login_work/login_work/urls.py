"""login_work URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.shortcuts import HttpResponse,render,redirect
import pymysql
def login(request):
    """
    处理用户登录请求,返回内容
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request,'login.html')
    else:
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        print(u)
        print(p)
        conn = pymysql.connect(host="localhost",user="root",password="123456",database="school")
        cursor = conn.cursor()
        sql = "select * from user where name=%s and password=%s"
        cursor.execute(sql,[u,p])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return redirect('/index/')
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误'})

def index(request):
    conn = pymysql.connect(host="localhost",user='root',password='123456',database='school')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select name,password from user"
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(
        request,
        'index.html',
        {
            'user_list':result
        }
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login),
    path('index/', index),
]
