# Generated by Django 3.0.6 on 2020-08-05 05:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0004_planmaterials_name_group'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeliveredMaterials',
        ),
    ]
