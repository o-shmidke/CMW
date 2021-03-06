# Generated by Django 3.0.6 on 2020-05-22 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0008_auto_20200520_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planworks',
            name='quantity_complete',
        ),
        migrations.AddField(
            model_name='planworks',
            name='NCH_ed_vrem',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Н/Ч за вид работ (единица времени)'),
        ),
        migrations.AlterField(
            model_name='completeworks',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Колличество (выполнено)'),
        ),
    ]
