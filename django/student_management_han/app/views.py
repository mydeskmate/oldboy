from django.shortcuts import render,redirect,HttpResponse

from utils import sqlhelper
import pymysql
import json

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        name = request.POST.get('name')
        pwd = request.POST.get('pwd')
        obj = sqlhelper.SqlHelper()
        ret = obj.get_one('select * from admin where name=%s and password=%s',[name,pwd,])
        obj.close()
        if ret:
            return redirect('/index/')
        else:
            return render(request,'login.html',{'msg':"用户名或密码错误!"})

def index(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'index.html', {'class_list': class_list})

def classes(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,'classes.html',{'class_list':class_list})

def students(request):
    students_list = sqlhelper.get_list("select student.id,student.name,student.class_id,class.title from student left join class on student.class_id=class.id",[])
    class_list =sqlhelper.get_list("select id,title from class",[])           # 需要ID,添加时需要传递id
    return render(request,'students.html',{'students_list':students_list,'class_list':class_list})