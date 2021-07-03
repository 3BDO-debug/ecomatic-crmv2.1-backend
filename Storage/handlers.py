from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Accounts import models as Accounts_Models


@api_view(["GET", "POST", "DELETE"])
def warehouses_handler(request):
    if request.method == "GET":
        warehouse = models.Warehouse.objects.all()
        warehouse_serializer = serializers.WarehouseSerializers(warehouse, many=True)
        return Response(warehouse_serializer.data)
    elif request.method == "POST":

        created_warehouse = models.Warehouse.objects.create(
            warehouse_name=request.data.get("warehouseName"),
            assigned_to=Accounts_Models.User.objects.get(
                id=int(request.data.get("assignedTo"))
            ),
        )
        warehouse_serializer = serializers.WarehouseSerializers(
            created_warehouse, many=False
        )
        created_warehouse.save()
        return Response(status=status.HTTP_201_CREATED, data=warehouse_serializer.data)

    elif request.method == "DELETE":
        warehouse_to_be_deleted = models.Warehouse.objects.get(id=request.data.get("warehouseId"))
        warehouse_to_be_deleted.delete()
        return Response(status=status.HTTP_200_OK)



@api_view(["GET", "POST", "DELETE"])
def items_handler(request):
    if request.method == "GET":
        items = models.Item.objects.all()
        items_serializer = serializers.ItemSerializers(items, many=True)
        return Response(items_serializer.data)
    elif request.method == "POST":
        created_item = models.Item.objects.create(
            related_warehouse=models.Warehouse.objects.get(
                id=int(request.data.get("relatedWarehouse"))
            ),
            item_name=request.data.get("itemName"),
            brand=request.data.get("brand"),
            category=request.data.get("category"),
            item_model_number=request.data.get("itemModelNumber"),
            item_img=request.data.get("itemImg"),
            main_dimension=request.data.get("mainDimension"),
            cut_off_dimension=request.data.get("cutoffDimension"),
        )
        items_serializer = serializers.ItemSerializers(created_item, many=False)
        created_item.save()
        return Response(status=status.HTTP_201_CREATED, data=items_serializer.data)
    elif request.method == "DELETE":

        item_to_be_deleted = models.Item.objects.get(id=request.data.get("itemId"))
        item_to_be_deleted.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET", "POST", "DELETE"])
def spare_parts_handler(request):
    if request.method == "GET":
        spare_parts = models.SparePart.objects.all()
        spare_parts_serializer = serializers.SparePartSerializers(
            spare_parts, many=True
        )
        return Response(spare_parts_serializer.data)
    elif request.method == "POST":
        created_spare_parts = models.SparePart.objects.create(
            related_warehouse=models.Warehouse.objects.get(
                id=int(request.data.get("relatedWarehouse"))
            ),
            spare_part_name=request.data.get("sparePartName"),
            spare_part_model_number=request.data.get("sparePartModelNumber"),
            spare_part_img=request.data.get("sparePartImage"),
            spare_part_price=float(request.data.get("sparePartPrice")),
            available_qty=int(request.data.get("availableQuantity")),
        )
        spare_parts_serializer = serializers.SparePartSerializers(
            created_spare_parts, many=False
        )
        return Response(
            status=status.HTTP_201_CREATED, data=spare_parts_serializer.data
        )
    elif request.method == "DELETE" :
        sparepart_to_be_deleted = models.SparePart.objects.get(id=request.data.get("sparepartId"))
        sparepart_to_be_deleted.delete()
        return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
def custody_handler(request):
    custody = models.Custody.objects.all()
    custody_serializer = serializers.CustodySerializers(custody, many=True)
    return Response(custody_serializer.data)


@api_view(["GET"])
def technitian_custody_handler(request):
    technitian_custody = models.TechnicianCustody.objects.all()
    technitian_custody_serializer = serializers.TechnicianCustodySerializers(
        technitian_custody, many=True
    )
    return Response(technitian_custody_serializer.data)
