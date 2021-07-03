import datetime
from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Configurations import models as Configurations_Models
from Storage import models as Storage_Models
from Tickets import models as Tickets_Models, serializers as Tickets_Serializers


@api_view(["POST"])
def client_lookup_handler(request):
    client_full_name = request.data.get("clientFullName")
    client_phone_number_1 = request.data.get("clientPhoneNumber1")
    client_lookup_response = {"client_exist": False}
    if models.Client.objects.filter(
        client_full_name=client_full_name, client_phone_number_1=client_phone_number_1
    ).exists():

        client_lookup_response["client_exist"] = True
    else:
        client_lookup_response["client_exist"] = False
    return Response(client_lookup_response)


@api_view(["GET", "POST"])
def clients_handler(request):
    if request.method == "GET":

        clients = models.Client.objects.all()
        client_serializer = serializers.ClientsSerializer(clients, many=True)
        return Response(client_serializer.data)
    else:
        created_client = models.Client.objects.get_or_create(
            client_full_name=request.data.get("clientFullName"),
            client_phone_number_1=request.data.get("clientPhoneNumber1"),
            client_phone_number_2=request.data.get("clientPhoneNumber2"),
            client_landline_number=request.data.get("clientLandlineNumber"),
            client_city=request.data.get("clientCity"),
            client_region=request.data.get("clientRegion"),
            client_address_1=request.data.get("clientAddress1"),
            client_address_2=request.data.get("clientAddress1"),
        )
        client_serializer = serializers.ClientsSerializer(created_client[0], many=False)

        return Response(status=status.HTTP_201_CREATED, data=client_serializer.data)


@api_view(["GET", "PUT"])
def client_details_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)
    if request.method == "GET":

        client_serializer = serializers.ClientsSerializer(client, many=False)

        return Response(client_serializer.data)
    elif request.method == "PUT":
        client.client_full_name = request.data.get("client_full_name")
        client.client_phone_number_1 = request.data.get("client_phone_number_1")
        client.client_phone_number_2 = request.data.get("client_phone_number_2")
        client.client_landline_number = request.data.get("client_landline_number")
        client.client_city = request.data.get("client_city")
        client.client_region = request.data.get("client_region")
        client.client_address_1 = request.data.get("client_address_1")
        client.client_address_2 = request.data.get("client_address_2")
        client.save()
        return Response(data=request.data, status=status.HTTP_200_OK)


@api_view(["GET", "POST", "DELETE"])
def client_devices_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)
    if request.method == "GET":
        client_devices = models.ClientDevice.objects.filter(related_client=client)
        client_devices_serializer = serializers.ClientDeviceSerializer(
            client_devices, many=True
        )
        return Response(client_devices_serializer.data)
    elif request.method == "POST":
        print(request.data.get("purchasingDate"))
        created_client_device = models.ClientDevice.objects.create(
            related_client=client,
            related_brand=Configurations_Models.Brand.objects.get(
                id=int(request.data.get("selectedBrand"))
            ),
            related_category=Configurations_Models.Category.objects.get(
                id=int(request.data.get("selectedCategory"))
            ),
            related_storage_item=Storage_Models.Item.objects.get(
                id=int(request.data.get("selectedItem"))
            ),
            device_feeding_source=request.data.get("selectedDeviceFeedingSource"),
            purchasing_date=request.data.get("purchasingDate"),
            installation_visit_date=request.data.get("installationVisitDate"),
            installation_date=request.data.get("installationDate"),
            warranty_start_date=request.data.get("warrantyStartDate"),
            related_branch=Configurations_Models.Branch.objects.get(
                id=int(request.data.get("selectedBranch"))
            ),
            related_distributor=Configurations_Models.Distributor.objects.get(
                id=int(request.data.get("selectedDistributor"))
            ),
            device_invoice=request.data.get("uploadedDeviceInvoice"),
        )
        client_device_serializer = serializers.ClientDeviceSerializer(
            created_client_device, many=False
        )
        return Response(
            status=status.HTTP_201_CREATED, data=client_device_serializer.data
        )
    elif request.method == "DELETE":
        client_device = models.ClientDevice.objects.get(
            id=int(request.data.get("clientDeviceId"))
        )
        client_device.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def client_tickets_handler(request, client_id):
    client = models.Client.objects.get(id=client_id)

    client_tickets = Tickets_Models.Ticket.objects.filter(related_client=client)
    client_tickets_serializer = Tickets_Serializers.TicketSerializers(
        client_tickets, many=True
    )
    return Response(status=status.HTTP_200_OK, data=client_tickets_serializer.data)
