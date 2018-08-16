from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError

class RegisterForm(Form):
    username =fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    nickname = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = fields.CharField(
        widget=widgets.PasswordInput(attrs={'class': 'form-control'})
    )
    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'class': 'form-control'})
    )
    avatar = fields.FileField(widget=widgets.FileInput(attrs={'id':"imgSelect",'class':'f1'}))
    code = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )

    def __init__(self,request,*args,**kwargs):
        super(RegisterForm,self).__init__(*args,**kwargs)
        self.request = request

    def clean_code(self):
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get('code')
        if input_code.upper() == session_code.upper():
            return input_code
        raise ValidationError("验证码错误")

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 == p2:
            return None
        else:
            # raise ValidationError("密码不一致")
            self.add_error("password2",ValidationError('密码不一致'))