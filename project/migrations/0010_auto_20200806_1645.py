# Generated by Django 3.0.6 on 2020-08-06 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20200806_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='ID_Position',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ID_Position', to='project.Position', verbose_name='Должность'),
        ),
    ]
