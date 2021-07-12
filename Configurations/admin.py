from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Brand)
admin.site.register(models.Category)
admin.site.register(models.Branch)
admin.site.register(models.Distributor)
admin.site.register(models.TicketType)
admin.site.register(models.TicketStatus)
admin.site.register(models.CommonDiagnostics)
admin.site.register(models.ClientCategory)
