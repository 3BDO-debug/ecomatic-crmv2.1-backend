from django.db import models

from Accounts import models as Accounts_Models
from Storage import models as Storage_Models
from Tickets import models as Tickets_Models
from Clients import models as Clients_Models

# Create your models here.


class UpdateTicketStatusRequest(models.Model):
    related_ticket = models.ForeignKey(Tickets_Models.Ticket, on_delete=models.CASCADE)
    new_status = models.CharField(max_length=350)
    created_by = models.CharField(max_length=350, verbose_name="Created By")
    is_proceeded = models.BooleanField(default=False)
    proceeded_by = models.ForeignKey(
        Accounts_Models.User, on_delete=models.CASCADE, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")


class SparepartRequest(models.Model):
    requested_from = models.ForeignKey(
        Storage_Models.Warehouse, on_delete=models.CASCADE
    )
    requested_spareparts = models.ManyToManyField(Storage_Models.SparePart)
    is_proceeded = models.BooleanField(default=False)
    proceeded_by = models.ForeignKey(Accounts_Models.User, on_delete=models.CASCADE)
