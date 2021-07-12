from . import handlers
from django.urls import path

urlpatterns = [
    path("Update-Ticket-Status-Request", handlers.update_ticket_status_requests_handler)
]
