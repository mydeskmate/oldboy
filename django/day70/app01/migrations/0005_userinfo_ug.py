# Generated by Django 2.0.6 on 2018-07-11 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_usergroup'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='ug',
            field=models.ForeignKey(null=True, on_delete=True, to='app01.UserGroup'),
        ),
    ]
