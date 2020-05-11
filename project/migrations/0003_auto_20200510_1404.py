# Generated by Django 3.0.6 on 2020-05-10 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20200510_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='patronymic_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='project',
            name='Name_Project',
            field=models.CharField(max_length=500, unique=True, verbose_name='Наименование ГК'),
        ),
        migrations.AlterField(
            model_name='project',
            name='Perform_proc',
            field=models.SmallIntegerField(default=0, verbose_name='Выполнено(%)'),
        ),
    ]
