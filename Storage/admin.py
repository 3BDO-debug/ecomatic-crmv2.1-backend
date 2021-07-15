from django.contrib import admin
from . import models


admin.site.register(models.Custody)
admin.site.register(models.Warehouse)
admin.site.register(models.CustodySparepart)
admin.site.register(models.Item)
admin.site.register(models.SparePart)
