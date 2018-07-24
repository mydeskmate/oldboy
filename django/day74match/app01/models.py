from django.db import models

# Create your models here.
class Boy(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    m = models.ManyToManyField('Girl',through="Love",through_fields=('bid','gid',))

class Girl(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

class Love(models.Model):
    bid = models.ForeignKey('Boy',on_delete=True)
    gid = models.ForeignKey('Girl',on_delete=True)

    class Meta:
        unique_together = [
            ('bid','gid'),
        ]