from django.db import models

# Create your models here.
class UserType(models.Model):
    title = models.CharField(max_length=32)

class UserInfo(models.Model):
    name = models.CharField(max_length=16)
    age = models.IntegerField()
    ut = models.ForeignKey('UserType',on_delete=True)

    def __str__(self):
        return "%s-%s" %(self.id,self.name)