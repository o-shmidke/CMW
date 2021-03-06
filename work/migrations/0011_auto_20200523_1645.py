# Generated by Django 3.0.6 on 2020-05-23 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0010_auto_20200522_1507'),
    ]

    operations = [
        migrations.AddField(
            model_name='completeworks',
            name='unit',
            field=models.ForeignKey(default=34, on_delete=django.db.models.deletion.CASCADE, to='work.Unit', verbose_name='Ед.измерения'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='planworks',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='work.Unit', verbose_name='Ед.измерения'),
        ),
    ]
