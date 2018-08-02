from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.forms import Form
from django.forms import fields


# Create your views here.
class ClassForm(Form):
    title = fields.RegexField('全栈/d+')

def class_list(request):
    if request.method == 'GET':
        cls_list = models.Classes.objects.all()
        return render(request,'class_list.html',{'cls_list':cls_list})

def add_class(request):
    if request.method == 'GET':
        obj = ClassForm()
        return render(request,'add_class.html',{'obj':obj})