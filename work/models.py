from django.core.exceptions import ValidationError
from django.db import models

from object.models import Object


class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название ед.измерения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ед.измерения"
        verbose_name_plural = "Ед.измерения"


class Groups(models.Model):
    name = models.CharField(max_length=200, verbose_name='Группа материалов и работ')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа материалов и работ"
        verbose_name_plural = "Группы материалов и работ"
        ordering = ['name']


class TypeOfWork(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name='Наименование работы')
    NCH_unit_of_time = models.DecimalField(verbose_name='Н/Ч на единицу времени', max_digits=6, decimal_places=2)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, verbose_name='Ед. измерения')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, verbose_name='Название группы', blank=True, null=True)

    def __str__(self):
        return self.name + ' (' + self.unit.name + ')'

    class Meta:
        verbose_name = "Вид работы"
        verbose_name_plural = "Вид работ"
        ordering = ['name']


class PlanWorks(models.Model):
    name_object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Название объекта')
    type_works = models.ForeignKey(TypeOfWork, on_delete=models.CASCADE, verbose_name='Вид работы')
    quantity_plan = models.DecimalField(verbose_name='Колличество (планируемое)', max_digits=8, decimal_places=2)
    NCH_general = models.DecimalField(verbose_name='Н/Ч за вид работ (общее)', max_digits=8, decimal_places=2)
    quantity_complete = models.DecimalField(verbose_name='Колличество (выполнено)', max_digits=6, decimal_places=2,
                                            default=0)
    NCH_left = models.DecimalField(verbose_name='Н/Ч за вид работ (осталось)', max_digits=6, decimal_places=2,
                                   blank=True)
    NCH_spent = models.DecimalField(verbose_name='Н/Ч за вид работ (затрачено)', max_digits=6, decimal_places=2,
                                    default=0)
    perform_proc = models.SmallIntegerField(verbose_name='Выполнено', default=0)
    comment = models.TextField(verbose_name='Примечание', blank=True)
    color = models.CharField(max_length=50, verbose_name='Процент в окрасе(от красного до зеленого)', blank=True)

    def __str__(self):
        return self.type_works.name

    class Meta:
        verbose_name = "Планируемые работы"
        verbose_name_plural = "Планируемые работы"
        ordering = ['type_works']


class CompleteWorks(models.Model):
    name_object = models.ForeignKey(Object, on_delete=models.CASCADE, verbose_name='Название объекта')
    type_works = models.ForeignKey(TypeOfWork, on_delete=models.CASCADE, verbose_name='Вид работы')
    plan = models.ForeignKey(PlanWorks, on_delete=models.CASCADE, verbose_name='Планируемые работы', blank=True)
    quantity_complete = models.DecimalField(verbose_name='Колличество (выполнено)', max_digits=6, decimal_places=2)
    NCH_left = models.DecimalField(verbose_name='Н/Ч за вид работ (осталось)', max_digits=6, decimal_places=2)
    NCH_spent = models.DecimalField(verbose_name='Н/Ч за вид работ (затрачено)', max_digits=6, decimal_places=2,
                                    default=0)
    comment = models.TextField(verbose_name='Примечание', blank=True)
    date = models.DateField(verbose_name='Дата выполнения')
    senior = models.CharField(max_length=300, verbose_name='Ответственный')
    perform_proc = models.SmallIntegerField(default=0, verbose_name='Выполнено')
    color = models.CharField(max_length=50, verbose_name='Процент в окрасе(от красного до зеленого)', blank=True)

    def __str__(self):
        return self.type_works.name

    def clean(self, *args, **kwargs):
        # if self.from_city == self.to_city:
        #     raise ValidationError('Измените пункт отправления/прибытия')
        # qs = PlanWorks.objects.filter(name_object__slug__iexact=self.name_object.slug)
        # if qs.exists():
        #     raise ValidationError('Ошибка')

        return super(CompleteWorks, self).clean(*args, **kwargs)

    class Meta:
        verbose_name = "Выполненные работы"
        verbose_name_plural = "Выполненные работы"
        ordering = ['-date', '-NCH_spent']
