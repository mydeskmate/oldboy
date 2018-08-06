from django.shortcuts import render,HttpResponse,redirect
from app01 import models
from django.forms import Form
from django.forms import fields
from django.forms import widgets

# Create your views here.
class ClassForm(Form):
    title = fields.RegexField('全栈\d+')

def class_list(request):
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
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    email = fields.EmailField(widget=widgets.TextInput(attrs={'class':'form-control'}))
    age = fields.IntegerField(min_value=18,max_value=40,widget=widgets.TextInput(attrs={'class':'form-control'}))
    cls_id = fields.IntegerField(
        widget=widgets.Select(choices=models.Classes.objects.values_list('id','title'),attrs={'class':'form-control'})
    )

def student_list(request):
    stu_list = models.Student.objects.all()
    return render(request,'student_list.html',{'stu_list':stu_list})

def add_student(request):
    if request.method == 'GET':
        obj = StudentForm()
        return render(request,'add_student.html',{'obj':obj})
    else:
        obj = StudentForm(request.POST)
        if obj.is_valid():
            models.Student.objects.create(**obj.cleaned_data)
            return redirect('/student_list/')
        return render(request,'add_student.html',{'obj':obj})

def edit_student(request,nid):
    if request.method == 'GET':
        row = models.Student.objects.filter(id=nid).values('name','email','age','cls_id').first()
        obj = StudentForm(initial=row)
        return render(request,'edit_student.html',{'nid':nid,'obj':obj})
    else:
        obj = StudentForm(request.POST)
        if obj.is_valid():
            models.Student.objects.filter(id=nid).update(**obj.cleaned_data)
            return redirect('/student_list/')
        return render(request,'edit_student.html',{'nid':nid,'obj':obj})

def teacher_list(request):
    tea_list = models.Teacher.objects.all()
    return render(request,'teacher_list.html',{'tea_list':tea_list})

from django.forms import Form
from django.forms import fields
from django.forms import models as from_model

class TeacherForm(Form):
    tname = fields.CharField(min_length=2)
    xx = fields.MultipleChoiceField(
        # choices=models.Classes.objects.values_list('id', 'title'),
        widget=widgets.SelectMultiple()
    )

    # 使用该方法
    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['xx'].choices = models.Classes.objects.values_list('id', 'title')


def add_teacher(request):
    if request.method == 'GET':
        obj = TeacherForm()
        return render(request,'add_teacher.html',{'obj':obj})
    else:
        obj = TeacherForm(request.POST)
        if obj.is_valid():
            xx = obj.cleaned_data.pop('xx')    #去掉班级表不需要的字段
            row = models.Teacher.objects.create(**obj.cleaned_data)
            row.c2t.add(*xx)
            return redirect('/teacher_list/')
        print(obj.errors)
        return render(request,'add_teacher.html',{'obj':obj})


def edit_teacher(request,nid):
    if request.method == "GET":
        row = models.Teacher.objects.filter(id=nid).first()
        class_ids = row.c2t.values_list('id')
        id_list = list(zip(*class_ids))[0] if list(zip(*class_ids)) else []
        obj = TeacherForm(initial={'tname':row.tname,'xx':id_list})
        return render(request,'edit_teacher.html',{'obj':obj})


from django.core.exceptions import ValidationError
class TestForm(Form):
    user = fields.CharField()
    pwd = fields.CharField()

    def clean_user(self):
        v = self.cleaned_data['user']
        if models.Student.objects.filter(name=v).count():
            raise ValidationError('用户名已经存在')
        return self.cleaned_data['user']

    def clean(self):
        user = self.cleaned_data.get('user')
        email = self.cleaned_data.get('email')
        if models.Student.objects.filter(user=user,email=email).count():
            raise ValidationError('用户名和邮箱联合已经存在')
        return self.cleaned_data

class F2Form(Form):
    user = fields.CharField()
    fafafa = fields.FileField()

def f2(request):
    if request.method == 'GET':
        obj = F2Form()
        return render(request,'f2.html',{'obj':obj})
    else:
        obj = F2Form(data=request.POST, files=request.FILES)
        if obj.is_valid():
            print(obj.cleaned_data.get('fafafa').name)
            import os
            file_obj = request.FILES.get('fafafa')
            f = open(os.path.join('static', file_obj.name), 'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
        return render(request,'f2.html',{'obj':obj})


def test(request):
    obj = TestForm()