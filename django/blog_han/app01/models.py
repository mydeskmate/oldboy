from django.db import models

# Create your models here.
class UserInfo(models.Model):
    """
    用户表
    """
    nid = models.BigAutoField(primary_key=True)
    username = models.CharField(verbose_name='用户名',max_length=32,unique=True)
    password = models.CharField(verbose_name='密码',max_length=32)
    nickname = models.CharField(verbose_name='昵称',max_length=32)
    email = models.EmailField(verbose_name='邮箱',unique=True)

    avatar = models.ImageField(verbose_name='头像',null=True)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    fans = models.ManyToManyField(verbose_name='粉丝',
                                  to='UserInfo',
                                  through='UserFans',
                                  through_fields=('user','follower'),
                                  related_name='f'
                                  )

class UserFans(models.Model):
    """
    互粉关系表
    """
    user = models.ForeignKey(verbose_name='博主',to='UserInfo',to_field='nid',related_name='users',on_delete=models.CASCADE)
    follower = models.ForeignKey(verbose_name='粉丝',to='UserInfo',to_field='nid',related_name='followers',on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('user','follower'),
        ]


class Blog(models.Model):
    """
    博客信息
    """
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题',max_length=64),
    site = models.CharField(verbose_name='个人博客前缀',max_length=32,unique=True)
    theme = models.CharField(verbose_name='博客主题',max_length=32)
    user = models.OneToOneField(to="UserInfo",to_field='nid',on_delete=models.CASCADE)

class Category(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称',max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='nid',on_delete=models.CASCADE)

class Article(models.Model):
    nid = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name='文章标题',max_length=128)
    summary = models.CharField(verbose_name='文章简介',max_length=255)
    read_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    blog = models.ForeignKey(verbose_name='所属博客', to='Blog',to_field='nid',on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='个人文章类型', to='Category',to_field='nid',null=True,on_delete=models.CASCADE)
    tag = models.ManyToManyField(
        to='Tag',
        through='Article2Tag',
        through_fields=('article','tag')
    )

    type_choices = [               #全局类型
        (1,'Python'),
        (2,'Linux'),
        (3,'OpenStack'),
        (4,'GoLang'),
    ]
    article_type_id = models.IntegerField(choices=type_choices,default=None)

class ArticleDetail(models.Model):
    """
    文章详细表
    """
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField(verbose_name='所属文章',to='Article',to_field='nid',on_delete=models.CASCADE)


class Article2Tag(models.Model):
    """
    文章标签关系表
    """
    article = models.ForeignKey(verbose_name='文章',to='Article',to_field='nid',on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签',to='Tag',to_field='nid',on_delete=models.CASCADE)

    class Meta:
        unique_together = [
            ('article','tag')
        ]


class UpDown(models.Model):
    """
    文章顶或踩
    """
    article = models.ForeignKey(verbose_name='文章', to='Article',to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='赞或踩用户', to='UserInfo',to_field='nid',on_delete=models.CASCADE)
    up = models.BooleanField(verbose_name='是否赞')

    class Meta:
        unique_together = [
            ('article','user'),
        ]


class Comment(models.Model):
    """
    评论表
    """
    nid = models.BigAutoField(primary_key=Tag)
    title = models.CharField(verbose_name='评论内容',max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    reply = models.ForeignKey(verbose_name='回复评论',to="self",related_name='back',null=True,on_delete=models.CASCADE)         #self 表示自己
    article = models.ForeignKey(verbose_name='评论文章',to='Article',to_field='nid',on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者',to='UserInfo',to_field='nid',on_delete=models.CASCADE)
