# Generated by Django 2.0.6 on 2018-07-15 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_boy_m'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='boy',
            name='m',
        ),
    ]
