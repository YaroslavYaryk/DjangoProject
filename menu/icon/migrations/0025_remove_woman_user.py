# Generated by Django 3.2.7 on 2021-09-20 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('icon', '0024_woman_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='woman',
            name='user',
        ),
    ]
