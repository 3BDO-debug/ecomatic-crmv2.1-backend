from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Ticket)
admin.site.register(models.TicketDevice)
admin.site.register(models.TicketDeviceSpareparts)
admin.site.register(models.TicketDeviceService)
admin.site.register(models.TicketFollowbackCallRating)
admin.site.register(models.SlimHobInstallationRequirementsForm)
admin.site.register(models.CookerInstallationRequirementsForm)
admin.site.register(models.HoodInstallationRequirementsForm)
admin.site.register(models.ElectricOvenInstallationRequirementsForm)
admin.site.register(models.GasOvenInstallationRequirementsForm)
