from django.db import models

# Create your models here.
class Class(models.Model):
    title = models.CharField(max_length=32)

