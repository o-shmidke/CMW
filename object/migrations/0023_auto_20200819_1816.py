# Generated by Django 3.0.6 on 2020-08-19 13:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0022_remove_documents_senior'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Дата загрузки'),
        ),
        migrations.AddField(
            model_name='documents',
            name='senior',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Ответственный'),
        ),
    ]