import datetime
import json
from Ecomatic_CRM.utils import convert_my_iso_8601
from pytz import timezone
from dateutil.relativedelta import relativedelta
from . import models, serializers
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from Configurations import models as Configurations_Models
from Storage import models as Storage_Models
from Tickets import models as Tickets_Models, serializers as Tickets_Serializers
from ast import literal_eval
from .utils import client_device_warranty_status_updater


@api_view(["POST"])
def expected_warranty_start_date_calc(request):
    if bool(request.data.get("invoiceAvailabe")):
        expected_warranty_start_date = (
            datetime.datetime.strptime(request.data.get("date"), "%Y- %m- %d")
            + relativedelta(months=2)
        ).date()
    else:
        expected_warranty_start_date = (
            datetime.datetime.strptime(request.data.get("date"), "%Y- %m- %d")
            + relativedelta(months=6)
        ).date()
    return Response({"expected_warranty_start_date": expected_warranty_start_date})


@api_view(["POST"])
def client_device_warranty_status_checker(request):
    installation_date = request.data.get("installationDate")
    warranty_expiry_date = (
        datetime.datetime.strptime(installation_date, "%Y- %m-%d")
        + relativedelta(months=int(request.data.get("itemWarrantyCoverage")))
    ).date()

    return Response({"in_warranty": datetime.date.today() <= warranty_expiry_date})


@api_view(["POST"])
def client_lookup_handler(request):
    if models.Client.objects.filter(
        client_phone_number_1=request.data.get("clientPhoneNumberOrLandline")
    ).exists():
        client = models.Client.objects.filter(
            client_phone_number_1=request.data.get("clientPhoneNumberOrLandline")
        )
        return Response({"client_exist": True, "client_id": client.first().id})
    elif models.Client.objects.filter(
        client_phone_number_2=request.data.get("clientPhoneNumberOrLandline")
    ).exists():
        client = models.Client.objects.filter(
            client_phone_number_2=request.data.get("clientPhoneNumberOrLandline")
        )
        return Response({"client_exist": True, "client_id": client.first().id})
    elif models.Client.objects.filter(
        client_landline_number=request.data.get("clientPhoneNumberOrLandline")
    ).exists():
        client = models.Client.objects.filter(
            client_landline_number=request.data.get("clientPhoneNumberOrLandline")
        )
        return Response({"client_exist": True, "client_id": client.first().id})
    else:
        return Response({"client_exist": False})


@api_view(["GET", "POST", "DELETE"])
def clients_handler(request):

    if request.method == "POST":
        models.Client.objects.get_or_create(
            client_full_name=request.data.get("fullname"),
            client_category=Configurations_Models.ClientCategory.objects.get(
                id=int(request.data.get("category"))
            ),
            client_phone_number_1=request.data.get("phoneNumber1"),
            client_phone_number_2=request.data.get("phoneNumber2"),
            client_landline_number=request.data.get("landline"),
            client_city=Configurations_Models.City.objects.get(
                id=int(request.data.get("city"))
            ),
            client_region=Configurations_Models.Region.objects.get(
                id=int(request.data.get("region"))
            ),
            client_address=request.data.get("address"),
            client_building_no=request.data.get("buildingNo"),
            client_floor_no=request.data.get("floorNo"),
            client_apartment_no=request.data.get("apartmentNo"),
            client_address_landmark=request.data.get("landmark"),
        )
    elif request.method == "DELETE":
        models.Client.objects.filter(
            id__in=literal_eval(request.data.get("clientsToBeDeleted"))
        ).delete()
    clients = models.Client.objects.all()
    client_serializer = serializers.ClientsSerializer(clients, many=True)
    return Response(client_serializer.data)


@api_view(["GET", "PUT"])
def client_details_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)

    client_serializer = serializers.ClientsSerializer(client, many=False)

    if request.method == "PUT":
        client.client_full_name = request.data.get("fullname")
        client.client_category = Configurations_Models.ClientCategory.objects.get(
            id=int(request.data.get("category")["id"])
        )
        client.client_phone_number_1 = request.data.get("phoneNumber1")
        client.client_phone_number_2 = request.data.get("phoneNumber2")
        client.client_landline_number = request.data.get("landline")
        client.client_city = Configurations_Models.City.objects.get(
            id=int(request.data.get("city")["id"])
        )
        client.client_region = Configurations_Models.Region.objects.get(
            id=int(request.data.get("region")["id"])
        )
        client.client_building_no = request.data.get("buildingNo")
        client.client_floor_no = request.data.get("floorNo")
        client.client_apartment_no = request.data.get("apartmentNo")
        client.client_address = request.data.get("address")
        client.save()
    return Response(client_serializer.data)


@api_view(["GET", "POST", "DELETE"])
def client_devices_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)

    if request.method == "POST":
        request_data = json.loads(request.data.get("formikValues"))
        models.ClientDevice.objects.create(
            related_client=client,
            related_storage_item=Storage_Models.Item.objects.get(
                id=int(request_data["device"])
            ),
            device_feeding_source=request_data["feedingSource"],
            manufacturing_date=convert_my_iso_8601(
                request_data["manufacturingDate"], timezone("EET")
            )
            if request_data["manufacturingDate"]
            else None,
            purchasing_date=convert_my_iso_8601(
                request_data["purchasingDate"], timezone("EET")
            )
            if request_data["purchasingDate"]
            else None,
            expected_warranty_start_date=request_data[
                "expectedWarrantyStartDate"
            ]
            or None,
            installation_status=request_data["installationStatus"],
            installation_date=convert_my_iso_8601(
                request_data["installationDate"], timezone("EET")
            )
            if request_data["installationDate"]
            else None,
            warranty_start_date=convert_my_iso_8601(
                request_data["installationDate"], timezone("EET")
            )
            if request_data["installationDate"]
            else None,
            in_warranty=bool(request_data["warrantyStatus"]),
            related_branch=request_data["branch"],
            related_distributor=request_data["distributor"],
            device_invoice_or_manufacturer_label=request.data.get(
                "deviceInvoiceOrManufacturingLabel"
            ),
        ).save()

    elif request.method == "DELETE":
        models.ClientDevice.objects.filter(
            id__in=literal_eval(request.data.get("clientDevicesToBeDeleted"))
        ).delete()

    client_devices = models.ClientDevice.objects.filter(related_client=client).order_by('-created_at')
    client_device_warranty_status_updater(client_devices)
    client_devices_serializer = serializers.ClientDeviceSerializer(
        client_devices, many=True
    )

    return Response(status=status.HTTP_200_OK, data=client_devices_serializer.data)


@api_view(["GET"])
def client_tickets_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)

    client_tickets = Tickets_Models.Ticket.objects.filter(related_client=client)
    client_tickets_serializer = Tickets_Serializers.TicketSerializers(
        client_tickets, many=True
    )
    return Response(status=status.HTTP_200_OK, data=client_tickets_serializer.data)
