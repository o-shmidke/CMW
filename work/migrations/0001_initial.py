# Generated by Django 3.0.6 on 2020-05-11 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('object', '0002_auto_20200510_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название ед.измерения')),
            ],
        ),
        migrations.CreateModel(
            name='TypeOfWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Наименование работы')),
                ('NCH_unit_of_time', models.SmallIntegerField(verbose_name='Н/Ч на единицу времени')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.Unit', verbose_name='Ед. измерения')),
            ],
        ),
        migrations.CreateModel(
            name='PlanWorks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(verbose_name='Колличество')),
                ('NCH_general', models.SmallIntegerField(verbose_name='Н/Ч за вид работ (на партию)')),
                ('name_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='object.Object', verbose_name='Название объекта')),
                ('type_works', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.TypeOfWork', verbose_name='Вид работы')),
            ],
        ),
        migrations.CreateModel(
            name='CompleteWorks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(verbose_name='Колличество')),
                ('NCH_left', models.SmallIntegerField(verbose_name='Н/Ч за вид работ (осталось)')),
                ('comment', models.TextField(verbose_name='Примечание')),
                ('data', models.DateField(verbose_name='Дата выполнения')),
                ('perform_proc', models.SmallIntegerField(default=0, verbose_name='Выполнено')),
                ('name_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='object.Object', verbose_name='Название объекта')),
                ('type_works', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work.TypeOfWork', verbose_name='Вид работы')),
            ],
        ),
    ]
