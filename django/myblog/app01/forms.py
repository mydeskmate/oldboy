from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError

class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class':'form-control'})
    )
    password2 = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class':'form-control'})
    )
    code = fields.CharField(
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