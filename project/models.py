from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _


class Position(models.Model):
    Name_Position = models.CharField(max_length=50, verbose_name="Должность", unique=True)

    def __str__(self):
        return self.Name_Position

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"


class CustomUser(AbstractUser):
    patronymic_name = models.CharField(_('Отчество'), max_length=150, blank=True)  # ---add
    ID_Position = models.ForeignKey(Position, on_delete=models.CASCADE, default=1, verbose_name="Должность",
                                    related_name='ID_Position')  # -------add
    objects = UserManager()

    def get_full_name(self):
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.patronymic_name)
        return full_name.strip()

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class Project(models.Model):
    Name_Project = models.CharField(max_length=500, unique=True, verbose_name="Наименование ГК")
    Perform_proc = models.SmallIntegerField(default=0, verbose_name="Выполнено(%)")

    def __str__(self):
        return self.Name_Project

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
