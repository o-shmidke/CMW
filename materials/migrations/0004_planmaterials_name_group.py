# Generated by Django 3.0.6 on 2020-08-04 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0003_remove_planmaterials_name_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='planmaterials',
            name='name_group',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='materials.Groups', verbose_name='Название группы'),
            preserve_default=False,
        ),
    ]