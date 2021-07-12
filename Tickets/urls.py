from . import handlers
from django.urls import path

urlpatterns = [
    path("Tickets-Data", handlers.tickets_handler),
    path("Ticket-Details-Data/<int:ticket_id>", handlers.ticket_details_handler),
    path("Ticket-Intializer", handlers.ticket_intializer_handler),
    path("Ticket-Devices-Data/<int:ticket_id>", handlers.ticket_devices_handler),
    path(
        "Ticket-Device-Spareparts/<int:ticket_device_id>",
        handlers.ticket_device_spareparts_handler,
    ),
    path("ticket_updates", handlers.ticket_updates_handler),
]
