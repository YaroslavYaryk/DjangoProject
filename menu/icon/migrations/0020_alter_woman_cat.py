# Generated by Django 3.2.7 on 2021-09-27 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('icon', '0019_alter_woman_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woman',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='icon.category', verbose_name='Category'),
        ),
    ]
