# Generated by Django 2.0.6 on 2018-07-15 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20180715_1237'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='love',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='love',
            name='b',
        ),
        migrations.RemoveField(
            model_name='love',
            name='g',
        ),
        migrations.RemoveField(
            model_name='boy',
            name='m',
        ),
        migrations.DeleteModel(
            name='Love',
        ),
    ]
