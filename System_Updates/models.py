from django.db import models

from Accounts import models as Accounts_Models
from Storage import models as Storage_Models
from Tickets import models as Tickets_Models
from Clients import models as Clients_Models

# Create your models here.
class CustodyReleaseRequest(models.Model):
    requested_from = models.ForeignKey(
        Storage_Models.Warehouse,
        on_delete=models.CASCADE,
        verbose_name="Requested From",
    )
    released_to = models.ForeignKey(
        Accounts_Models.User,
        on_delete=models.CASCADE,
        verbose_name="Released To",
    )
    released_custody = models.ForeignKey(
        Storage_Models.Item, on_delete=models.CASCADE, verbose_name="Released Custody"
    )
    related_ticket = models.ForeignKey(
        Tickets_Models.Ticket,
        on_delete=models.CASCADE,
        verbose_name="Related Ticket",
        default=3,
    )
    request_proceeded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    def __str__(self):
        return f"Custody release request from {self.requested_from.warehouse_name}, to {self.released_to.first_name}"

    class Meta:
        verbose_name = "Custody Release Request"
        verbose_name_plural = "Custody Release Requests"


class ChangeTicketStatusRequest(models.Model):
    related_ticket = models.ForeignKey(
        Tickets_Models.Ticket, on_delete=models.CASCADE, verbose_name="Related Ticket"
    )
    requested_status = models.CharField(max_length=350, verbose_name="Requested Status")
    request_proceeded = models.BooleanField(
        default=False, verbose_name="Request Proceeded"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Change Ticket Status Request"
        verbose_name_plural = "Change Ticket Status Requests"

    def __str__(self):
        return f"New Ticket Change Request for {self.related_ticket.id}"


class SparePartsRequest(models.Model):

    related_ticket_device = models.ForeignKey(
        Tickets_Models.TicketDevice,
        on_delete=models.CASCADE,
        verbose_name="Related ticket device ",
    )
    required_spare_parts = models.ManyToManyField(
        Storage_Models.SparePart, verbose_name="Required Spare Part"
    )
    extra_note = models.TextField(verbose_name="Extra Note")
    storage_approved = models.BooleanField(
        default=False, verbose_name="Storage Approved"
    )
    supervisor_approved = models.BooleanField(
        default=False, verbose_name="Supervisor Approved"
    )
    spare_parts_availability_date = models.DateField(
        verbose_name="Spare Part Availability Date", null=True, blank=True
    )
    admin_approved = models.BooleanField(default=False, verbose_name="Admin Approved")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Spare Part Request"
        verbose_name_plural = "Spare Parts Requests"

    def __str__(self):
        return f"Spare part request for {self.related_ticket_device.related_ticket.related_client.client_full_name} from {self.related_ticket_device.related_ticket.related_technician.first_name}"


class SparePartsRequestUpdate(models.Model):
    related_request = models.ForeignKey(
        SparePartsRequest,
        on_delete=models.CASCADE,
        verbose_name="Related Request",
        default=6,
    )
    action_type = models.CharField(max_length=350, verbose_name="Action Type")
    storage_approved = models.BooleanField(
        default=False, verbose_name="Storage Approved"
    )
    supervisor_approved = models.BooleanField(
        default=False, verbose_name="Supervisor Approved"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Spare Parts Request Update"
        verbose_name_plural = "Spare Parts Request Updates"

    def __str__(self):
        return f"New Spare Parts Request Update {self.id}"


class ClientDeviceReplaceRequest(models.Model):
    requested_by = models.ForeignKey(
        Accounts_Models.User, on_delete=models.CASCADE, verbose_name="Requested by"
    )
    device_to_be_replaced = models.ForeignKey(
        Clients_Models.ClientDevice,
        on_delete=models.CASCADE,
        verbose_name="Device to be replaced",
    )
    related_ticket = models.ForeignKey(
        Tickets_Models.Ticket, on_delete=models.CASCADE, verbose_name="Related Ticket"
    )
    extra_notes = models.TextField(verbose_name="Extra Note")
    supervisor_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Client Device Replace Request"
        verbose_name_plural = "Client Devices Replace Requests"


class ClientDeviceReplaceRequestUpdate(models.Model):
    related_request = models.ForeignKey(
        ClientDeviceReplaceRequest,
        on_delete=models.CASCADE,
        verbose_name="Related request",
    )
    supervisor_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Client Device Replace Request Update"
        verbose_name_plural = "Client Device Replace Request Updates"


class CallbackReminder(models.Model):
    related_ticket = models.ForeignKey(
        Tickets_Models.Ticket,
        on_delete=models.CASCADE,
        verbose_name="Related Ticket",
        default=2,
    )
    reminder_text = models.TextField(verbose_name="Reminder Text")
    remind_at = models.DateTimeField(verbose_name="Remind at")
    user_to_be_reminded = models.ForeignKey(
        Accounts_Models.User,
        on_delete=models.CASCADE,
        verbose_name="User to be reminded",
        default=4,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Callback Reminder"
        verbose_name_plural = "Callback Reminders"

    def __str__(self):
        return f"New callback reminder {self.id}"


class Notification(models.Model):
    app_name = models.CharField(max_length=350, verbose_name="App Name")
    action_type = models.CharField(max_length=350, verbose_name="Action Type")
    created_at = models.DateTimeField(auto_now_add=True)
