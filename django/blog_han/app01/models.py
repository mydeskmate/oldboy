from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=32)
    nickname = models.CharField(max_length=32)
    email = models.EmailField(max_length=64)
    phone = models.CharField(max_length=11)

class Blog(models.Model):
    url = models.CharField(max_length=32)
    uf = models.OneToOneField(to="UserInfo")

class Category(models.Model):
    title = models.CharField(max_length=32)

class Tag(models.Model):
    title = models.CharField(max_length=32)

class Article(models.Model):
    created_time = models.DateField()
    like_count = models.IntegerField()
    unlike_count = models.IntegerField()
    read_count = models.IntegerField()
    comment_count = models.IntegerField()
    bg = models.ForeignKey(Blog)
    cg = models.OneToOneField(Category)
    tg = models.ManyToManyField(Tag)



class CommentDetail(models.Model):
    content = models.CharField(max_length=512)

class Comment(models.Model):
    comment_time = models.DateField()
    cd = models.ForeignKey(CommentDetail)
    at = models.ForeignKey(Article)