from django.shortcuts import render,HttpResponse
from app01 import models
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
# Create your views here.

def index(request):
    current_page = request.GET.get('page')
    user_list = models.UserInfo.objects.all()
    paginator = Paginator(user_list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e:
        posts = paginator.page(1)
    except EmptyPage as e:
        posts = paginator.page(1)

    # for i in range(300):
    #     name = 'root' + str(i)
    #     models.UserInfo.objects.create(name=name,age=18,ut_id=1)
    return render(request,'index.html',{'posts':posts})

def test(request):
    # models.UserType.objects.create(title='普通用户')
    # models.UserType.objects.create(title='二笔用户')
    # models.UserType.objects.create(title='牛逼用户')

    # models.UserInfo.objects.create(name='方少伟',age=18,ut_id=1)
    # models.UserInfo.objects.create(name='由秦兵',age=18,ut_id=2)
    # models.UserInfo.objects.create(name='刘庚',age=18,ut_id=2)
    # models.UserInfo.objects.create(name='陈涛',age=18,ut_id=3)
    # models.UserInfo.objects.create(name='王者',age=18,ut_id=3)
    # models.UserInfo.objects.create(name='杨涵',age=18,ut_id=1)
    # result = models.UserInfo.objects.all()
    # for obj in result:
    #     print(obj.name, obj.age,obj.ut_id,obj.ut.title)
    # result = models.UserInfo.objects.all().values('id','name','ut__title')
    # for item in result:
    #     print(item['id'],item['name'],item['ut__title'])

    # obj = models.UserInfo.objects.all().first()
    # print(obj.name,obj.age,obj.ut.title)

    # models.UserInfo.objects.filter(id__gt=6).delete()
    # result = models.UserInfo.objects.all().values('id','name')
    # for row in result:
    #     print(row)


    # result = models.UserInfo.objects.all().values_list('id','name')
    # for row in result:
    #     print(row)

    # result = models.UserInfo.objects.all().values('id','name','ut__title')
    # for item in result:
    #     print(item['id'],item['name'],item['ut__title'])

    # v1 = models.UserType.objects.values('id','title')
    # print(v1)

    # v2 = models.UserType.objects.values('id','title','userinfo__name')
    # print(v2)

    # v1 = models.UserInfo.objects.all().order_by('-id')
    # print(v1)

    from django.db.models import Count,Sum,Max,Min
    # v = models.UserInfo.objects.values('ut__id').annotate(xxx=Count('id')).filter(xxx__gt=2)
    # print(v.query)

    # from django.db.models import F
    # models.UserInfo.objects.all().update(age=F("age")+2)
    #
    # from django.db.models import Q
    # # v = models.UserInfo.objects.filter(Q(id=2) | Q(id=4))
    # v = models.UserInfo.objects.filter(Q(id=1) | Q(id=3))
    # print(v)
    from django.db.models import Q
#     con = Q()
#     q1 = Q()
#     q1.connector = "OR"
#     q1.children.append(('id',1))
#     q1.children.append(('id',3))
#     q1.children.append(('id',5))
#     q1.children.append(('id',6))
#
#     q2 = Q()
#     q2.connector = "OR"
#     q2.children.append(('id',1))
#     q2.children.append(('id',4))
#     q2.children.append(('id',5))
#
#     q3 = Q()
#     q3.connector = 'AND'
#     q3.children.append(('id',6))
#     q2.add(q3,'OR')
#     print(q3)
#     print(q2)
#     print(q1)
#
#     con.add(q1,'AND')
#     con.add(q2,'AND')
#     print(con)
# # (1 OR 3 OR 5  OR 6  ) AND  ( 1 OR 4 OR 5 OR (6))
#     v = models.UserInfo.objects.filter(con)
#     print(v)

    # condition_dict = {
    #     'k1':[1,2,3,4],
    #     'k2':[1,2,],
    # }
    # con = Q()
    # for k,v in condition_dict.items():
    #     q = Q()
    #     q.connector = 'OR'
    #     for i in v:
    #         q.children.append(('id',i))
    #     con.add(q,'AND')
    # print(con)
    # v = models.UserInfo.objects.filter(con)
    # print(v)
    # v = models.UserInfo.objects.all().extra(
    #     select={
    #         'n':"select count(1) from app01_usertype where id=%s or id=%s",
    #         'm':"select count(1) from app01_usertype where id=%s or id=%s",
    #     },
    #     select_params=[1,2,3,4]
    # )
    # for obj in v:
    #     print(obj.name,obj.age,obj.n)

    # v = models.UserInfo.objects.extra(
    #     where=['id=%s','name=%s'],
    #     params=[1,"方少伟"]
    # )
    #
    # for obj in v:
    #     print(obj.name,obj.age)
    #

    # v = models.UserInfo.objects.extra(
    #     tables=['app01_usertype'],
    # )
    # # for obj in v:
    # #     print(obj.name,obj.ut.title)
    # print(v.query)

    # result = models.UserInfo.objects.aggregate(k=Count('ut_id'),n=Count('id'))
    # print(result)

    # objs = [
    #     models.UserInfo(name='r11',age=19,ut_id=1),
    #     models.UserInfo(name='r12',age=20,ut_id=2),
    # ]
    # models.UserInfo.objects.bulk_create(objs,10)

    name_map = {'title':'name'}
    v1 = models.UserInfo.objects.raw('SELECT id,title FROM app01_usertype',translations=name_map)
    for i in v1:
        print(i,type(i))

    return HttpResponse('l...............')