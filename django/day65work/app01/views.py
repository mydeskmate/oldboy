import pymysql
from django.shortcuts import redirect, render

def teachers(request):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,name from teacher")
    teacher_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,'teachers.html',{'teacher_list':teacher_list})

def del_teacher(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from teacher where id=%s",[nid,])
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/teachers/')

def add_teacher(request):
    if request.method == "GET":
        return render(request,'add_teacher.html')
    else:
        name = request.POST.get('name')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into teacher(name) values(%s)",[name,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/teachers/')

def edit_teacher(request):
    if request.method == "GET":
        nid = request.GET.get("nid")
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select id, name from teacher where id=%s", [nid, ])
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return render(request,'edit_teacher.html',{'result':result})
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',
                               charset='utf8')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update teacher set name=%s where id=%s", [name,nid,])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/teachers/')

