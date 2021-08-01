from django.db import models

# Create your models here.
from Storage import models as Storage_Models
from Clients import models as Clients_Models
from Accounts import models as Accounts_Models
from django.db import models
from Configurations import models as Configurations_Models

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
    current_stage = models.CharField(max_length=350, verbose_name="Current Stage")
    total_cost = models.FloatField(verbose_name="Total Cost", default=0.00)
    closed_by = models.CharField(
        max_length=350, verbose_name="Closed By", null=True, blank=True
    )
    is_closed = models.BooleanField(default=False, verbose_name="Is Closed")
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

    device_ticket_type = models.CharField(
        max_length=350, verbose_name="Device Ticket type"
    )

    common_diagnostics = models.CharField(
        max_length=350, verbose_name="Common Diagnostics", null=True, blank=True
    )
    is_completed = models.BooleanField(
        verbose_name="Is Completed", null=True, blank=True
    )
    is_not_completed = models.BooleanField(
        verbose_name="Is Not Completed", null=True, blank=True
    )
    not_completed_notes = models.TextField(
        verbose_name="Not Completed Notes", null=True, blank=True
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


class TicketDeviceSpareparts(models.Model):
    related_ticket_device = models.ForeignKey(
        TicketDevice, on_delete=models.CASCADE, verbose_name="Related Ticket Device"
    )
    assigned_sparepart = models.ForeignKey(
        Storage_Models.SparePart,
        on_delete=models.CASCADE,
        verbose_name="Assigned Spareparts",
        null=True,
        blank=True,
    )
    required_qty = models.IntegerField(verbose_name="Required QTY")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Ticket Device Spareparts"
        verbose_name_plural = "Tickets Devices Spareparts"

    def __str__(self):
        return f"New Spareparts assigned for {self.related_ticket_device.related_client_device.related_storage_item.item_model_number}"


class TicketDeviceService(models.Model):
    related_ticket_device = models.ForeignKey(
        TicketDevice, on_delete=models.CASCADE, verbose_name="Related Ticket Device"
    )
    assigned_service = models.ForeignKey(
        Configurations_Models.TicketService,
        on_delete=models.CASCADE,
        verbose_name="Assigned Service",
        null=True,
        blank=True,
    )
    required_qty = models.IntegerField(verbose_name="Required QTY")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Ticket Device Service"
        verbose_name_plural = "Tickets Devices Services"

    def __str__(self):
        return f"New Services assigned for {self.related_ticket_device.related_client_device.related_storage_item.item_model_number}"


class TicketFollowbackCallRating(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, verbose_name="Related Ticket"
    )
    rating = models.IntegerField(verbose_name="Rating")
    notes = models.TextField(verbose_name="Notes", null=True, blank=True)

    class Meta:
        verbose_name = "Ticket Followback Call Rating"
        verbose_name_plural = "Ticket Followback Call Ratings"

    def __str__(self):
        return f"Ticket rating for {self.related_ticket.id}"
