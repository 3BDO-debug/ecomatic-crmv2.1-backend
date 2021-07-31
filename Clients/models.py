from django.db import models
from Storage import models as Storage_Models
from Configurations import models as Configurations_Models

# Create your models here.


class Client(models.Model):
    client_full_name = models.CharField(max_length=750, verbose_name="Client Full Name")
    client_category = models.ForeignKey(
        Configurations_Models.ClientCategory,
        on_delete=models.CASCADE,
        verbose_name="Client Category",
    )
    client_phone_number_1 = models.CharField(
        max_length=750, verbose_name="Client Phone Number 1"
    )
    client_phone_number_2 = models.CharField(
        max_length=750, verbose_name="Client Phone Number 2"
    )
    client_landline_number = models.CharField(
        max_length=750, verbose_name="Client Landline Number"
    )
    client_city = models.ForeignKey(
        Configurations_Models.City, on_delete=models.CASCADE, verbose_name="Client City"
    )
    client_region = models.ForeignKey(
        Configurations_Models.Region,
        on_delete=models.CASCADE,
        verbose_name="Client Region",
    )
    client_address = models.CharField(max_length=750, verbose_name="Client Address 1")
    client_building_no = models.CharField(
        max_length=350, verbose_name="Client Building No", null=True, blank=True
    )
    client_floor_no = models.CharField(
        max_length=350, verbose_name="Client Floor No", blank=True, null=True
    )
    client_apartment_no = models.CharField(
        max_length=350, verbose_name="Client Apartment No", null=True, blank=True
    )
    client_address_landmark = models.CharField(
        max_length=350, verbose_name="Client Address Landmark", null=True, blank=True
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added at")

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.client_full_name


class ClientDevice(models.Model):
    related_client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="Related Client"
    )

    related_storage_item = models.ForeignKey(
        Storage_Models.Item,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Related Storage Item",
    )
    device_feeding_source = models.CharField(
        max_length=350, verbose_name="Device Feeding Source"
    )
    manufacturing_date = models.DateField(
        verbose_name="Manufacturing Date", null=True, blank=True
    )
    purchasing_date = models.DateField(
        verbose_name="Purchasing Date", null=True, blank=True
    )
    installation_date = models.DateField(
        verbose_name="Installation Date", null=True, blank=True
    )
    expected_warranty_start_date = models.DateField(
        verbose_name="Expected Warranty Start Date", null=True, blank=True
    )
    warranty_start_date = models.DateField(
        verbose_name="Warranty Start Date", null=True, blank=True
    )
    related_branch = models.CharField(
        max_length=350, verbose_name="Related Branch", null=True, blank=True
    )
    related_distributor = models.CharField(
        max_length=350, verbose_name="Related Distributor", null=True, blank=True
    )
    device_invoice_or_manufacturer_label = models.FileField(
        upload_to="Client_Devices_Invoices_Manufacturer_Labels",
        verbose_name="Device Attachment",
    )
    in_warranty = models.BooleanField(verbose_name="In Warranty", null=True, blank=True)
    installed_through_the_company = models.BooleanField(
        verbose_name="Installed Through The Company", null=True, blank=True
    )

    class Meta:
        verbose_name = "Client Device"
        verbose_name_plural = "Client Devices"

    def __str__(self):
        return f"New Device For {self.related_client.client_full_name}"
