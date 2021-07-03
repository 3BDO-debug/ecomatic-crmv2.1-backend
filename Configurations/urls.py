from django.urls import path
from . import handlers


urlpatterns = [
    path("Brands", handlers.brands_handlers),
    path("Categories", handlers.categories_handlers),
    path("Branches", handlers.branches_handler),
    path("Distributors", handlers.distributors_handler),
    path("Ticket-Types", handlers.ticket_types_handler),
    path("Ticket-Status", handlers.ticket_status_handler),
    path("Common-Diagnostics/<str:category_name>", handlers.common_diagnostics_handler),
]
