# Generated by Django 3.0.6 on 2020-05-20 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0006_auto_20200512_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='works',
            options={'ordering': ['-date'], 'verbose_name': 'Работы (планируемые и выполненные)', 'verbose_name_plural': 'Работы (планируемые и выполненные)'},
        ),
        migrations.RenameField(
            model_name='works',
            old_name='data',
            new_name='date',
        ),
        migrations.AddField(
            model_name='works',
            name='NCH_spent',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Н/Ч за вид работ (затрачено)'),
        ),
        migrations.AlterField(
            model_name='works',
            name='NCH_general',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Н/Ч за вид работ (общее)'),
        ),
    ]
