from django.shortcuts import render,HttpResponse,redirect
from app01 import models

# Create your views here.
def index(request):
    """
    首页
    :param request:
    :return:
    """
    article_list = models.Article.objects.all()
    return render(request,'index.html',{'article_list':article_list})