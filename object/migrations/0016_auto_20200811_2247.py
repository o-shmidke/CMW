# Generated by Django 3.0.6 on 2020-08-11 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0015_auto_20200811_2205'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='documents',
            options={'ordering': ['name_document'], 'verbose_name': 'Документ', 'verbose_name_plural': 'Документы'},
        ),
        migrations.AddField(
            model_name='documents',
            name='name_document',
            field=models.CharField(blank=True, max_length=500, verbose_name='Имя'),
        ),
    ]