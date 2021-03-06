from django.shortcuts import render,redirect,HttpResponse
import pymysql
import json
import time


def auth(func):
    def wrapper(request):
        tk = request.get_signed_cookie('ticket', salt='jjjjjj')
        if not tk:
            return redirect('/login/')
        res = func(request)
        return res

    return wrapper

@auth
def classes(request):
    # tk = request.COOKIES.get('ticket')
    # tk = request.get_signed_cookie('ticket',salt='jjjjjj')
    # if not tk:
    #     return redirect('/login/')

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='student_management',charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request,'classes.html',{'class_list':class_list})


@auth
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

@auth
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


@auth
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

@auth
def students(request):
    students_list = dbhelper.get_list("select student.id,student.name,student.class_id,class.title from student left join class on student.class_id=class.id",[])
    class_list =dbhelper.get_list("select id,title from class",[])           # 需要ID,添加时需要传递id
    return render(request,'students.html',{'students_list':students_list,'class_list':class_list})


@auth
def add_students(request):
    if request.method == 'GET':
        class_list = dbhelper.get_list("select id,title from class",[])
        return render(request,'add_students.html',{'class_list':class_list})
    else:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        dbhelper.modify("insert into student(name,class_id) value (%s,%s)",[name,class_id,])
        return redirect('/students/')

@auth
def del_students(request):
    nid = request.GET.get('nid')
    dbhelper.modify('delete from student where id=%s',[nid,])
    return redirect('/students/')


@auth
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


@auth
def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        dbhelper.modify('insert into class(title) values(%s)',[title,])
        return HttpResponse('OK')
    else:
        return HttpResponse('班级标题不能为空')

@auth
def del_class_ajax(request):
    nid = request.POST.get('nid')
    print(nid)
    dbhelper.modify("delete from class where id=%s", [nid, ])
    return HttpResponse('OK')


@auth
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


