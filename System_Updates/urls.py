from . import handlers
from django.urls import path

urlpatterns = [
    path("Client-Logs/<int:client_id>", handlers.client_logs_handler),
    path(
        "Update-Ticket-Status-Request", handlers.update_ticket_status_requests_handler
    ),
    path("Ticket-Logs/<int:ticket_id>", handlers.ticket_logs_handler),
    path("Missing-Data-Requests", handlers.missing_data_requests_handler),
]
