# Generated by Django 3.0.6 on 2020-08-19 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0021_remove_documents_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documents',
            name='senior',
        ),
    ]