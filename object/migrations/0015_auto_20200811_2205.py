# Generated by Django 3.0.6 on 2020-08-11 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0014_documents'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documents',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='documents'),
        ),
    ]