# Generated by Django 3.0.6 on 2020-08-05 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0026_auto_20200805_1316'),
        ('materials', '0007_auto_20200805_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='materials',
            name='group',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='work.Groups', verbose_name='Название группы'),
            preserve_default=False,
        ),
    ]