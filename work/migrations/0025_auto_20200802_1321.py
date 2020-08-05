# Generated by Django 3.0.6 on 2020-08-02 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0024_remove_completeworks_last_add_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planworks',
            name='NCH_left',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, verbose_name='Н/Ч за вид работ (осталось)'),
        ),
        migrations.AlterField(
            model_name='planworks',
            name='quantity_complete',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Колличество (выполнено)'),
        ),
    ]