from import_export import resources
from .models import Sarana

class SaranaResource (resources.ModelResource):
    class Meta:
        model = Sarana
