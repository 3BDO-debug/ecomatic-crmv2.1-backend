from . import handlers
from django.urls import path

urlpatterns = [
    path("Client-Lookup", handlers.client_lookup_handler),
    path("Client-Device-Warranty-Status", handlers.client_device_warranty_status_checker),
    path("Clients-Data", handlers.clients_handler),
    path("Client-Details/<int:client_id>", handlers.client_details_handler),
    path("Client-Devices-Data/<int:client_id>", handlers.client_devices_handler),
    path("Client-Tickets-Data/<int:client_id>", handlers.client_tickets_handler),
]
