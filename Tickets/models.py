from django.db import models

# Create your models here.
from Storage import models as Storage_Models
from Clients import models as Clients_Models
from Accounts import models as Accounts_Models
from django.db import models

# Create your models here.


class Ticket(models.Model):
    related_client = models.ForeignKey(
        Clients_Models.Client, on_delete=models.CASCADE, verbose_name="Related Client"
    )

    related_technician = models.ForeignKey(
        Accounts_Models.User,
        on_delete=models.CASCADE,
        verbose_name="Related Technician",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def __str__(self):
        return f"{self.related_client.client_full_name}'s ticket"


class TicketDevice(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, verbose_name="Related Ticket"
    )
    related_client_device = models.ForeignKey(
        Clients_Models.ClientDevice,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Related Client Device",
    )
    related_secondary_custody = models.ForeignKey(
        Storage_Models.Item,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Related Secondary Custody",
    )
    device_ticket_type = models.CharField(
        max_length=350, verbose_name="Device Ticket type"
    )
    device_ticket_status = models.CharField(
        max_length=350, verbose_name="Device Ticket Status"
    )
    common_diagnostics = models.CharField(
        max_length=350, verbose_name="Common Diagnostics", null=True, blank=True
    )
    extra_notes = models.TextField(
        verbose_name="Extra Notes",
        null=True,
        blank=True,
        default="Device Extra Notes Goes Here",
    )

    class Meta:
        verbose_name = "Ticket Device"
        verbose_name_plural = "Ticket Devices"

    def __str__(self):
        return f"{self.related_ticket.related_client.client_full_name}'s Related Device"


class TicketUpdate(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, verbose_name="Related Ticket"
    )
    currently_assigned_technician = models.ForeignKey(
        Accounts_Models.User,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Currently Assigned Technician",
    )
    new_ticket_status = models.CharField(
        max_length=350, verbose_name="New Ticket Status"
    )
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Ticket Update"
        verbose_name_plural = "Ticket Updates"

    def __str__(self):
        return f"New Ticket Update {self.id}"
