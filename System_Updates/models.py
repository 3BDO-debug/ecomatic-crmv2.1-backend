from django.db import models

from Accounts import models as Accounts_Models
from Storage import models as Storage_Models
from Tickets import models as Tickets_Models
from Clients import models as Clients_Models

# Create your models here.


class ClientLog(models.Model):
    related_client = models.ForeignKey(
        Clients_Models.Client, on_delete=models.CASCADE, verbose_name="Related client"
    )
    action = models.CharField(max_length=350, verbose_name="Action done")
    created_by = models.CharField(max_length=350, verbose_name="Created by")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Client log"
        verbose_name_plural = "Client logs"

    def __str__(self):
        return f"New log by {self.created_by} - {self.created_at}"


class UpdateTicketStatusRequest(models.Model):
    related_ticket = models.ForeignKey(Tickets_Models.Ticket, on_delete=models.CASCADE)
    current_stage = models.CharField(max_length=350, verbose_name="Current Stage")
    new_status = models.CharField(max_length=350)
    created_by = models.CharField(max_length=350, verbose_name="Created By")
    is_proceeded = models.BooleanField(default=False)
    proceeded_by = models.ForeignKey(
        Accounts_Models.User, on_delete=models.CASCADE, null=True, blank=True
    )
    new_status_description = models.TextField(
        verbose_name="New Status Description", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")


class TicketLog(models.Model):
    related_ticket = models.ForeignKey(
        Tickets_Models.Ticket, on_delete=models.CASCADE, verbose_name="Related Ticket"
    )
    action = models.CharField(max_length=350, verbose_name="Action")
    stage = models.CharField(max_length=350, verbose_name="Stage")
    created_by = models.ForeignKey(
        Accounts_Models.User, on_delete=models.CASCADE, verbose_name="Created By"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Ticket Log"
        verbose_name_plural = "Ticket Logs"

    def __str__(self):
        return f"New Action '{self.action}' done on {self.related_ticket.id}"


class SparepartRequest(models.Model):
    requested_from = models.ForeignKey(
        Storage_Models.Warehouse, on_delete=models.CASCADE
    )
    requested_spareparts = models.ManyToManyField(Storage_Models.SparePart)
    is_proceeded = models.BooleanField(default=False)
    proceeded_by = models.ForeignKey(Accounts_Models.User, on_delete=models.CASCADE)


class MissingDataRequest(models.Model):
    data_type = models.CharField(max_length=350, verbose_name="Data Type")
    data_to_be_added = models.CharField(max_length=350, verbose_name="Data To Be Added")

    class Meta:
        verbose_name = "Missing Data Request"
        verbose_name_plural = "Missing Data Requests"

    def __str__(self):
        return f"New missing data for {self.data_type}"
