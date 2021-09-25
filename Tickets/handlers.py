import datetime
import json
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
            ticket.related_technician = (
                Accounts_Models.User.objects.get(
                    id=int(request.data.get("technicianId"))
                )
                if ticket.related_technician == None
                else None
            )
        if request.data.get("routeId"):
            ticket.related_route = (
                Configurations_Models.Route.objects.get(
                    id=int(request.data.get("routeId"))
                )
                if ticket.related_route == None
                else None
            )

        ticket.current_stage = request.data.get("currentStage")
        ticket.ticket_status = request.data.get("ticketStatus")
        if request.data.get("forcedStatus"):
            ticket.ticket_forced_status = request.data.get("forcedStatus")
        ticket_serializer = serializers.TicketSerializers(ticket, many=False)
        ticket.save()
        for ticket_device in models.TicketDevice.objects.filter(related_ticket=ticket):
            if (
                ticket_device.device_ticket_type == "Installation"
                and ticket.ticket_status == "Closed"
            ):
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

        if bool(request.data.get("agentNotes")):
            ticket_device_to_be_updated.agent_notes = request.data.get("agentNotes")

        if bool(request.data.get("technicalSupportNotes")):
            ticket_device_to_be_updated.technical_support_notes = request.data.get(
                "technicalSupportNotes"
            )
        if bool(request.data.get("techniciansSupervisorNotes")):
            ticket_device_to_be_updated.technicans_supervisor_notes = request.data.get(
                "techniciansSupervisorNotes"
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
                ticket_device_to_be_updated.not_completed_attachment = request.data.get(
                    "notCompletedAttachment"
                )
                ticket_device_to_be_updated.device_ticket_status = "Not Completed"

                ticket_device_to_be_updated.save()
            elif request.data.get("redirectTicketDevice"):
                ticket_device_to_be_updated.device_ticket_status = "Redirected"
                ticket_device_to_be_updated.redirection_notes = request.data.get(
                    "redirectionNotes"
                )
                ticket_device_to_be_updated.save()

        elif request.data.get("currentStage") == "redirection-stage":

            ticket_device_to_be_updated.not_completed_notes = None
            ticket_device_to_be_updated.not_completed_attachment = None
            ticket_device_to_be_updated.device_ticket_status = "Under Processing"
            ticket_device_to_be_updated.customer_service_notes = None
            installationRequirementsFormsResetter(
                ticket_id, ticket_device_to_be_updated.id
            )

            ticket_device_to_be_updated.save()

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
        ticket_status="In progress",
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
def ticket_follow_up_call_rating_handler(request, ticket_id):
    ticket = models.Ticket.objects.get(id=ticket_id)
    if request.method == "POST":
        ticket_follow_up_call_data = literal_eval(
            request.data.get("ticketFollowUpCallData")
        )
        ticket_follow_up_devices_data = json.loads(
            request.data.get("ticketFollowUpDevicesData")
        )

        created_ticket_follow_up_call = models.TicketFollowUpCallRating.objects.create(
            related_ticket=ticket,
            agent_stage_rating=int(ticket_follow_up_call_data["agentStageRating"]),
            technicial_support_stage_rating=int(
                ticket_follow_up_call_data["technicialSupportStageRating"]
            ),
            technician_rating=int(ticket_follow_up_call_data["technicianRating"]),
            overall_rating=int(ticket_follow_up_call_data["overallRating"]),
            follow_up_notes=ticket_follow_up_call_data["followUpNotes"],
        )
        for device in ticket_follow_up_devices_data:
            models.TicketFollowUpCallDeviceRating.objects.create(
                related_ticket_follow_back_call=created_ticket_follow_up_call,
                related_ticket_device=models.TicketDevice.objects.get(
                    id=int(device["ticketDeviceId"])
                ),
                rating=int(device["rating"]),
            ).save()

        created_ticket_follow_up_call.save()
    ticket_follow_up_call = models.TicketFollowUpCallRating.objects.get(
        related_ticket=ticket
    )
    ticket_follow_up_call_serializer = serializers.TicketFollowUpCallRatingSerializer(
        ticket_follow_up_call, many=False
    )
    ticket_follow_up_devices_ratings = (
        models.TicketFollowUpCallDeviceRating.objects.filter(
            related_ticket_follow_back_call=ticket_follow_up_call
        )
    )
    ticket_follow_up_devices_ratings_serializer = (
        serializers.TicketFollowUpCallDeviceRatingSerializer(
            ticket_follow_up_devices_ratings, many=True
        )
    )

    return Response(
        data={
            "ticket_follow_up_call": ticket_follow_up_call_serializer.data,
            "ticket_follow_up_devices_ratings": ticket_follow_up_devices_ratings_serializer.data,
        }
    )


""" Ticket Completion Forms """


@api_view(["GET", "POST"])
def gas_oven_installation_requirements_form_handler(request, ticket_device_id):
    related_ticket_device = models.TicketDevice.objects.get(id=ticket_device_id)
    if request.method == "POST":
        request_data = json.loads(request.data.get("formikValues"))
        models.GasOvenInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            gas_oven_model_number=request_data["gasOvenModelNumber"],
            gas_type=request_data["gasType"],
            gas_pressure=request_data["gasPressure"],
            ventillation_opening_below_oven_is_available=bool(
                request_data["ventillationOpeningBelowOvenIsAvailable"]
            ),
            ventillation_opening_below_oven_measurements=request_data[
                "ventillationOpeningBelowOvenMeasurements"
            ],
            ventillation_opening_in_front_of_oven_is_available=bool(
                request_data["ventillationOpeningInFrontOfOvenIsAvailable"]
            ),
            ventillation_opening_in_front_of_oven_measurements=request_data[
                "ventillationOpeningInFrontOfOvenMeasurements"
            ],
            stabilizer_type=request_data["stabilizerType"],
            gas_oven_fonia_number=request_data["gasOvenFoniaNumber"],
            grill_fonia_number=request_data["grillFoniaNumber"],
            whats_done_by_the_technician=request_data["whatsDoneByTechnician"],
            gas_oven_final_condition=request_data["gasOvenFinalCondition"],
            notes=request_data["whatsDoneByTechnician"],
            client_signature=request_data["clientSignature"],
            technician_name=request_data["technicianName"],
            attachment=request.data.get("attachment"),
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
        request_data = json.loads(request.data.get("formikValues"))
        models.ElectricOvenInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            electric_oven_model_number=request_data["electricOvenModelNumber"],
            ventillation_opening_is_available=bool(
                request_data["ventaillationOpeningIsAvailable"]
            ),
            ventillation_opening_measurements=request_data[
                "ventiallationOpeningMeasurements"
            ],
            notes=request_data["notes"],
            whats_done_by_the_technician=request_data["whatsDoneByTechnician"],
            electric_oven_final_condition=request_data["electricOvenFinalCondition"],
            client_signature=request_data["clientSignature"],
            technician_name=request_data["technicianName"],
            attachment=request.data("attachment"),
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
        request_data = json.loads(request.data.get("formikValues"))
        models.SlimHobInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            slim_hob_model_number=request_data["slimHobModelNumber"],
            gas_type=request_data["gasType"],
            marble_opening_hole_is_available=bool(
                request_data["marbleOpeningHoleIsAvailable"]
            ),
            marble_opening_hole_measurements=request_data[
                "marbleOpeningHoleMeasurements"
            ],
            gas_pressure=request_data["gasPressure"],
            stabilizer_type=request_data["stabilizerType"],
            whats_done_by_the_technician=request_data["whatsDoneByTechnician"],
            slim_hob_final_condition=request_data["slimHobFinalCondition"],
            client_signature=request_data["clientSignature"],
            technician_name=request_data["technicianName"],
            notes=request_data["slimHobFinalCondition"],
            attachment=request.data.get("attachment"),
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
        request_data = json.loads(request.data.get("formikValues"))
        models.CookerInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            cooker_model_number=request_data["cookerModelNumber"],
            gas_type=request_data["gasType"],
            gas_pressure=request_data["gasPressure"],
            notes=request_data["cookerFinalCondition"],
            stabilizer_type=request_data["stabilizerType"],
            cooker_fonia_number=request_data["cookerFoniaNumber"],
            grill_fonia_number=request_data["grillFoniaNumber"],
            whats_done_by_the_technician=request_data["whatsDoneByTechnician"],
            cooker_final_condition=request_data["cookerFinalCondition"],
            client_signature=request_data["clientSignature"],
            technician_name=request_data["technicianName"],
            attachment=request.data.get("attachment"),
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
        request_data = json.loads(request.data.get("formikValues"))

        models.HoodInstallationRequirementsForm.objects.create(
            related_ticket=related_ticket_device.related_ticket,
            related_ticket_device=related_ticket_device,
            hood_model_number=request_data["hoodModelNumber"],
            hood_height=request_data["hoodHeight"],
            hood_exhaust_height=request_data["hoodExhaustHeight"],
            hood_exhaust_is_straight=bool(request_data["hoodExhaustIsStraight"]),
            notes=request_data["hoodFinalCondition"],
            whats_done_by_the_technician=request_data["whatsDoneByTechnician"],
            hood_final_condition=request_data["hoodFinalCondition"],
            client_signature=request_data["clientSignature"],
            technician_name=request_data["technicianName"],
            attachment=request.data.get("attachment"),
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
