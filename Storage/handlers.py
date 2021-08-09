from . import models, serializers
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Accounts import models as Accounts_Models
from ast import literal_eval
from Storage import models as Storage_Models


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

        models.Warehouse.objects.filter(
            id__in=literal_eval(request.data.get("warehousesToBeDeleted"))
        ).delete()

        warehouses = models.Warehouse.objects.all()
        warehouses_serializer = serializers.WarehouseSerializers(warehouses, many=True)
        return Response(status=status.HTTP_200_OK, data=warehouses_serializer.data)


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
            brand=request.data.get("brand"),
            category=request.data.get("category"),
            item_model_number=request.data.get("itemModelNumber"),
            item_img=request.data.get("itemImg"),
            main_dimension=request.data.get("mainDimension"),
            cut_off_dimension=request.data.get("cutoffDimension"),
            warranty_coverage=int(request.data.get("warrantyCoverage")),
        )
        items_serializer = serializers.ItemSerializers(created_item, many=False)
        created_item.save()
        return Response(status=status.HTTP_201_CREATED, data=items_serializer.data)
    elif request.method == "DELETE":

        models.Item.objects.filter(
            id__in=literal_eval(request.data.get("itemsToBeDeleted"))
        ).delete()
        items = models.Item.objects.all()
        items_serializer = serializers.ItemSerializers(items, many=True)
        return Response(status=status.HTTP_200_OK, data=items_serializer.data)


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
    elif request.method == "DELETE":
        models.SparePart.objects.filter(
            id__in=literal_eval(request.data.get("sparepartsToBeDeleted"))
        ).delete()
        spareparts = models.SparePart.objects.all()
        spareparts_serializer = serializers.SparePartSerializers(spareparts, many=True)
        return Response(status=status.HTTP_200_OK, data=spareparts_serializer.data)


@api_view(["GET", "POST", "DELETE"])
def custodies_handler(request):
    if request.method == "POST":
        models.Custody.objects.create(
            custody_name=request.data.get("custodyName")
        ).save()
    elif request.method == "DELETE":
        models.Custody.objects.filter(
            id__in=literal_eval(request.data.get("custodiesToBeDeleted"))
        ).delete()
    custodies = models.Custody.objects.all().order_by("-created_at")
    custodies_serializer = serializers.CustodySerializer(custodies, many=True)
    return Response(status=status.HTTP_200_OK, data=custodies_serializer.data)


@api_view(["GET", "POST", "DELETE"])
def custody_details_handler(request, custody_id):
    custody = models.Custody.objects.get(id=custody_id)
    if request.method == "POST":
        models.CustodySparepart.objects.create(
            related_custody=custody,
            assigned_sparepart=Storage_Models.SparePart.objects.get(
                id=int(request.data.get("assignedSparepartId"))
            ),
            assigned_qty=int(request.data.get("assignedQty")),
        ).save()
    elif request.method == "DELETE":
        models.CustodySparepart.objects.filter(
            id__in=literal_eval(request.data.get("custodySparepartsTobeDeleted"))
        ).delete()

    custody_spareparts = models.CustodySparepart.objects.filter(related_custody=custody)
    custody_spareparts_serializer = serializers.CustodySparepartSerializer(
        custody_spareparts, many=True
    )
    return Response(status=status.HTTP_200_OK, data=custody_spareparts_serializer.data)



