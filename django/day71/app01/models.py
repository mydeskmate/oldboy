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

class Boy(models.Model):
    name = models.CharField(max_length=32)
    m = models.ManyToManyField('Girl',through="LOVE",through_fields=('b','g'))

class Girl(models.Model):
    nick = models.CharField(max_length=32)

class Love(models.Model):
    b = models.ForeignKey('Boy',on_delete=True)
    g = models.ForeignKey('Girl',on_delete=True)
    class Meta:
        unique_together = [
            ('b','g'),
        ]

