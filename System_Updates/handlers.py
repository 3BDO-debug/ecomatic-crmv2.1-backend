from rest_framework.response import Response
from . import models, serializers
from rest_framework.decorators import api_view
from Tickets import models as Tickets_Models
from Accounts import models as Accounts_Models
from rest_framework import status


@api_view(["GET", "PUT"])
def update_ticket_status_requests_handler(request):
    if request.method == "GET":
        if request.GET.get("relatedTicketId"):
            update_ticket_status_request = models.UpdateTicketStatusRequest.objects.get(
                related_ticket=Tickets_Models.Ticket.objects.get(
                    id=int(request.GET.get("relatedTicketId"))
                )
            )
            update_ticket_status_request_serializer = (
                serializers.UpdateTicketStatusRequestSerializer(
                    update_ticket_status_request, many=False
                )
            )
            return Response(data=update_ticket_status_request_serializer.data)
        else:
            update_ticket_status_requests = (
                models.UpdateTicketStatusRequest.objects.filter(is_proceeded=False)
            )
            update_Ticket_status_requests_serializer = (
                serializers.UpdateTicketStatusRequestSerializer(
                    update_ticket_status_requests, many=True
                )
            )
            return Response(data=update_Ticket_status_requests_serializer.data)
    elif request.method == "PUT":
        update_ticket_status_request = models.UpdateTicketStatusRequest.objects.get(
            id=int(request.data.get("updateTicketStatusRequestId"))
        )
        update_ticket_status_request.is_proceeded = bool(
            request.data.get("proceededStatus")
        )
        update_ticket_status_request.current_stage = request.data.get("currentStage")
        update_ticket_status_request.proceeded_by = (
            Accounts_Models.User.objects.get(id=request.user.id)
            if bool(request.data.get("proceededStatus"))
            else None
        )
        update_ticket_status_request.new_status = request.data.get("newStatus")

        update_ticket_status_request.new_status_description = request.data.get(
            "newStatusDescription"
        )
        update_ticket_status_serializer = (
            serializers.UpdateTicketStatusRequestSerializer(
                update_ticket_status_request, many=False
            )
        )
        update_ticket_status_request.save()
        return Response(
            status=status.HTTP_200_OK, data=update_ticket_status_serializer.data
        )


@api_view(["GET", "POST"])
def ticket_logs_handler(request, ticket_id):

    if request.method == "POST":
        models.TicketLog.objects.create(
            related_ticket=Tickets_Models.Ticket.objects.get(id=ticket_id),
            action=request.data.get("action"),
            stage=request.data.get("stage"),
            created_by=Accounts_Models.User.objects.get(id=request.user.id),
        ).save()
    ticket_logs = models.TicketLog.objects.filter(
        related_ticket=Tickets_Models.Ticket.objects.get(id=ticket_id)
    )
    ticket_logs_serializer = serializers.TicketLogSerializer(ticket_logs, many=True)

    return Response(status=status.HTTP_200_OK, data=ticket_logs_serializer.data)


@api_view(["POST"])
def missing_data_requests_handler(request):

    models.MissingDataRequest.objects.create(
        data_type=request.data.get("dataType"),
        data_to_be_added=request.data.get("dataToBeAdded"),
    ).save()

    return Response(status=status.HTTP_201_CREATED)
