# Generated by Django 2.0.6 on 2018-07-28 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='u2u',
            name='b',
        ),
        migrations.RemoveField(
            model_name='u2u',
            name='g',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='m',
            field=models.ManyToManyField(to='app01.UserInfo'),
        ),
        migrations.DeleteModel(
            name='U2U',
        ),
    ]
