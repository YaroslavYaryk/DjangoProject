# Generated by Django 3.2.5 on 2021-08-19 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icon', '0014_auto_20210818_0518'),
    ]

    operations = [
        migrations.AddField(
            model_name='likedcomment',
            name='choice',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
