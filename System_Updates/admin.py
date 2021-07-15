from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.UpdateTicketStatusRequest)
admin.site.register(models.SparepartRequest)
admin.site.register(models.MissingDataRequest)
