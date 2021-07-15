import datetime
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


@api_view(["POST"])
def client_device_warranty_status_checker(request):
    installation_date = request.data.get("installationDate")
    warranty_expiry_date = (
        datetime.datetime.strptime(installation_date, "%Y-%m-%d")
        + relativedelta(months=int(request.data.get("itemWarrantyCoverage")))
    ).date()

    return Response(
        {"in_warranty": False if datetime.date.today() > warranty_expiry_date else True}
    )


@api_view(["POST"])
def client_lookup_handler(request):

    if models.Client.objects.filter(
        client_phone_number_1=request.data.get("clientPhoneNumber1")
    ).exists():
        return Response({"client_exist": True})
    elif models.Client.objects.filter(
        client_phone_number_2=request.data.get("clientPhoneNumber2")
    ).exists():
        return Response({"client_exist": True})
    elif models.Client.objects.filter(
        client_landline_number=request.data.get("clientLandlineNumber")
    ).exists():
        return Response({"client_exist": True})
    else:
        return Response({"client_exist": False})


@api_view(["GET", "POST", "DELETE"])
def clients_handler(request):

    if request.method == "GET":

        clients = models.Client.objects.all()
        client_serializer = serializers.ClientsSerializer(clients, many=True)
        return Response(client_serializer.data)
    elif request.method == "POST":
        created_client = models.Client.objects.get_or_create(
            client_full_name=request.data.get("clientFullName"),
            client_category=Configurations_Models.ClientCategory.objects.get(
                id=int(request.data.get("clientCategoryId"))
            ),
            client_phone_number_1=request.data.get("clientPhoneNumber1"),
            client_phone_number_2=request.data.get("clientPhoneNumber2"),
            client_landline_number=request.data.get("clientLandlineNumber"),
            client_city=Configurations_Models.City.objects.get(
                id=int(request.data.get("clientCity"))
            ),
            client_region=Configurations_Models.Region.objects.get(
                id=int(request.data.get("clientRegion"))
            ),
            client_address=request.data.get("clientAddress"),
            client_building_no=request.data.get("clientBuildingNo"),
            client_apartment_no=request.data.get("clientApartmentNo"),
            client_address_landmark=request.data.get("landmark"),
        )
        client_serializer = serializers.ClientsSerializer(created_client[0], many=False)

        return Response(status=status.HTTP_201_CREATED, data=client_serializer.data)
    elif request.method == "DELETE":
        models.Client.objects.filter(
            id__in=literal_eval(request.data.get("clientsToBeDeleted"))
        ).delete()
        clients = models.Client.objects.all()
        clients_serializer = serializers.ClientsSerializer(clients, many=True)
        return Response(status=status.HTTP_200_OK, data=clients_serializer.data)


@api_view(["GET", "PUT"])
def client_details_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)
    if request.method == "GET":

        client_serializer = serializers.ClientsSerializer(client, many=False)

        return Response(client_serializer.data)
    elif request.method == "PUT":
        client.client_full_name = request.data.get("client_full_name")
        client.client_category = Configurations_Models.ClientCategory.objects.get(
            id=int(request.data.get("clientCategoryId"))
        )
        client.client_phone_number_1 = request.data.get("client_phone_number_1")
        client.client_phone_number_2 = request.data.get("client_phone_number_2")
        client.client_landline_number = request.data.get("client_landline_number")
        client.client_city = request.data.get("client_city")
        client.client_region = request.data.get("client_region")
        client.client_address = request.data.get("client_address")
        client.save()
        return Response(data=request.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "DELETE"])
def client_devices_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)

    if request.method == "POST":
        print(request.data)
        models.ClientDevice.objects.create(
            related_client=client,
            related_storage_item=Storage_Models.Item.objects.get(
                id=int(request.data.get("selectedItem"))
            ),
            device_feeding_source=request.data.get("selectedDeviceFeedingSource"),
            manufacturing_date=request.data.get("manufacturingDate"),
            purchasing_date=request.data.get("purchasingDate"),
            expected_warranty_start_date=request.data.get("expectedWarrantyStartDate"),
            installed_through_the_company=bool(
                request.data.get("installedThroughTheCompany")
            ),
            installation_date=request.data.get("installationDate"),
            warranty_start_date=request.data.get("warrantyStartDate"),
            in_warranty=bool(request.data.get("warrantyStatus")),
            related_branch=request.data.get("selectedBranch"),
            related_distributor=request.data.get("selectedDistributor"),
            device_invoice_or_manufacturer_label=request.data.get(
                "uploadedDeviceInvoiceOrManufacturerLabel"
            ),
        ).save()

    elif request.method == "DELETE":
        models.ClientDevice.objects.filter(
            id__in=literal_eval(request.data.get("clientDevicesToBeDeleted"))
        ).delete()

    client_devices = models.ClientDevice.objects.filter(related_client=client)
    client_devices_serializer = serializers.ClientDeviceSerializer(
        client_devices, many=True
    )

    return Response(client_devices_serializer.data)


@api_view(["GET"])
def client_tickets_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)

    client_tickets = Tickets_Models.Ticket.objects.filter(related_client=client)
    client_tickets_serializer = Tickets_Serializers.TicketSerializers(
        client_tickets, many=True
    )
    return Response(status=status.HTTP_200_OK, data=client_tickets_serializer.data)
