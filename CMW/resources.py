from import_export import resources
from materials.models import PlanMaterials, Materials


class PlanMaterialsResource(resources.ModelResource):
    class Meta:
        model = PlanMaterials


class MaterialsResource(resources.ModelResource):
    class Meta:
        model = Materials
