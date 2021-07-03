from django.db import models
from Storage import models as Storage_Models
from Configurations import models as Configurations_Models

# Create your models here.


class Client(models.Model):
    client_full_name = models.CharField(max_length=750, verbose_name="Client Full Name")
    client_phone_number_1 = models.CharField(
        max_length=750, verbose_name="Client Phone Number 1"
    )
    client_phone_number_2 = models.CharField(
        max_length=750, verbose_name="Client Phone Number 2"
    )
    client_landline_number = models.CharField(
        max_length=750, verbose_name="Client Landline Number"
    )
    client_city = models.CharField(max_length=350, verbose_name="Client City")
    client_region = models.CharField(max_length=350, verbose_name="Client Region")
    client_address_1 = models.CharField(max_length=750, verbose_name="Client Address 1")
    client_address_2 = models.CharField(max_length=750, verbose_name="Client Address 2")
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
    related_brand = models.ForeignKey(
        Configurations_Models.Brand,
        on_delete=models.CASCADE,
        verbose_name="Related Brand",
        null=True,
        blank=True,
    )
    related_category = models.ForeignKey(
        Configurations_Models.Category,
        on_delete=models.CASCADE,
        verbose_name="Related Category",
        null=True,
        blank=True,
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
    purchasing_date = models.DateField(verbose_name="Purchasing Date")
    installation_visit_date = models.DateField(verbose_name="Installation Visit Date")
    installation_date = models.DateField(verbose_name="Installation Date")
    warranty_start_date = models.DateField(verbose_name="Warranty Start Date")
    related_branch = models.ForeignKey(
        Configurations_Models.Branch,
        on_delete=models.CASCADE,
        verbose_name="Related Branch",
    )
    related_distributor = models.ForeignKey(
        Configurations_Models.Distributor,
        on_delete=models.CASCADE,
        verbose_name="Related Distributor",
    )
    device_invoice = models.FileField(
        upload_to="Client_Devices_Invoices", verbose_name="Device Invoice"
    )
    in_warranty = models.BooleanField(default=True, verbose_name="In Warranty")

    class Meta:
        verbose_name = "Client Device"
        verbose_name_plural = "Client Devices"

    def __str__(self):
        return f"New Device For {self.related_client.client_full_name}"
