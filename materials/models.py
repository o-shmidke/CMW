from django.db import models

from object.models import Object
from work.models import Unit, Groups


class Materials(models.Model):
    name = models.CharField(max_length=1000, verbose_name='Наименование материала')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='Ед. измерения')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name='Название группы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Материалы"
        verbose_name_plural = "Материалы"
        ordering = ['name']


# class Groups(models.Model):
#     name = models.CharField(max_length=200, verbose_name='Группа материалов и работ')
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = "Группа материалов и работ"
#         verbose_name_plural = "Группы материалов и работ"
#         ordering = ['name']


class PlanMaterials(models.Model):
    material = models.ForeignKey(Materials, on_delete=models.CASCADE, verbose_name='Материал')
    quantity_plan = models.DecimalField(verbose_name='Колличество (планируемое)', max_digits=8, decimal_places=2)
    quantity_delivered = models.DecimalField(verbose_name='Колличество (поставленное)', max_digits=8, decimal_places=2,
                                             default=0)
    name_object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Название объекта')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name='Название группы')

    def __str__(self):
        return self.material.name

    class Meta:
        verbose_name = "Планируемые материалы"
        verbose_name_plural = "Планируемые материалы"
        ordering = ['material']

