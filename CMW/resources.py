from import_export import resources
from materials.models import PlanMaterials, Materials
from  work.models import TypeOfWork


class PlanMaterialsResource(resources.ModelResource):
    class Meta:
        model = PlanMaterials


class MaterialsResource(resources.ModelResource):
    class Meta:
        model = Materials


class WorksResource(resources.ModelResource):
    class Meta:
        model = TypeOfWork
