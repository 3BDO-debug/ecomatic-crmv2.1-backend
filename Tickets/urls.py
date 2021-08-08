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
    path(
        "Ticket-Device-Services/<int:ticket_device_id>",
        handlers.ticket_device_services_handler,
    ),
    path("ticket_updates", handlers.ticket_updates_handler),
    path(
        "Ticket-Followback-Call-Rating/<int:ticket_id>",
        handlers.ticket_followback_call_rating_handler,
    ),
    path(
        "Gas-Oven-Instllation-Requirements-Form/<int:ticket_device_id>",
        handlers.gas_oven_installation_requirements_form_handler,
    ),
    path(
        "Electric-Oven-Instllation-Requirements-Form/<int:ticket_device_id>",
        handlers.electric_oven_installation_requirements_form_handler,
    ),
    path(
        "Slim-Hob-Instllation-Requirements-Form/<int:ticket_device_id>",
        handlers.slim_hob_installation_requirements_form_handler,
    ),
    path(
        "Hood-Instllation-Requirements-Form/<int:ticket_device_id>",
        handlers.hood_installation_requirements_form_handler,
    ),
    path(
        "Cooker-Instllation-Requirements-Form/<int:ticket_device_id>",
        handlers.cooker_installation_requirements_form_handler,
    ),
]
