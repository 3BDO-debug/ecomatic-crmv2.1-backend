from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Accounts import models as Accounts_Models
from ast import literal_eval
from Storage import models as Storage_Models


@api_view(["GET", "POST", "DELETE"])
def warehouses_handler(request):
    warehouse = models.Warehouse.objects.all()
    warehouses_serializer = serializers.WarehouseSerializers(warehouse, many=True)

    if request.method == "POST":

        models.Warehouse.objects.create(
            warehouse_name=request.data.get("warehouseName"),
            assigned_to=Accounts_Models.User.objects.get(
                id=int(request.data.get("assignedTo"))
            ),
        ).save()

    elif request.method == "DELETE":
        models.Warehouse.objects.filter(
            id__in=literal_eval(request.data.get("warehousesToBeDeleted"))
        ).delete()

    return Response(status=status.HTTP_200_OK, data=warehouses_serializer.data)


@api_view(["GET", "POST", "DELETE"])
def items_handler(request):
    items = models.Item.objects.all()
    items_serializer = serializers.ItemSerializers(items, many=True)

    if request.method == "POST":
        models.Item.objects.create(
            related_warehouse=models.Warehouse.objects.get(
                id=int(request.data.get("warehouse"))
            ),
            brand=request.data.get("brand"),
            category=request.data.get("category"),
            item_model_number=request.data.get("modelNumber"),
            item_img=request.data.get("image")["path"],
            main_dimension=request.data.get("mainDimensions"),
            cut_off_dimension=request.data.get("cutOffDimensions"),
            warranty_coverage=int(request.data.get("warrantyCoverage")),
        ).save()

    elif request.method == "DELETE":

        models.Item.objects.filter(
            id__in=literal_eval(request.data.get("itemsToBeDeleted"))
        ).delete()

    return Response(items_serializer.data)


@api_view(["GET", "POST", "PUT", "DELETE"])
def spare_parts_handler(request):
    spareparts = models.SparePart.objects.all()
    spareparts_serializer = serializers.SparePartSerializers(spareparts, many=True)
    if request.method == "POST":
        created_spare_parts = models.SparePart.objects.create(
            related_warehouse=models.Warehouse.objects.get(
                id=int(request.data.get("warehouse"))
            ),
            spare_part_model_number=request.data.get("modelNumber"),
            spare_part_img=request.data.get("image")["path"],
            spare_part_price=float(request.data.get("pricePerUnit")),
            available_qty=int(request.data.get("availableQTY")),
        )

    elif request.method == "PUT":
        sparepart_to_be_edited = models.SparePart.objects.get(
            id=request.data.get("sparepartId")
        )
        sparepart_to_be_edited.available_qty = int(
            request.data.get("availableQuantity")
        )
        sparepart_to_be_edited.save()

    elif request.method == "DELETE":
        models.SparePart.objects.filter(
            id__in=literal_eval(request.data.get("sparepartsToBeDeleted"))
        ).delete()

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
