# Generated by Django 3.0.6 on 2020-08-19 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0018_auto_20200819_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='senior',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ответственный'),
        ),
    ]