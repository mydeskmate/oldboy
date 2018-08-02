from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.forms import Form
from django.forms import fields
from django.forms import widgets

# Create your views here.
class ClassForm(Form):
    title = fields.RegexField('全栈\d+')

def class_list(request):
    if request.method == 'GET':
        cls_list = models.Classes.objects.all()
        return render(request,'class_list.html',{'cls_list':cls_list})

def add_class(request):
    if request.method == 'GET':
        obj = ClassForm()
        return render(request,'add_class.html',{'obj':obj})
    else:
        obj = ClassForm(request.POST)
        print(obj.is_valid())
        if obj.is_valid():
            models.Classes.objects.create(**obj.cleaned_data)
            print(obj.cleaned_data)
            return redirect('/class_list/')
        return render(request,'add_class.html',{'obj':obj})

def edit_class(request,nid):
    if request.method == 'GET':
        row = models.Classes.objects.filter(id=nid).first()
        obj = ClassForm(initial={'title':row.title})
        return render(request,'edit_class.html',{'nid':nid,'obj':obj})
    else:
        obj = ClassForm(request.POST)
        if obj.is_valid():
            models.Classes.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/class_list/')
        return render(request,'edit_class.html',{'nid':nid,'obj':obj})

class StudentForm(Form):
    name = fields.CharField(
        min_length=2,
        max_length=6,
        widget=widgets.TextInput()
    )

def student_list(request):
    pass