@auth
def modal_edit_class(request):
    ret = {'status': True, 'message': None}
    try:
        nid = request.POST.get('nid')
        title = request.POST.get('title')
        dbhelper.modify('update class set title=%s where id=%s',[title,nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = '处理异常'
    return HttpResponse(json.dumps(ret))


@auth
def modal_add_student(request):
    ret = {'status':True, 'message':None}
    name = request.POST.get('name')
    classId = request.POST.get('classId')
    print(name)
    print(classId)
    try:
        dbhelper.modify('insert into student (name,class_id) values (%s,%s)',[name,classId,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))


@auth
def modal_edit_student(request):
    ret = {'status':True,'message':None}
    try:
        nid = request.POST.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        dbhelper.modify('update student set name=%s,class_id=%s where id=%s',[name,class_id,nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def modal_del_student(request):
    ret = {'status':True,'message':None}
    try:
        nid = request.POST.get('nid')
        dbhelper.modify('delete from student where id=%s',[nid,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

# 多对多，以老师表展示

@auth
def teacher(request):
    teacher_list = dbhelper.get_list('''
    select teacher.id as tid,teacher.name,class.title from teacher 
	left join teacher2class on teacher.id=teacher2class.teacher_id
	left join class on teacher2class.class_id=class.id
	''',[])
    result = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['titles'].append(row['title'])
        else:
            result[tid] = {'tid':tid,'name':row['name'],'titles':[row['title'],]}
    return render(request,'teacher.html',{'teacher_list':result.values()})


@auth
def add_teacher(request):
    if request.method == 'GET':
        class_list = dbhelper.get_list('select * from class',[])
        return render(request,'add_teacher.html',{'class_list':class_list})
    else:
        name = request.POST.get('name')
        selected_class = request.POST.getlist('class_id')
        tid = dbhelper.modify('insert into teacher (name) values (%s)', [name, ])
        # 多次连接,多次提交
        # for class_id in selected_class:
        #     dbhelper.modify('insert into teacher2class (teacher_id,class_id) values (%s,%s)',[last_rowid,class_id,])
        # 一次连接,一次提交
        print(selected_class)
        # data_list = []  #[(17, '9'), (17, '12')]
        # for class_id in selected_class:
        #     temp = (tid,class_id)
        #     data_list.append(temp)

        data_list = [(tid,class_id) for class_id in selected_class]
        print(data_list)
        obj = dbhelper.DbHelper()
        obj.multiple_modify('insert into teacher2class(teacher_id,class_id) values(%s,%s)',data_list)
        obj.close()
        return redirect('/teacher/')


@auth
def edit_teacher(request):
    if request.method == 'GET':
        tid = request.GET.get('tid')
        obj = dbhelper.DbHelper()
        teacher_info = obj.get_one('select id,name from teacher where id=%s',[tid,])
        class_list = obj.get_list('select id,title from class',[])
        t_class_id = obj.get_list('select class_id from teacher2class where teacher_id=%s',[tid,])
        obj.close()
        temp = [item['class_id'] for item in t_class_id]
        return render(request,'edit_teacher.html',{'teacher_info':teacher_info,'class_list':class_list,'t_class_id':temp})
    else:
        tid = request.GET.get('tid')
        name = request.POST.get('name')
        class_list = request.POST.getlist('class_id')
        obj = dbhelper.DbHelper()
        obj.modify('update teacher set name=%s where id=%s',[name,tid,])
        obj.modify('delete from teacher2class where teacher_id=%s',[tid,])
        data_list = [(tid, class_id) for class_id in class_list]
        obj.multiple_modify('insert into teacher2class(teacher_id,class_id) values(%s,%s)',data_list)
        obj.close()
        return redirect('/teacher/')


@auth
def del_teacher(request):
    tid = request.GET.get('tid')
    obj = dbhelper.DbHelper()
    obj.modify('delete from teacher2class where teacher_id=%s',[tid,])
    obj.modify('delete from teacher  where id=%s',[tid,])
    return redirect('/teacher/')


@auth
def get_all_class(request):
    obj = dbhelper.DbHelper()
    class_list = obj.get_list('select id,title from class',[])
    obj.close()
    # print(class_list)
    time.sleep(5)
    return HttpResponse(json.dumps(class_list))


@auth
def modal_add_teacher(request):
    name = request.POST.get('name')
    selected_class = request.POST.getlist('class_ids')
    ret = {'status': True, 'message': None}
    try:
        tid = dbhelper.modify('insert into teacher (name) values (%s)', [name, ])
        data_list = [(tid, class_id) for class_id in selected_class]
        obj = dbhelper.DbHelper()
        obj.multiple_modify('insert into teacher2class(teacher_id,class_id) values(%s,%s)', data_list)
        obj.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = '处理异常'
    return HttpResponse(json.dumps(ret))


@auth
def get_teacher_class(request):
    tid = request.POST.get('tid')
    obj = dbhelper.DbHelper()
    class_ids = obj.get_list('select id,title from class',[])
    tea_class_id = obj.get_list('select class_id from teacher2class where teacher_id=%s',[tid,])
    tea_class_id = [item['class_id'] for item in tea_class_id]
    class_info = {'class_ids':class_ids,'tea_class_id':tea_class_id}
    obj.close()
    return HttpResponse(json.dumps(class_info))


@auth
def modal_edit_teacher(request):
    ret = {'status':True,'message':None}
    try:
        tid = request.POST.get('tid')
        name = request.POST.get('name')
        class_id = request.POST.getlist('class_id')

        obj = dbhelper.DbHelper()
        obj.modify('update teacher set name=%s where id=%s',[name,tid,])
        obj.modify('delete from teacher2class where teacher_id=%s',[tid,])
        data_list = [(tid,cls_id) for cls_id in class_id]
        obj.multiple_modify('insert into teacher2class(teacher_id,class_id) values(%s,%s)',data_list)
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))



def layout(request):
    return render(request,'layout.html')

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == 'han' and pwd == '123':
            obj = redirect('/classes/')
            print(obj)
            # obj.set_cookie('ticket','adfasdfsdfdsfd')
            obj.set_signed_cookie('ticket','123123',salt='jjjjjj')
            return obj
        else:
            return render(request,'login.html')

