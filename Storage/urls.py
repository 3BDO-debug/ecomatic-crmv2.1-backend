from . import handlers
from django.urls import path

urlpatterns = [
    path("Warehouses", handlers.warehouses_handler),
    path("Items", handlers.items_handler),
    path("Spareparts", handlers.spare_parts_handler),
    path("Custodies", handlers.custodies_handler),
    path("Custody-Details/<int:custody_id>", handlers.custody_details_handler),
]
