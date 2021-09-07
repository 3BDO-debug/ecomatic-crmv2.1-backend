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
from .utils import installationRequirementsFormsResetter


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
                related_client_device.installation_status = "Installed by the company"
                related_client_device.installation_date = datetime.date.today()
                related_client_device.warranty_start_date = datetime.date.today()
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
            ticket_device_to_be_updated.device_ticket_status = "Under Processing"
            ticket_device_to_be_updated.common_diagnostics = request.data.get(
                "commonDiagnostic"
            )

            ticket_device_to_be_updated.extra_notes = request.data.get("extraNotes")
            ticket_device_to_be_updated.save()

        elif request.data.get("currentStage") == "technician-stage":

            if request.data.get("markCompleted"):
                ticket_device_to_be_updated.device_ticket_status = "Completed"

                ticket_device_to_be_updated.save()
            elif request.data.get("markNotCompleted"):

                ticket_device_to_be_updated.not_completed_notes = request.data.get(
                    "notCompletedNotes"
                )
                ticket_device_to_be_updated.device_ticket_status = "Not Completed"

                ticket_device_to_be_updated.save()
            elif request.data.get("redirectTicketDevice"):
                ticket_device_to_be_updated.device_ticket_status = "Redirected"
                ticket_device_to_be_updated.customer_service_notes = request.data.get(
                    "redirectionNotes"
                )
                ticket_device_to_be_updated.save()

        elif request.data.get("currentStage") == "customer-service-stage":

            ticket_device_to_be_updated.not_completed_notes = None
            ticket_device_to_be_updated.device_ticket_status = "Under Processing"
            ticket_device_to_be_updated.customer_service_notes = None
            installationRequirementsFormsResetter(
                ticket_id, ticket_device_to_be_updated.id
            )

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

        ticket.total_cost += (
            float(request.data.get("requiredQty")) * assigned_sparepart.spare_part_price
        )
        ticket.save()
        ticket_serializer = serializers.TicketSerializers(ticket, many=False)
        assigned_sparepart.available_qty -= int(request.data.get("requiredQty"))
        assigned_sparepart.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "ticket_device_spareparts": ticket_device_spareparts_serializer.data,
                "ticket_details": ticket_serializer.data,
            },
        )
    elif request.method == "DELETE":
        sparepart_to_be_deleted = models.TicketDeviceSpareparts.objects.filter(
            assigned_sparepart=Storage_Models.SparePart.objects.get(
                id=int(request.data.get("assignedSparepartId"))
            ),
            related_ticket_device=ticket_device,
        ).first()
        ticket.total_cost -= (
            sparepart_to_be_deleted.required_qty
            * sparepart_to_be_deleted.assigned_sparepart.spare_part_price
        )
        ticket.save()
        ticket_serializer = serializers.TicketSerializers(ticket, many=False)
        sparepart_to_be_deleted.delete()
        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "ticket_device_spareparts": ticket_device_spareparts_serializer.data,
                "ticket_details": ticket_serializer.data,
            },
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

        assigned_service = Configurations_Models.TicketService.objects.get(
            id=int(request.data.get("assignedServiceId"))
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
        ticket_serializer = serializers.TicketSerializers(ticket, many=False)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "ticket_device_services": ticket_device_service_serializer.data,
                "ticket_details": ticket_serializer.data,
            },
        )
    elif request.method == "DELETE":
        service_to_be_deleted = models.TicketDeviceService.objects.filter(
            assigned_service=Configurations_Models.TicketService.objects.get(
                id=int(request.data.get("assignedServiceId"))
            ),
            related_ticket_device=ticket_device,
        ).first()
        ticket.total_cost -= (
            service_to_be_deleted.required_qty
            * service_to_be_deleted.assigned_service.service_price
        )
        ticket.save()
        ticket_serializer = serializers.TicketSerializers(ticket, many=False)

        service_to_be_deleted.delete()
        return Response(
            data={
                "ticket_device_services": ticket_device_service_serializer.data,
                "ticket_details": ticket_serializer.data,
            },
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


""" Ticket Completion Forms """


@api_view(["GET", "POST"])
def gas_oven_installation_requirements_form_handler(request, ticket_device_id):
    related_ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    if request.method == "POST":
        models.GasOvenInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            gas_oven_model_number=request.data.get("gasOvenModelNumber"),
            gas_type=request.data.get("gasType"),
            gas_pressure=request.data.get("gasPressure"),
            ventillation_opening_below_oven_is_available=bool(
                request.data.get("ventillationOpeningBelowOvenIsAvailable")
            ),
            ventillation_opening_below_oven_measurements=request.data.get(
                "ventillationOpeningBelowOvenMeasurements"
            ),
            ventillation_opening_in_front_of_oven_is_available=bool(
                request.data.get("ventillationOpeningInFrontOfOvenIsAvailable")
            ),
            ventillation_opening_in_front_of_oven_measurements=request.data.get(
                "ventillationOpeningInFrontOfOvenMeasurements"
            ),
            stabilizer_type=request.data.get("stabilizerType"),
            gas_oven_fonia_number=request.data.get("gasOvenFoniaNumber"),
            grill_fonia_number=request.data.get("grillFoniaNumber"),
            whats_done_by_the_technician=request.data.get("whatsDoneByTechnician"),
            gas_oven_final_condition=request.data.get("gasOvenFinalCondition"),
            notes=request.data.get("whatsDoneByTechnician"),
            client_signature=request.data.get("clientSignature"),
            technician_name=request.data.get("technicianName"),
        ).save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        gas_oven_installation_requirements_form = (
            models.GasOvenInstallationRequirementsForm.objects.get(
                related_ticket=related_ticket_device.related_ticket,
                related_ticket_device=related_ticket_device,
            )
        )
        gas_oven_installation_requirements_form_serializer = (
            serializers.GasOvenInstallationRequirementsFormSerializer(
                gas_oven_installation_requirements_form, many=False
            )
        )
        return Response(
            data=gas_oven_installation_requirements_form_serializer.data,
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST"])
def electric_oven_installation_requirements_form_handler(request, ticket_device_id):
    related_ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    if request.method == "POST":
        models.ElectricOvenInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            electric_oven_model_number=request.data.get("electricOvenModelNumber"),
            ventillation_opening_is_available=bool(
                request.data.get("ventaillationOpeningIsAvailable")
            ),
            ventillation_opening_measurements=request.data.get(
                "ventiallationOpeningMeasurements"
            ),
            notes=request.data.get("notes"),
            whats_done_by_the_technician=request.data.get("whatsDoneByTechnician"),
            electric_oven_final_condition=request.data.get(
                "electricOvenFinalCondition"
            ),
            client_signature=request.data.get("clientSignature"),
            technician_name=request.data.get("technicianName"),
        ).save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        electric_oven_installation_requirements_form = (
            models.ElectricOvenInstallationRequirementsForm.objects.get(
                related_ticket=related_ticket_device.related_ticket,
                related_ticket_device=related_ticket_device,
            )
        )
        electric_oven_installation_requirements_form_serializer = (
            serializers.ElectricOvenInstallationRequirementsFormSerializer(
                electric_oven_installation_requirements_form, many=False
            )
        )
        return Response(
            data=electric_oven_installation_requirements_form_serializer.data,
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST"])
def slim_hob_installation_requirements_form_handler(request, ticket_device_id):
    related_ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)

    if request.method == "POST":

        models.SlimHobInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            slim_hob_model_number=request.data.get("slimHobModelNumber"),
            gas_type=request.data.get("gasType"),
            marble_opening_hole_is_available=bool(
                request.data.get("marbleOpeningHoleIsAvailable")
            ),
            marble_opening_hole_measurements=request.data.get(
                "marbleOpeningHoleMeasurements"
            ),
            gas_pressure=request.data.get("gasPressure"),
            stabilizer_type=request.data.get("stabilizerType"),
            whats_done_by_the_technician=request.data.get("whatsDoneByTechnician"),
            slim_hob_final_condition=request.data.get("slimHobFinalCondition"),
            client_signature=request.data.get("clientSignature"),
            technician_name=request.data.get("technicianName"),
            notes=request.data.get("slimHobFinalCondition"),
        ).save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        slim_hob_installation_requirements_form = (
            models.SlimHobInstallationRequirementsForm.objects.get(
                related_ticket=related_ticket_device.related_ticket,
                related_ticket_device=related_ticket_device,
            )
        )
        slim_hob_installation_requirements_form_serializer = (
            serializers.SlimHobInstallationRequirementsFormSerializer(
                slim_hob_installation_requirements_form, many=False
            )
        )
        return Response(
            data=slim_hob_installation_requirements_form_serializer.data,
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST"])
def cooker_installation_requirements_form_handler(request, ticket_device_id):
    related_ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    if request.method == "POST":
        models.CookerInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            cooker_model_number=request.data.get("cookerModelNumber"),
            gas_type=request.data.get("gasType"),
            gas_pressure=request.data.get("gasPressure"),
            notes=request.data.get("cookerFinalCondition"),
            stabilizer_type=request.data.get("stabilizerType"),
            cooker_fonia_number=request.data.get("cookerFoniaNumber"),
            grill_fonia_number=request.data.get("grillFoniaNumber"),
            whats_done_by_the_technician=request.data.get("whatsDoneByTechnician"),
            cooker_final_condition=request.data.get("cookerFinalCondition"),
            client_signature=request.data.get("clientSignature"),
            technician_name=request.data.get("technicianName"),
        ).save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        cooker_installation_requirements_form = (
            models.CookerInstallationRequirementsForm.objects.get(
                related_ticket=related_ticket_device.related_ticket,
                related_ticket_device=related_ticket_device,
            )
        )
        cooker_installation_requirements_form_serializer = (
            serializers.CookerInstallationRequirementsFormSerializer(
                cooker_installation_requirements_form, many=False
            )
        )
        return Response(
            data=cooker_installation_requirements_form_serializer.data,
            status=status.HTTP_200_OK,
        )


