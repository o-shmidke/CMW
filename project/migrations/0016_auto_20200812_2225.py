# Generated by Django 3.0.6 on 2020-08-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0015_auto_20200812_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='img',
            field=models.ImageField(blank=True, default='img/images.jpg', null=True, upload_to='img', verbose_name='Фото'),
        ),
    ]
