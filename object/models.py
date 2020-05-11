from django.db import models

from project.models import CustomUser, Project


class Object(models.Model):
    Name_Object = models.CharField(max_length=500, verbose_name='Наименование объекта', unique=True)
    Adress_Object = models.TextField(verbose_name='Адрес', unique=True)
    NCH_General = models.SmallIntegerField(verbose_name='Н/Ч общее')
    NCH_Spent = models.SmallIntegerField(default=0, verbose_name='Н/Ч затрачено')
    Perform_proc = models.SmallIntegerField(default=0, verbose_name='Выполнено')
    ID_Project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    ID_Rukovoditel = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Руководитель',
                                       related_name='Руководитель')
    ID_Menedger = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Менеджер',
                                    related_name='Менеджер')
    ID_Ingener = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Инженер',
                                   related_name='Инженер')
    ID_Montazhnik = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Старший_монтажник',
                                      related_name='Старший_монтажник')

    def __str__(self):
        return self.Name_Object

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
