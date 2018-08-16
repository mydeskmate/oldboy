from django.shortcuts import render,HttpResponse,redirect
from django.forms import Form
from django.forms import fields
from django.forms import widgets
from app01 import models
from utils.pager import PageInfo


# Create your views here.
def index(request,*args,**kwargs):

    # if type_id:
    #     article_list = models.Article.objects.filter(article_type_id=type_id)
    # else:
    #     article_list = models.Article.objects.all()

    username = request.session.get('username')
    nickname = request.session.get('nickname')
    if not username:
        session_stat = 0
    else:
        session_stat = 1

    #分类查找文章表
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    condition = {}
    if type_id:
        condition['article_type_id'] = type_id

    article_list = models.Article.objects.filter(**condition)
    article_type_choices = models.Article.type_choices

    #分页
    all_count = article_list.count()
    page_info = PageInfo(request.GET.get('page'),all_count,10,'/index.html',11)
    article_list_page = article_list[page_info.start():page_info.end()]

    return render(
        request,
        'index.html',
        {
            'article_type_choices':article_type_choices,
            'type_id': type_id,
            'article_list_page':article_list_page,
            'page_info':page_info,
            'session_stat':session_stat,
            'nickname':nickname
        },
    )

class LoginForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=3,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'不能少于6位',
            'max_length':'不能多于18位'
        },
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password = fields.CharField(
        min_length=6,
        error_messages={
            'required':'密码不能为空',
            'min_length':'密码不能少于8位'
        },
        widget=widgets.PasswordInput(attrs={'class':'form-control'})
    )
    code = fields.CharField(widget=widgets.TextInput(attrs={'class':'form-control'}))


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method == 'GET':
        obj = LoginForm()
        return render(request,'login.html',{'obj':obj})
    else:
        obj = LoginForm(request.POST)
        input_code = request.POST.get('code')
        session_code = request.session.get('code')

        if obj.is_valid():
            if input_code.upper() == session_code:
                obj.cleaned_data.pop('code')
                print(obj.cleaned_data)
                res = models.UserInfo.objects.filter(**obj.cleaned_data).first()

                if res:
                    request.session['username'] = res.username
                    request.session['nickname'] = res.nickname
                    return redirect('/')
                else:
                    return render(request, 'login.html', {'obj': obj})
            else:
                return render(request, 'login.html', {'obj': obj,'msg':'验证码不正确'})
        else:
            return render(request, 'login.html', {'obj': obj})



def check_code(request):
    from io import BytesIO
    from utils.random_check_code import rd_check_code

    img, code = rd_check_code()
    stream = BytesIO()
    img.save(stream, 'png')
    request.session['code'] = code
    return HttpResponse(stream.getvalue())


# self  放弃
# class RegisterForm(Form):
#     username = fields.CharField(
#         max_length=18,
#         min_length=3,
#         error_messages={
#             'required': '用户名不能为空',
#             'min_length': '不能少于3位',
#             'max_length': '不能多于18位'
#         },
#         widget=widgets.TextInput(attrs={'class': 'form-control'})
#     )
#     password = fields.CharField(
#         min_length=6,
#         error_messages={
#             'required': '密码不能为空',
#             'min_length': '密码不能少于8位'
#         },
#         widget=widgets.PasswordInput(attrs={'class': 'form-control'})
#     )
#     nickname = fields.CharField(max_length=32,widget=widgets.TextInput(attrs={'class': 'form-control'}))
#     email = fields.EmailField(widget=widgets.EmailInput(attrs={'class': 'form-control'}))

from app01.forms import RegisterForm
from django.core.exceptions import NON_FIELD_ERRORS

import os
def register(request):
    if request.method == 'GET':
        obj = RegisterForm(request)
        return render(request,'register.html',{'obj':obj})
    else:
        obj = RegisterForm(request,request.POST,request.FILES)
        if obj.is_valid():
            pass
        else:
            # print(obj.errors['__all__'])
            # print(obj.errors[NON_FIELD_ERRORS])
            pass
        return render(request,'register.html',{'obj':obj})




