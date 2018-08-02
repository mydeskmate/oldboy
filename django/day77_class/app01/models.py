from django.db import models

# Create your models here.
class Classes(models.Model):
    title = models.CharField(max_length=32)

