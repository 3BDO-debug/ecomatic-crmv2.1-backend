from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Ticket)
admin.site.register(models.TicketDevice)
admin.site.register(models.TicketDeviceSpareparts)
admin.site.register(models.TicketUpdate)
