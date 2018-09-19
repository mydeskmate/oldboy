from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError

class RegisterForm(Form):
    """
    注册Form
    """
    username = fields.CharField(
        min_length=5,
        max_length=32,
        error_messages={
            'required':'用户名不能为空',
            'min_length':'用户名不能少于5位',
            'max_length':'用户名不能多于32位'
        },
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password = fields.CharField(
        min_length=6,
        max_length=32,
        error_messages={
            'required':'密码不能为空',
            'min_length':'密码不能少于6位',
            'max_length':'密码不能多于32位'
        },
        widget=widgets.PasswordInput(attrs={'class':'form-control'})
    )
    password2 = fields.CharField(
        error_messages={
            'required':'密码不能为空'
        },
        widget=widgets.PasswordInput(attrs={'class':'form-control'})
    )
    code = fields.CharField(
        error_messages={
            'required':'请输入验证码'
        },
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )


    def __init__(self,request,*args,**kwargs):
        """
        #定义init函数, 将request封装进来, 下面会用到self.request.session
        :param request:
        :param args:
        :param kwargs:
        """
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.request = request

    def clean_code(self):
        """
        验证验证码是否正确
        :return:
        """
        input_code = self.cleaned_data.get('code')
        session_code = self.request.session.get('code')
        if input_code.upper() == session_code.upper():
            return input_code                     #需要返回
        raise ValidationError('验证码错误')

    def clean(self):
        """
        验证两次输入的密码是否一致
        :return:
        """
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 == p2 or p1 is None:  # None为password出错的情况
            return None
        self.add_error('password2',ValidationError('密码不一致'))


class LoginForm(Form):
    """
    登录Form
    """
    username = fields.CharField(
        min_length=5,
        max_length=32,
        error_messages={
            'required': '用户名不能为空',
            'min_length': '用户名不能少于5位',
            'max_length': '用户名不能多于32位'
        },
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    password = fields.CharField(
        min_length=6,
        max_length=32,
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码不能少于6位',
            'max_length': '密码不能多于32位'
        },
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )