from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from django.forms import Form
from django.forms import fields
class LoginForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=6,
        required=True,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'不能少于6位',
            'max_length':'不能大于18位',
        }
    )
    password = fields.CharField(
        min_length=16,
        required=True,
        error_messages={
            'required':'密码不能为空',
            'min_length':'不能少于16位',
        })

class RegisterForm(Form):
    username = fields.CharField(
        max_length=18,
        min_length=6,
        required=True,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'不能少于6位',
            'max_length':'不能大于18位',
        }
    )

    password = fields.CharField(
        min_length=16,
        required=True,
        error_messages={
            'required':'密码不能为空',
            'min_length':'不能少于16位',
        })

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        obj = LoginForm(request.POST)
        if obj.is_valid():
            print(obj.cleaned_data)
            return redirect('http://www.baidu.com')
        else:
            return render(request,'login.html',{'obj':obj})

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
