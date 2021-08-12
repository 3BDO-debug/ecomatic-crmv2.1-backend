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
    device_ticket_status = models.CharField(
        verbose_name="Device Ticket Status", max_length=350, default="Under Processing"
    )
    not_completed_notes = models.TextField(
        verbose_name="Not Completed Notes", null=True, blank=True
    )
    extra_notes = models.TextField(
        verbose_name="Extra Notes",
        null=True,
        blank=True,
    )
    customer_service_notes = models.TextField(
        verbose_name="Customer Service Notes", null=True, blank=True
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


""" Ticket Completion Forms """


class GasOvenInstallationRequirementsForm(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, blank=True
    )
    related_ticket_device = models.ForeignKey(
        TicketDevice,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Related Ticket Device",
    )
    gas_oven_model_number = models.CharField(
        max_length=350,
        verbose_name="Gas Oven Model Number",
    )
    gas_type = models.CharField(max_length=350, verbose_name="Gas Type")
    gas_pressure = models.CharField(max_length=350, verbose_name="Gas Pressure")
    ventillation_opening_below_oven_is_available = models.BooleanField(
        default=True, verbose_name="Ventaillation Opening Below Oven Is Available"
    )
    ventillation_opening_below_oven_measurements = models.CharField(
        max_length=350, verbose_name="Ventillation Opening Below Oven Measurements"
    )
    ventillation_opening_in_front_of_oven_is_available = models.BooleanField(
        default=True, verbose_name="Ventaillaiton Opening In Front Of Oven Is Available"
    )
    ventillation_opening_in_front_of_oven_measurements = models.CharField(
        max_length=350,
        verbose_name="Ventaillaiton Opening In Front Of Oven Measurements",
    )
    stabilizer_type = models.CharField(max_length=350, verbose_name="Stabilizer Type")
    gas_oven_fonia_number = models.CharField(
        max_length=350, verbose_name="Gas Oven Fonia Number"
    )
    grill_fonia_number = models.CharField(
        max_length=350, verbose_name="Grill Fonia Number"
    )
    whats_done_by_the_technician = models.TextField(
        verbose_name="What's Done By The Technician"
    )
    gas_oven_final_condition = models.TextField(verbose_name="Gas Oven Final Condition")
    client_signature = models.CharField(max_length=350, verbose_name="Client Signature")
    technician_name = models.CharField(max_length=350, verbose_name="Technician Name")
    notes = models.TextField(verbose_name="Notes")


class ElectricOvenInstallationRequirementsForm(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, blank=True
    )
    related_ticket_device = models.ForeignKey(
        TicketDevice,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Related Ticket Device",
    )
    electric_oven_model_number = models.CharField(
        max_length=350, verbose_name="Electricc Oven Model Number"
    )
    ventillation_opening_is_available = models.BooleanField(
        default=True, verbose_name="Ventillation Opening Is Available"
    )
    ventillation_opening_measurements = models.CharField(
        max_length=350, verbose_name="Ventillation Opening Measurements"
    )
    notes = models.TextField(verbose_name="Notes")
    whats_done_by_the_technician = models.TextField(
        verbose_name="What's Done By The Technician"
    )
    electric_oven_final_condition = models.TextField(
        verbose_name="Electric Oven Final Condition"
    )
    client_signature = models.CharField(max_length=350, verbose_name="Client Signature")
    technician_name = models.CharField(max_length=350, verbose_name="Technician Name")


class SlimHobInstallationRequirementsForm(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, blank=True
    )
    related_ticket_device = models.ForeignKey(
        TicketDevice,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Related Ticket Device",
    )
    slim_hob_model_number = models.CharField(
        max_length=350, verbose_name="Slim Hob Model Number"
    )
    gas_type = models.CharField(max_length=350, verbose_name="Gas Type")
    marble_opening_hole_is_available = models.BooleanField(
        default=True, verbose_name="Marble Opening Hole"
    )
    marble_opening_hole_measurements = models.CharField(
        max_length=350, verbose_name="Marble Opening Hole Measurements"
    )

    gas_pressure = models.CharField(max_length=350, verbose_name="Gas Pressure")
    stabilizer_type = models.CharField(max_length=350, verbose_name="Stabilizer Type")

    whats_done_by_the_technician = models.TextField(
        verbose_name="What's Done By The Technician"
    )
    slim_hob_final_condition = models.TextField(verbose_name="Slim Hob Final Condition")
    client_signature = models.CharField(max_length=350, verbose_name="Client Signature")
    technician_name = models.CharField(max_length=350, verbose_name="Technician Name")
    notes = models.TextField(verbose_name="Notes")


class CookerInstallationRequirementsForm(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, blank=True
    )
    related_ticket_device = models.ForeignKey(
        TicketDevice,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Related Ticket Device",
    )
    cooker_model_number = models.CharField(
        max_length=350, verbose_name="Cooker Model Number"
    )
    gas_type = models.CharField(max_length=350, verbose_name="Gas Type")
    gas_pressure = models.CharField(max_length=350, verbose_name="Gas Pressure")
    notes = models.TextField(verbose_name="Notes")
    stabilizer_type = models.CharField(max_length=350, verbose_name="Stabilizer Type")
    cooker_fonia_number = models.CharField(
        max_length=350, verbose_name="Cooker Fonia Number"
    )
    grill_fonia_number = models.CharField(
        max_length=350, verbose_name="Grill Fonia Number"
    )
    whats_done_by_the_technician = models.TextField(
        verbose_name="What's Done By The Technician"
    )
    cooker_final_condition = models.TextField(verbose_name="Cooker Final Condition")
    client_signature = models.CharField(max_length=350, verbose_name="Client Signature")
    technician_name = models.CharField(max_length=350, verbose_name="Technician Name")
    notes = models.TextField(verbose_name="Notes")


class HoodInstallationRequirementsForm(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, blank=True
    )
    related_ticket_device = models.ForeignKey(
        TicketDevice,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Related Ticket Device",
    )
    hood_model_number = models.CharField(
        max_length=350, verbose_name="Hood Model Number"
    )
    hood_height = models.CharField(max_length=350, verbose_name="Hood Height")
    hood_exhaust_height = models.CharField(
        max_length=350, verbose_name="Hood Exhaust Height"
    )
    hood_exhaust_is_straight = models.BooleanField(
        default=True, verbose_name="Hood Exhaust Is Straight"
    )
    notes = models.TextField(verbose_name="Notes")
    whats_done_by_the_technician = models.TextField(
        verbose_name="What's Done By The Technician"
    )
    hood_final_condition = models.TextField(verbose_name="Hood Final Condition")
    client_signature = models.CharField(max_length=350, verbose_name="Client Signature")
    technician_name = models.CharField(max_length=350, verbose_name="Technician Name")


""" End Ticket Completetion Forms """
