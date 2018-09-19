from django.shortcuts import render,redirect,HttpResponse
from app01 import models
from app01.forms import RegisterForm
from app01.forms import LoginForm
from django.db.models import Count
from django.db.models import F
import json

# Create your views here.
def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == "GET":
        obj = LoginForm()
        return render(request, 'login.html',{'obj':obj})
    else:
        obj = LoginForm(request.POST)
        if obj.is_valid():
            res = models.UserInfo.objects.filter(**obj.cleaned_data).first()
            if res:
                request.session['user_info'] = {'username':res.username,'nickname':res.nickname}
                # 此处存放多个session会好一点， 但如果存放的数据比较多， 放在字典里面比较好
                # request.session['username'] = res.username
                # request.session['nickname'] = res.nickname
                return redirect('/')
            else:
                return render(request,'login.html',{'obj':obj,'msg':'用户名或密码错误'})
        else:
            return render(request,'login.html',{'obj':obj})

def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    if request.session.get('user_info'):
        request.session.clear()
    return redirect('/index.html/')

def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == 'GET':
        obj = RegisterForm(request)
        return render(request,'register.html',{'obj':obj})
    else:
        obj = RegisterForm(request,request.POST)
        if obj.is_valid():
            pass
        else:
            pass
        return render(request,'register.html',{'obj':obj})


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    from io import BytesIO
    from utils.random_check_code import rd_check_code
    img,code = rd_check_code()
    stream = BytesIO()
    img.save(stream,'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())

def index(request,*args,**kwargs):
    """
    首页
    :param request:
    :param args:
    :param kwargs: 接受类别id
    :return:
    """
    # 获取session 判断是否登录
    user_info = request.session.get('user_info')
    if not user_info:
        login_stat = 0
        username = None
    else:
        login_stat = 1
        username = user_info.get('username')
        nickname = user_info.get('nickname')

    type_choice_list = models.Article.type_choices

    #分类查找文章
    condition = {}
    #注意此处需要转换成int，否则比较不成功
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    if type_id:
        condition['article_type_id'] = type_id
    article_list = models.Article.objects.filter(**condition)

    # 获取该用户的博客信息
    blog = models.Blog.objects.filter(user__username=username).first()

    return render(
        request,
        'index.html',
          {
              'type_choice_list': type_choice_list,
              'article_list':article_list,
              'type_id':type_id,
              'login_stat':login_stat,
              'user_info':user_info,
              'blog':blog,
          }
    )

def home(request,site):
    """
    访问博客主页
    :param request:
    :param site: 个人博客后缀
    :return:
    """
    blog = models.Blog.objects.filter(site=site).first()
    # 访问博客不存在,跳转到主页
    if not blog:
        return redirect('/')

    # 按照分类,标签,时间分类
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values("category_id","category__title").annotate(ct=Count("nid"))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id',"tag__title").annotate(ct=Count("id"))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(select={'ctime':"strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count("nid"))

    # 显示文章, 此处未分页 ,稍后处理
    article_list = models.Article.objects.all()

    # 博客主题

    return render(
        request,
        'home.html',
        {
            'blog':blog,
            'category_list':category_list,
            'tag_list':tag_list,
            'date_list':date_list,
            'article_list':article_list,
        }
    )

def filter(request,site,key,val):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 按照分类,标签,时间分类
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values("category_id", "category__title").annotate(
        ct=Count("nid"))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', "tag__title").annotate(
        ct=Count("id"))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'ctime': "strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count("nid"))

    # 根据分类,标签,时间筛选文章
    if key == 'category':
        article_list = models.Article.objects.filter(blog=blog,category_id=val)
    elif key == 'tag':
        # 直接跨到tag表
        article_list = models.Article.objects.filter(blog=blog,tags__nid=val)
    else:
        article_list = models.Article.objects.filter(blog=blog).extra(where=["strftime('%%Y-%%m',create_time)=%s"],params=[val,])

    return render(
        request,
        'filter.html',
        {
            'blog':blog,
            'category_list':category_list,
            'tag_list':tag_list,
            'date_list':date_list,
            'article_list':article_list,
        }
    )

def article(request,site,nid):
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')

    # 按照分类,标签,时间分类
    # 分类
    category_list = models.Article.objects.filter(blog=blog).values("category_id", "category__title").annotate(
        ct=Count("nid"))

    # 标签
    tag_list = models.Article2Tag.objects.filter(article__blog=blog).values('tag_id', "tag__title").annotate(
        ct=Count("id"))

    # 时间
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'ctime': "strftime('%%Y-%%m',create_time)"}).values('ctime').annotate(ct=Count("nid"))

    # 获取指定文章
    obj = models.Article.objects.filter(blog=blog,nid=nid).first()

    return render(
        request,
        'article.html',
        {
            'blog': blog,
            'category_list': category_list,
            'tag_list': tag_list,
            'date_list': date_list,
            'obj':obj,
        }
    )

def up(request):
    """
    处理赞和踩
    :param request:
    :return: 返回赞或踩得status值  1 赞  2 踩  0 表示出错
    """
    respone = {'status':0,'msg':None}

    try:
        user_id = request.session.get('user_id')
        article_id = request.POST.get('nid')
        val = int(request.POST.get('val'))
        obj = models.UpDown.objects.filter(user_id=user_id,article_id=article_id).first()
        if obj:
            # 已经赞或者踩过
            print(1111)
            pass
        else:
            print(2222)
            from django.db import transaction
            with transaction.atomic():
                print(val)
                if val:
                    print(4444)
                    print(user_id)
                    print(article_id)
                    models.UpDown.objects.create(user_id=user_id,article_id=article_id,up=True)
                    models.Article.objects.filter(nid=article_id).update(up_count=F('up_count')+1)
                    respone['status'] = 1
                else:
                    print(3333)
                    print(user_id)
                    print(article_id)
                    models.UpDown.objects.create(user_id=user_id,article_id=article_id,up=False)
                    models.Article.objects.filter(nid=article_id).update(down_count=F('down_count')+1)
                    respone['status'] = 2

    except Exception as e:
        respone['msg'] = str(e)
    print(respone)
    return HttpResponse(json.dumps(respone))