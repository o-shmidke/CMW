# Generated by Django 3.0.6 on 2020-05-20 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('object', '0009_object_note'),
        ('work', '0007_auto_20200520_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompleteWorks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Колличество(выполнено)')),
                ('NCH_left', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Н/Ч за вид работ (осталось)')),
                ('NCH_spent', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Н/Ч за вид работ (затрачено)')),
                ('comment', models.TextField(verbose_name='Примечание')),
                ('date', models.DateField(verbose_name='Дата выполнения')),
                ('perform_proc', models.SmallIntegerField(default=0, verbose_name='Выполнено')),
                ('name_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='object.Object', verbose_name='Название объекта')),
                ('type_works', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.TypeOfWork', verbose_name='Вид работы')),
            ],
            options={
                'verbose_name': 'Выполненные работы',
                'verbose_name_plural': 'Выполненные работы',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='PlanWorks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity_plan', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Колличество (планируемое)')),
                ('quantity_complete', models.DecimalField(decimal_places=2, default=0, max_digits=6, verbose_name='Колличество (выполнено)')),
                ('NCH_general', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Н/Ч за вид работ (общее)')),
                ('comment', models.TextField(blank=True, verbose_name='Примечание')),
                ('name_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='object.Object', verbose_name='Название объекта')),
                ('type_works', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.TypeOfWork', verbose_name='Вид работы')),
            ],
            options={
                'verbose_name': 'Планируемые работы',
                'verbose_name_plural': 'Планируемые работы',
                'ordering': ['type_works'],
            },
        ),
        migrations.DeleteModel(
            name='Works',
        ),
    ]
