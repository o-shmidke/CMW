# Generated by Django 3.0.6 on 2020-06-30 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0017_auto_20200630_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='completeworks',
            name='color',
            field=models.CharField(blank=True, max_length=50, verbose_name='Процент в окрасе(от красного до зеленого)'),
        ),
    ]
