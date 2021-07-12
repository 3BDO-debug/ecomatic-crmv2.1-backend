from . import serializers, models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Clients import models as Clients_Models
from Accounts import models as Accounts_Models
from ast import literal_eval
from Storage import models as Storage_Models
from System_Updates import models as System_Updates_Models


@api_view(["GET", "DELETE"])
def tickets_handler(request):
    if request.method == "GET":
        if request.data.get("related_technician"):
            tickets = models.Ticket.objects.filter(
                related_technician=Accounts_Models.User.objects.get(
                    id=int(request.data.get("technicianId"))
                )
            ).order_by("-created_at")
        else:
            tickets = models.Ticket.objects.all().order_by("-created_at")
        tickets_serializer = serializers.TicketSerializers(tickets, many=True)
        return Response(tickets_serializer.data)
    elif request.method == "DELETE":
        models.Ticket.objects.filter(
            id__in=literal_eval(request.data.get("ticketsToBeDeleted"))
        ).delete()
        tickets = models.Ticket.objects.all()
        tickets_serializer = serializers.TicketSerializers(tickets, many=True)
        return Response(status=status.HTTP_200_OK, data=tickets_serializer.data)


@api_view(["GET", "PUT"])
def ticket_details_handler(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    if request.method == "GET":
        ticket_serializer = serializers.TicketSerializers(ticket, many=False)
        return Response(ticket_serializer.data)
    elif request.method == "PUT":
        ticket.related_technician = Accounts_Models.User.objects.get(
            id=int(request.data.get("technicianId"))
        )

        ticket_serializer = serializers.TicketSerializers(ticket, many=False)
        ticket.save()

        return Response(status=status.HTTP_200_OK, data=ticket_serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def ticket_devices_handler(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    if request.method == "GET":

        ticket_devices = models.TicketDevice.objects.filter(related_ticket=ticket)
        ticket_devices_serializer = serializers.TicketDeviceSerializers(
            ticket_devices, many=True
        )
        return Response(ticket_devices_serializer.data)
    elif request.method == "PUT":

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
            print("bro", type(literal_eval(request.data.get("assignedSpareparts"))))
            ticket_device_to_be_updated.assigned_spareparts.add(
                *literal_eval(request.data.get("assignedSpareparts"))
            )
            ticket_device_to_be_updated.extra_notes = request.data.get("extraNotes")
            ticket_device_to_be_updated.save()

            return Response(status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        models.TicketDevice.objects.filter(
            id__in=literal_eval(request.data.get("ticketDevicesToBeDeleted"))
        ).delete()
        ticket_devices = models.TicketDevice.objects.filter(related_ticket=ticket)
        ticket_devices_serializer = serializers.TicketDeviceSerializers(
            ticket_devices, many=True
        )
        return Response(
            status=status.HTTP_205_RESET_CONTENT, data=ticket_devices_serializer.data
        )


@api_view(["GET", "POST", "DELETE"])
def ticket_device_spareparts_handler(request, ticket_device_id):
    ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    if request.method == "GET":
        ticket_device_spareparts = models.TicketDeviceSpareparts.objects.filter(
            related_ticket_device=ticket_device
        )
        ticket_device_spareparts_serializer = (
            serializers.TicketDeviceSparepartsSerializer(
                ticket_device_spareparts, many=True
            )
        )
        return Response(data=ticket_device_spareparts_serializer.data)
    elif request.method == "POST":
        assigned_sparepart = Storage_Models.SparePart.objects.get(
            id=int(request.data.get("assignedSparepartId"))
        )
        models.TicketDeviceSpareparts.objects.create(
            related_ticket_device=ticket_device,
            assigned_sparepart=assigned_sparepart,
            required_qty=int(request.data.get("requiredQty")),
        ).save()
        assigned_sparepart.available_qty -= int(request.data.get("requiredQty"))
        assigned_sparepart.save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        models.TicketDeviceSpareparts.objects.filter(
            assigned_sparepart=Storage_Models.SparePart.objects.get(
                id=int(request.data.get("assignedSparepartId"))
            ),
            related_ticket_device=ticket_device,
        ).delete()
        return Response(status=status.HTTP_205_RESET_CONTENT)


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
    System_Updates_Models.UpdateTicketStatusRequest.objects.create(
        related_ticket=pre_intialized_ticket,
        new_status="Pre-Intialized",
        created_by=f"{request.user.first_name} {request.user.last_name}",
    ).save()
    pre_intialized_ticket.save()
    return Response(status=status.HTTP_201_CREATED, data=ticket_serializer.data)


@api_view(["GET"])
def ticket_updates_handler(request):
    ticket_updates = models.TicketUpdate.objects.all()
    ticket_updates_serializer = serializers.TicketUpdateSerializers(
        ticket_updates, many=True
    )
    return Response(ticket_updates_serializer.data)
