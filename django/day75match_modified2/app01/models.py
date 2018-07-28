from django.db import models

# Create your models here.
class UserInfo(models.Model):
    nickname = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    gender_choices = (
        (1,'男'),
        (2,'女'),
    )
    gender = models.IntegerField(choices=gender_choices)

    m = models.ManyToManyField('UserInfo')

# class U2U(models.Model):
#     g = models.ForeignKey('UserInfo',related_name='boys',on_delete=True)
#     b = models.ForeignKey('UserInfo',related_name='girls',on_delete=True)