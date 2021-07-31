import datetime
from dateutil.relativedelta import relativedelta
from . import serializers, models
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Clients import models as Clients_Models
from Accounts import models as Accounts_Models
from ast import literal_eval
from Storage import models as Storage_Models
from System_Updates import models as System_Updates_Models
from Configurations import models as Configurations_Models


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
        print("wlaaa")
        models.Ticket.objects.filter(
            id__in=literal_eval(request.data.get("ticketsToBeDeleted"))
        ).delete()
        tickets = models.Ticket.objects.all()
        tickets_serializer = serializers.TicketSerializers(tickets, many=True)
        return Response(status=status.HTTP_200_OK, data=tickets_serializer.data)


@api_view(["GET", "PUT"])
def ticket_details_handler(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    if request.method == "PUT":
        if request.data.get("technicianId"):
            ticket.related_technician = Accounts_Models.User.objects.get(
                id=int(request.data.get("technicianId"))
            )

        ticket.current_stage = request.data.get("currentStage")
        if request.data.get("isClosed"):
            ticket.is_closed = True
        if ticket.current_stage == "supervisor-stage" and ticket.is_closed:
            ticket.is_closed = False
        ticket_serializer = serializers.TicketSerializers(ticket, many=False)
        ticket.save()
        for ticket_device in models.TicketDevice.objects.filter(related_ticket=ticket):
            if ticket_device.device_ticket_type == "Installation" and ticket.is_closed:
                related_client_device = Clients_Models.ClientDevice.objects.get(
                    id=ticket_device.related_client_device.id
                )
                if (
                    datetime.date.today()
                    > related_client_device.purchasing_date + relativedelta(months=2)
                ):
                    related_client_device.instllation_date = datetime.date.today()

                    related_client_device.warranty_start_date = (
                        related_client_device.purchasing_date + relativedelta(months=2)
                    )
                else:
                    related_client_device.instllation_date = datetime.date.today()
                    related_client_device.warranty_start_date = datetime.date.today()
                related_client_device.installed_through_the_company = True
                related_client_device.in_warranty = (
                    True
                    if related_client_device.warranty_start_date
                    + relativedelta(
                        months=related_client_device.related_storage_item.warranty_coverage
                    )
                    > datetime.date.today()
                    else False
                )
                related_client_device.save()

    ticket_serializer = serializers.TicketSerializers(ticket, many=False)
    return Response(ticket_serializer.data)


@api_view(["GET", "PUT", "DELETE"])
def ticket_devices_handler(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    ticket_devices = models.TicketDevice.objects.filter(related_ticket=ticket)
    ticket_devices_serializer = serializers.TicketDeviceSerializers(
        ticket_devices, many=True
    )

    if request.method == "PUT":
        ticket_device_to_be_updated = models.TicketDevice.objects.get(
            id=int(request.data.get("ticketDeviceId"))
        )

        if (
            request.data.get("currentStage") == "agent-stage"
            or request.data.get("currentStage") == "supervisor-stage"
        ):

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

        elif request.data.get("currentStage") == "technician-stage":

            if request.data.get("markCompleted"):
                ticket_device_to_be_updated.is_completed = True
                ticket_device_to_be_updated.is_not_completed = False
                ticket_device_to_be_updated.save()
            elif request.data.get("markNotCompleted"):

                ticket_device_to_be_updated.not_completed_notes = request.data.get(
                    "notCompletedNotes"
                )
                ticket_device_to_be_updated.is_completed = False
                ticket_device_to_be_updated.is_not_completed = True
                ticket_device_to_be_updated.save()

    elif request.method == "DELETE":
        models.TicketDevice.objects.filter(
            id__in=literal_eval(request.data.get("ticketDevicesToBeDeleted"))
        ).delete()

    return Response(ticket_devices_serializer.data)


@api_view(["GET", "POST", "DELETE"])
def ticket_device_spareparts_handler(request, ticket_device_id):
    ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    ticket = models.Ticket.objects.get(id=ticket_device.related_ticket.id)

    ticket_device_spareparts = models.TicketDeviceSpareparts.objects.filter(
        related_ticket_device=ticket_device
    )
    ticket_device_spareparts_serializer = serializers.TicketDeviceSparepartsSerializer(
        ticket_device_spareparts, many=True
    )
    if request.method == "GET":

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
        print("hereee", type(float(request.data.get("requiredQty"))))
        ticket.total_cost += (
            float(request.data.get("requiredQty")) * assigned_sparepart.spare_part_price
        )
        assigned_sparepart.available_qty -= int(request.data.get("requiredQty"))
        assigned_sparepart.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=ticket_device_spareparts_serializer.data,
        )
    elif request.method == "DELETE":
        models.TicketDeviceSpareparts.objects.filter(
            assigned_sparepart=Storage_Models.SparePart.objects.get(
                id=int(request.data.get("assignedSparepartId"))
            ),
            related_ticket_device=ticket_device,
        ).delete()
        return Response(
            status=status.HTTP_205_RESET_CONTENT,
            data=ticket_device_spareparts_serializer.data,
        )


@api_view(["GET", "POST", "DELETE"])
def ticket_device_services_handler(request, ticket_device_id):
    ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    ticket = models.Ticket.objects.get(id=ticket_device.related_ticket.id)
    ticket_device_services = models.TicketDeviceService.objects.filter(
        related_ticket_device=ticket_device
    )
    ticket_device_service_serializer = serializers.TicketDeviceServicepartsSerializer(
        ticket_device_services, many=True
    )
    if request.method == "GET":

        return Response(data=ticket_device_service_serializer.data)
    elif request.method == "POST":
        print("hellldls", request.data.get("assignedServiceId"))

        assigned_service = Configurations_Models.TicketService.objects.get(
            id=int(request.data.get("assignedServicetId"))
        )
        models.TicketDeviceService.objects.create(
            related_ticket_device=ticket_device,
            assigned_service=assigned_service,
            required_qty=int(request.data.get("requiredQty")),
        ).save()
        ticket.total_cost += (
            int(request.data.get("requiredQty")) * assigned_service.service_price
        )
        ticket.save()
        return Response(
            status=status.HTTP_201_CREATED, data=ticket_device_service_serializer.data
        )
    elif request.method == "DELETE":
        models.TicketDeviceService.objects.filter(
            assigned_service=Configurations_Models.TicketService.objects.get(
                id=int(request.data.get("assignedServiceId"))
            ),
            related_ticket_device=ticket_device,
        ).delete()
        return Response(
            status=status.HTTP_205_RESET_CONTENT,
            data=ticket_device_service_serializer.data,
        )


@api_view(["POST"])
def ticket_intializer_handler(request):
    related_client = Clients_Models.Client.objects.get(
        id=int(request.data.get("clientId"))
    )
    pre_intialized_ticket = models.Ticket.objects.create(
        related_client=related_client,
        current_stage="agent-stage",
    )

    for device in literal_eval(request.data.get("ticketDevices")):

        models.TicketDevice.objects.create(
            related_ticket=pre_intialized_ticket,
            related_client_device=Clients_Models.ClientDevice.objects.get(id=device),
            device_ticket_type="pre-intialized",
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


@api_view(["GET", "POST"])
def ticket_followback_call_rating_handler(request, ticket_id):
    if request.method == "GET":

        ticket_followback_call_rating = models.TicketFollowbackCallRating.objects.get(
            related_ticket=ticket_id
        )

        ticket_followback_call_rating_serializer = (
            serializers.TicketFollowbackCallRatingSerializer(
                ticket_followback_call_rating, many=False
            )
        )
        return Response(data=ticket_followback_call_rating_serializer.data)
    if request.method == "POST":
        ticket_followback_call_rating = (
            models.TicketFollowbackCallRating.objects.create(
                related_ticket=models.Ticket.objects.get(id=ticket_id),
                rating=int(request.data.get("rating")),
                notes=request.data.get("notes"),
            )
        )
        ticket_followback_call_rating_serializer = (
            serializers.TicketFollowbackCallRatingSerializer(
                ticket_followback_call_rating, many=False
            )
        )
        return Response(data=ticket_followback_call_rating_serializer.data)
