from django.db import models


from Accounts import models as Accounts_Models

# Create your models here.
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=350, verbose_name="Warehouse Name")
    assigned_to = models.ForeignKey(
        Accounts_Models.User, on_delete=models.CASCADE, verbose_name="Assigned To"
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added at")

    class Meta:
        verbose_name = "Warehouse"
        verbose_name_plural = "Warehouses"

    def __str__(self):
        return f"{self.warehouse_name} assigned to {self.assigned_to.first_name}"





class Item(models.Model):
    related_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, verbose_name="Related Warehouse"
    )
    brand = models.CharField(max_length=350, verbose_name="Brand")
    category = models.CharField(max_length=350, verbose_name="Category")
    item_name = models.CharField(max_length=750, verbose_name="Item Name")
    item_model_number = models.CharField(
        max_length=350, verbose_name="Item Model Number"
    )
    item_img = models.ImageField(upload_to="Items_Imgs", verbose_name="Item Img")
    main_dimension = models.CharField(max_length=350, verbose_name="Main Dimension")
    cut_off_dimension = models.CharField(
        max_length=350, verbose_name="Cutt off Dimension"
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added at")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.item_name


class SparePart(models.Model):
    related_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, verbose_name="Related Warehouse"
    )
    spare_part_name = models.CharField(max_length=350, verbose_name="Spare Part Name")
    spare_part_model_number = models.CharField(
        max_length=350, verbose_name="Spare Part Model"
    )
    spare_part_img = models.ImageField(
        upload_to="Spare_Parts_Imgs", verbose_name="Spare Part Img"
    )
    spare_part_price = models.FloatField(verbose_name="Spare Part Price", default=0.00)
    available_qty = models.IntegerField(verbose_name="Available QTY")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added at")

    class Meta:
        verbose_name = "Spare Part"
        verbose_name_plural = "Spare Parts"

    def __str__(self):
        return self.spare_part_name


class Custody(models.Model):
    custody_name = models.CharField(max_length=350, verbose_name="Custody Name")
    related_spare_parts = models.ManyToManyField(SparePart)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Custody"
        verbose_name_plural = "Custodies"

    def __str__(self):
        return self.custody_name


class TechnicianCustody(models.Model):
    related_technician = models.ForeignKey(
        Accounts_Models.User,
        on_delete=models.CASCADE,
        verbose_name="Related Technician",
    )
    assigned_custodies = models.ManyToManyField(
        Custody, verbose_name="Assigned Custodies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Technician Custody"
        verbose_name_plural = "Technician Custodies"

    def __str__(self):
        return f"{self.related_technician.first_name}'s Custodies"
