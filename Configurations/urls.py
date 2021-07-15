from django.urls import path
from . import handlers


urlpatterns = [
    path("Brands", handlers.brands_handlers),
    path("Categories", handlers.categories_handlers),
    path("Branches", handlers.branches_handler),
    path("Distributors", handlers.distributors_handler),
    path("Ticket-Types", handlers.ticket_types_handler),
    path("Ticket-Status", handlers.ticket_status_handler),
    path("Ticket-Services", handlers.ticket_services_handler),
    path("Common-Diagnostics/<str:category_name>", handlers.common_diagnostics_handler),
    path("Clients-Categories", handlers.clients_categories_handler),
    path(
        "Technician-Assigned-Custodies/<int:technicain_id>",
        handlers.technicain_assigned_custodies_handler,
    ),
    path("Cities", handlers.cities_handler),
    path("Regions", handlers.regions_handler),
]
