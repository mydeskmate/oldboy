from django.shortcuts import render,redirect,HttpResponse
import pymysql

def classes(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,'classes.html',{'class_list':class_list})

def add_class(request):
    if request.method == "GET":
        return render(request,'add_class.html')
    else:
        print(request.POST)
        v = request.POST.get('title')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into class(title) values(%s)",[v,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes/')

def del_class(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',
                           charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where id=%s", [nid, ])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes/')

def edit_class(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id,title from class where id=%s", [nid,])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request, 'edit_class.html',{'result':result})
    else:
        nid = request.GET.get('nid')
        title = request.POST.get('title')
        print(nid, title)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set title=%s where id=%s", [title, nid,])
        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/classes/')

from utils import dbhelper
def students(request):
    students_list = dbhelper.get_list("select student.id,student.name,class.title from student left join class on student.class_id=class.id",[])
    return render(request,'students.html',{'students_list':students_list})

def add_students(request):
    if request.method == 'GET':
        class_list = dbhelper.get_list("select id,title from class",[])
        return render(request,'add_students.html',{'class_list':class_list})
    else:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        dbhelper.modify("insert into student(name,class_id) value (%s,%s)",[name,class_id,])
        return redirect('/students/')

def del_students(request):
    nid = request.GET.get('nid')
    dbhelper.modify('delete from student where id=%s',[nid,])
    return redirect('/students/')

def edit_students(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        # 此处需要用户的class_id, 页面中需要拿来和class中的id进行比较
        student_info = dbhelper.get_one('select id,name,class_id from student where id=%s',[nid,])
        class_list = dbhelper.get_list('select id,title from class',[])
        return render(request,'edit_students.html',{'student_info':student_info,'class_list':class_list})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        dbhelper.modify('update student set name=%s,class_id=%s where id=%s',[name,class_id,nid,])
        return redirect('/students/')

# ############################ 对话框 ############################

def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        dbhelper.modify('insert into class(title) values(%s)',[title,])
        return HttpResponse('OK')
    else:
        return HttpResponse('班级标题不能为空')

def del_class_ajax(request):
    nid = request.POST.get('nid')
    print(nid)
    dbhelper.modify("delete from class where id=%s", [nid, ])
    return HttpResponse('OK')


def edit_class_ajax(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        current_class = dbhelper.get_one("select id,title from class where id=%s", [nid,])
        return render(request,'edit_class_ajax.html',{'current_class':current_class})
    else:
        nid = request.POST.get('nid')
        title = request.POST.get('title')
        dbhelper.modify("update class set title=%s where id=%s", [title, nid,])
        return HttpResponse("OK")


def edit_class_ajax2(request):
    pass
