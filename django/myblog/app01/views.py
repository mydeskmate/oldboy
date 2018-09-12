from django.shortcuts import render,redirect,HttpResponse
from app01 import models

# Create your views here.
def login(request):
    return render(request,'login.html')


def index(request,*args,**kwargs):
    """
    首页
    :param request:
    :param args:
    :param kwargs: 接受类别id
    :return:
    """
    type_choice_list = models.Article.type_choices

    #分类查找文章
    condition = {}
    #注意此处需要转换成int，否则比较不成功
    type_id = int(kwargs.get('type_id')) if kwargs.get('type_id') else None
    if type_id:
        condition['article_type_id'] = type_id
    article_list = models.Article.objects.filter(**condition)

    return render(
        request,
        'index.html',
          {
              'type_choice_list': type_choice_list,
              'article_list':article_list,
              'type_id':type_id
          }
    )
