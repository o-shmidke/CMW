from django.core.validators import RegexValidator
from django.shortcuts import reverse

from django.db import models
from time import time

from django.utils.text import slugify

from project.models import CustomUser, Project


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Object(models.Model):
    Name_Object = models.CharField(max_length=500, verbose_name='Наименование объекта', unique=True)
    Adress_Object = models.TextField(verbose_name='Адрес', unique=True)
    NCH_General = models.DecimalField(verbose_name='Н/Ч общее', max_digits=6, decimal_places=2)
    NCH_Spent = models.DecimalField(default=0, verbose_name='Н/Ч затрачено', max_digits=6, decimal_places=2)
    NCH_Left = models.DecimalField(default=0, verbose_name='Н/Ч осталось', max_digits=6, decimal_places=2)

    Perform_proc = models.SmallIntegerField(default=0, verbose_name='Выполнено')
    ID_Project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    ID_Rukovoditel = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Руководитель',
                                       related_name='Руководитель', blank=True, null=True)
    ID_Menedger = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Менеджер',
                                    related_name='Менеджер', blank=True, null=True)
    ID_Ingener = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Инженер',
                                   related_name='Инженер', blank=True, null=True)
    ID_Montazhnik = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Старший_монтажник',
                                      related_name='Старший_монтажник', blank=True,null=True)
    FIO_zakazchika = models.CharField(max_length=500, verbose_name='ФИО заказчика', blank=True)
    Number_phone = models.CharField(max_length=20, verbose_name='Номер телефона заказчика', blank=True)
    Note = models.TextField(verbose_name='Примечание', blank=True)
    slug = models.SlugField(max_length=150, blank=True)

    # def get_absolute_url(self):
    #     return reverse('object:home', kwargs={'slug_obj': self.slug, })

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.Name_Object)
            # self.ID_Project = self.kwargs['slug_proj']
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Name_Object

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
