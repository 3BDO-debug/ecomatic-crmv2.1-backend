import datetime as dt
from django.db import models
from Storage import models as Storage_Models
from Clients import models as Clients_Models
from Accounts import models as Accounts_Models
from django.db import models
from Configurations import models as Configurations_Models

# Create your models here.


class Ticket(models.Model):
    ticket_generated_id = models.CharField(
        max_length=350,
        verbose_name="Ticket ID",
    )
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
    related_route = models.ForeignKey(
        Configurations_Models.Route,
        on_delete=models.CASCADE,
        verbose_name="Related route",
        null=True,
        blank=True,
    )
    current_stage = models.CharField(max_length=350, verbose_name="Current Stage")
    total_cost = models.FloatField(verbose_name="Total Cost", default=0.00)
    ticket_status = models.CharField(
        verbose_name="Ticket status", null=True, blank=True, max_length=350
    )
    ticket_forced_status = models.CharField(
        max_length=350, verbose_name="Ticket forced status", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"

    def ticket_id_generator(self):
        months = {
            "1": "A",
            "2": "B",
            "3": "C",
            "4": "D",
            "5": "E",
            "6": "F",
            "7": "G",
            "8": "H",
            "9": "I",
            "10": "J",
            "11": "K",
            "12": "L",
        }
        tdy_day = str(dt.datetime.today().day)
        tdy_month = str(dt.datetime.today().month)
        tdy_year = str(dt.datetime.today().year)[-2:]
        ticket_order = Ticket.objects.filter(created_at__gt=dt.date.today()).count() + 1
        return f"{tdy_year}{months[tdy_month]}{tdy_day}-{ticket_order}"

    def __str__(self):
        return f"{self.related_client.client_full_name}'s ticket"

    def save(self, *args, **kwargs):
        self.ticket_generated_id = self.ticket_id_generator()
        super(Ticket, self).save(*args, **kwargs)


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
    not_completed_attachment = models.FileField(
        verbose_name="Not completed attachment",
        upload_to="Not_Completed_Attachment",
        null=True,
        blank=True,
    )
    extra_notes = models.TextField(
        verbose_name="Extra Notes",
        null=True,
        blank=True,
    )
    agent_notes = models.TextField(verbose_name="Agent notes", null=True, blank=True)
    technical_support_notes = models.TextField(
        verbose_name="Technical support notes", null=True, blank=True
    )
    technicans_supervisor_notes = models.TextField(
        verbose_name="Technicians supervisor notes", null=True, blank=True
    )
    redirection_notes = models.TextField(
        verbose_name="Redirection notes", null=True, blank=True
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


class TicketFollowUpCallRating(models.Model):
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, verbose_name="Related Ticket"
    )
    agent_stage_rating = models.IntegerField(
        verbose_name="Agent stage rating", null=True, blank=True
    )
    technicial_support_stage_rating = models.IntegerField(
        verbose_name="Technicial support stage rating", null=True, blank=True
    )
    technician_rating = models.IntegerField(
        verbose_name="Technician rating", null=True, blank=True
    )
    overall_rating = models.IntegerField(
        verbose_name="Overall rating", null=True, blank=True
    )
    follow_up_notes = models.TextField(
        verbose_name="Follow up notes", null=True, blank=True
    )

    class Meta:
        verbose_name = "Ticket Follow Up Call Rating"
        verbose_name_plural = "Ticket Follow Up Call Ratings"

    def __str__(self):
        return f"Ticket rating for {self.related_ticket.id}"


class TicketFollowUpCallDeviceRating(models.Model):
    related_ticket_follow_back_call = models.ForeignKey(
        TicketFollowUpCallRating,
        on_delete=models.CASCADE,
        verbose_name="Related ticket follow back call device rating",
        null=True,
        blank=True,
    )
    related_ticket_device = models.ForeignKey(
        TicketDevice,
        on_delete=models.CASCADE,
        verbose_name="Related ticket device",
        null=True,
        blank=True,
    )
    rating = models.IntegerField(verbose_name="Rating", null=True, blank=True)


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
    attachment = models.FileField(
        verbose_name="Attachment",
        upload_to="Gas_Oven_Installation_Attachment",
        null=True,
        blank=True,
    )


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

    attachment = models.FileField(
        verbose_name="Attachment",
        upload_to="Electric_Oven_Installation_Attachment",
        null=True,
        blank=True,
    )


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

    attachment = models.FileField(
        verbose_name="Attachment",
        upload_to="Slim_Hob_Installation_Attachment",
        null=True,
        blank=True,
    )


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
    attachment = models.FileField(
        verbose_name="Attachment",
        upload_to="Cooker_Installation_Attachment",
        null=True,
        blank=True,
    )


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
    attachment = models.FileField(
        verbose_name="Attachment",
        upload_to="Hood_Installation_Attachment",
        null=True,
        blank=True,
    )


""" End Ticket Completetion Forms """
