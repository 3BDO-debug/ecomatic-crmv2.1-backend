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
        update_ticket_status_request.is_proceeded = True
        update_ticket_status_request.proceeded_by = Accounts_Models.User.objects.get(
            id=request.user.id
        )
        update_ticket_status_request.save()
        return Response(status=status.HTTP_200_OK)
