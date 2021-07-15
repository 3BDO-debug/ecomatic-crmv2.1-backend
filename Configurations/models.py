from django.db import models
from Accounts import models as Accounts_Models
from Storage import models as Storage_Models


class Brand(models.Model):
    brand_name = models.CharField(max_length=350, verbose_name="Brand Name")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        return self.brand_name


class Category(models.Model):
    related_brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, verbose_name="Related Brand"
    )
    category_name = models.CharField(
        max_length=350,
        verbose_name="Category Name",
        choices=[
            ("hoods", "Hoods"),
            ("slim-hobs", "Slim Hobs"),
            ("ovens", "Ovens"),
            ("cookers", "Cookers"),
        ],
    )
    category_feeding_source = models.CharField(
        max_length=350,
        verbose_name="Category Feeding Source",
        choices=[
            ("natural-gas", "Natural Gas"),
            ("gas-cylinder", "Gas Cylinder"),
            ("internal-expulsion", "Internal Expulsion"),
            ("external-expulsion", "External Expulsion"),
        ],
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name


class Branch(models.Model):
    branch_name = models.CharField(max_length=350, verbose_name="Branch Name")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.branch_name


class Distributor(models.Model):
    distributor_name = models.CharField(max_length=350, verbose_name="distributor_name")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Distributor"
        verbose_name_plural = "Distributors"

    def __str__(self):
        return self.distributor_name


class TicketType(models.Model):
    ticket_type = models.CharField(max_length=350, verbose_name="Ticket Type")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.ticket_type

    class Meta:
        verbose_name = "Ticket Type"
        verbose_name_plural = "Ticket Types"


class TicketStatus(models.Model):
    ticket_status = models.CharField(max_length=350, verbose_name="Ticket Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Ticket Status"
        verbose_name_plural = "Tickets Status"


class TicketService(models.Model):
    service_name = models.CharField(max_length=350, verbose_name="Service Name")
    service_price = models.FloatField(verbose_name="Service Price")

    class Meta:
        verbose_name = "Ticket Service"
        verbose_name_plural = "Ticket Services"

    def __str__(self):
        return self.service_name


class CommonDiagnostics(models.Model):
    related_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Related Category"
    )
    issue_type = models.CharField(max_length=350, verbose_name="Issue Type")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Common Diagnostic"
        verbose_name_plural = "Common Diagnostics"

    def __str__(self):
        return self.issue_type


class ClientCategory(models.Model):
    client_category = models.CharField(max_length=350, verbose_name="Client Category")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Client Category"
        verbose_name_plural = "Clients Categories"

    def __str__(self):
        return self.client_category


class TechnicianAssignedCustody(models.Model):
    related_technician = models.ForeignKey(
        Accounts_Models.User, on_delete=models.CASCADE, verbose_name="User"
    )
    assigned_custodies = models.ManyToManyField(
        Storage_Models.Custody, verbose_name="Assign Custodies"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Technician Assigned Custody"
        verbose_name_plural = "Technicians Assigned Custodies"

    def __str__(self):
        return f"Custody Assigned To {self.related_technician.first_name} {self.related_technician.last_name}"


class City(models.Model):
    city_name = models.CharField(max_length=350, verbose_name="City Name")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.city_name


class Region(models.Model):
    region_name = models.CharField(max_length=350, verbose_name="Region Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"

    def __str__(self):
        return self.region_name
