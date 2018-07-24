from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator,URLValidator,DecimalValidator,\
MaxLengthValidator,MinLengthValidator,MaxValueValidator,MinValueValidator

# Create your models here.
class UserInfor(models.Model):
    username = models.CharField(max_length=32,verbose_name='用户名')
    email = models.EmailField(null=True,default='1111',unique=True,blank=True)
    ctime = models.DateTimeField(null=True)
    test = models.CharField(
        max_length=32,
        error_messages={
            'c1': '优先错信息1',
            'c2': '优先错信息2',
            'c3': '优先错信息3',
        },
        validators=[
            RegexValidator(regex='root_\d+', message='错误了', code='c1'),
            RegexValidator(regex='root_112233\d+', message='又错误了2', code='c2'),
            EmailValidator(message='又错误了3', code='c3'), ]
    )
    color_list = (
        (1,'黑色'),
        (2,'白色'),
        (3,'蓝色')
    )
    color = models.IntegerField(choices=color_list,default=2)