# Generated by Django 3.0.6 on 2020-05-12 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0003_auto_20200511_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
    ]
