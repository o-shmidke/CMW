from materials.models import Materials
from work.models import Unit, Groups


def _save_unit(unit):
    """Сохранение ед.измерения в БД"""
    if unit is not None:
        if unit != 0:
            unit = unit.replace(' ', '')
        try:
            Unit.objects.get(name=unit)
        except Unit.DoesNotExist:
            value_unit = Unit(name=unit)
            value_unit.save()
        return Unit.objects.get(name=unit)


def _save_materials(name, manufacturer, code_of_product, unit, articul):
    """Сохранение материала в БД"""
    if name is not None or articul is not None:
        unit = _save_unit(unit)
        try:
            Materials.objects.get(articul=articul)
        except Materials.MultipleObjectsReturned:
            print('multiply')
        except Materials.DoesNotExist:
            value = Materials(name=name, unit=unit, manufacturer=manufacturer,
                              code_of_product=code_of_product, articul=articul)
            value.save()


def _save_group(group):
    try:
        Groups.objects.get(name__iexact=group)
    except Groups.DoesNotExist:
        value = Groups(name=group)
        value.save()
    return Groups.objects.get(name__iexact=group)
