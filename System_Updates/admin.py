from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.CustodyReleaseRequest)
admin.site.register(models.ChangeTicketStatusRequest)
admin.site.register(models.CallbackReminder)
admin.site.register(models.Notification)
admin.site.register(models.SparePartsRequest)
admin.site.register(models.SparePartsRequestUpdate)
admin.site.register(models.ClientDeviceReplaceRequest)
admin.site.register(models.ClientDeviceReplaceRequestUpdate)