from . import serializers, models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Clients import models as Clients_Models
from ast import literal_eval


@api_view(["GET", "DELETE"])
def tickets_handler(request):
    if request.method == "GET":
        tickets = models.Ticket.objects.all()
        tickets_serializer = serializers.TicketSerializers(tickets, many=True)
        return Response(tickets_serializer.data)
    elif request.method == "DELETE":
        ticket_to_be_deleted = models.Ticket.objects.get(
            id=int(request.data.get("ticketId"))
        )
        ticket_to_be_deleted.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def ticket_details_handler(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    ticket_serializer = serializers.TicketSerializers(ticket, many=False)
    return Response(ticket_serializer.data)


@api_view(["GET", "PUT"])
def ticket_devices_handler(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    if request.method == "GET":

        ticket_devices = models.TicketDevice.objects.filter(related_ticket=ticket)
        ticket_devices_serializer = serializers.TicketDeviceSerializers(
            ticket_devices, many=True
        )
        return Response(ticket_devices_serializer.data)
    elif request.method == "PUT":
        print(request.data)
        if request.data.get("currentStage") == "customer-service-department":
            ticket_device_to_be_updated = models.TicketDevice.objects.get(
                id=int(request.data.get("ticketDeviceId"))
            )
            ticket_device_to_be_updated.device_ticket_type = request.data.get(
                "deviceTicketType"
            )
            ticket_device_to_be_updated.device_ticket_status = request.data.get(
                "deviceTicketStatus"
            )
            ticket_device_to_be_updated.common_diagnostics = request.data.get(
                "commonDiagnostic"
            )
            ticket_device_to_be_updated.extra_notes = request.data.get("extraNotes")
            ticket_device_to_be_updated.save()

            return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def ticket_intializer_handler(request):
    related_client = Clients_Models.Client.objects.get(
        id=int(request.data.get("clientId"))
    )
    pre_intialized_ticket = models.Ticket.objects.create(related_client=related_client)

    for device in literal_eval(request.data.get("ticketDevices")):

        models.TicketDevice.objects.create(
            related_ticket=pre_intialized_ticket,
            related_client_device=Clients_Models.ClientDevice.objects.get(id=device),
            device_ticket_type="pre-intialized",
            device_ticket_status="pre-intialized",
        ).save()
    ticket_serializer = serializers.TicketSerializers(pre_intialized_ticket, many=False)
    pre_intialized_ticket.save()
    return Response(status=status.HTTP_201_CREATED, data=ticket_serializer.data)


@api_view(["GET"])
def ticket_updates_handler(request):
    ticket_updates = models.TicketUpdate.objects.all()
    ticket_updates_serializer = serializers.TicketUpdateSerializers(
        ticket_updates, many=True
    )
    return Response(ticket_updates_serializer.data)
