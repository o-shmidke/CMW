# Generated by Django 3.0.6 on 2020-05-11 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='completeworks',
            options={'verbose_name': 'Выполненные работы', 'verbose_name_plural': 'Выполненные работы'},
        ),
        migrations.AlterModelOptions(
            name='planworks',
            options={'verbose_name': 'Планируемые работы', 'verbose_name_plural': 'Планируемые работы'},
        ),
        migrations.AlterModelOptions(
            name='typeofwork',
            options={'verbose_name': 'Вид работы', 'verbose_name_plural': 'Вид работ'},
        ),
        migrations.AlterModelOptions(
            name='unit',
            options={'verbose_name': 'Ед.измерения', 'verbose_name_plural': 'Ед.измерения'},
        ),
        migrations.AlterField(
            model_name='completeworks',
            name='NCH_left',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Н/Ч за вид работ (осталось)'),
        ),
        migrations.AlterField(
            model_name='completeworks',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Колличество'),
        ),
        migrations.AlterField(
            model_name='planworks',
            name='NCH_general',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Н/Ч за вид работ (на партию)'),
        ),
        migrations.AlterField(
            model_name='planworks',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Колличество'),
        ),
        migrations.AlterField(
            model_name='typeofwork',
            name='NCH_unit_of_time',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Н/Ч на единицу времени'),
        ),
    ]