@api_view(["GET", "POST"])
def hood_installation_requirements_form_handler(request, ticket_device_id):
    related_ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    if request.method == "POST":
        models.HoodInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            hood_model_number=request.data.get("hoodModelNumber"),
            hood_height=request.data.get("hoodHeight"),
            hood_exhaust_height=request.data.get("hoodExhaustHeight"),
            hood_exhaust_is_straight=bool(request.data.get("hoodExhaustIsStraight")),
            notes=request.data.get("hoodFinalCondition"),
            whats_done_by_the_technician=request.data.get("whatsDoneByTechnician"),
            hood_final_condition=request.data.get("hoodFinalCondition"),
            client_signature=request.data.get("clientSignature"),
            technician_name=request.data.get("technicianName"),
        ).save()
        return Response(status=status.HTTP_201_CREATED)
    elif request.method == "GET":
        hood_installation_requirements_form = (
            models.HoodInstallationRequirementsForm.objects.get(
                related_ticket=related_ticket_device.related_ticket,
                related_ticket_device=related_ticket_device,
            )
        )
        hood_installation_requirements_form_serializer = (
            serializers.HoodInstallationRequirementsFormSerializer(
                hood_installation_requirements_form, many=False
            )
        )
        return Response(
            data=hood_installation_requirements_form_serializer.data,
            status=status.HTTP_200_OK,
        )


""" End Ticket Completeion Forms """
