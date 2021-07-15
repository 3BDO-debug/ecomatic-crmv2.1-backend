from django.db import models
from Storage import models as Storage_Models
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

    item_model_number = models.CharField(
        max_length=350, verbose_name="Item Model Number"
    )
    item_img = models.ImageField(upload_to="Items_Imgs", verbose_name="Item Img")
    main_dimension = models.CharField(max_length=350, verbose_name="Main Dimension")
    cut_off_dimension = models.CharField(
        max_length=350, verbose_name="Cutt off Dimension"
    )
    warranty_coverage = models.IntegerField(verbose_name="Warranty Coverage")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Added at")

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    def __str__(self):
        return self.item_model_number


class SparePart(models.Model):
    related_warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, verbose_name="Related Warehouse"
    )

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
        return self.spare_part_model_number


class Custody(models.Model):
    custody_name = models.CharField(max_length=350, verbose_name="Custody Name")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Custody"
        verbose_name_plural = "Custodies"

    def __str__(self):
        return self.custody_name


class CustodySparepart(models.Model):
    related_custody = models.ForeignKey(
        Custody, on_delete=models.CASCADE, verbose_name="Related Custody"
    )
    assigned_sparepart = models.ForeignKey(
        Storage_Models.SparePart,
        on_delete=models.CASCADE,
        verbose_name="Assigned Sparepart",
        null=True,
        blank=True,
    )
    assigned_qty = models.IntegerField(verbose_name="Assigned Qty")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Custody Sparepart"
        verbose_name_plural = "Custodies Spareparts"

    def __str__(self):
        return f"New Custody Sparepart for {self.related_custody.custody_name}"
