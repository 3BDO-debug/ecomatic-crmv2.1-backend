from . import handlers
from django.urls import path

urlpatterns = [
    path("Warehouses", handlers.warehouses_handler),
    path("Items", handlers.items_handler),
    path("Spareparts", handlers.spare_parts_handler),
    path("Custody", handlers.custody_handler),
    # path("technitian_custody", handlers.technitian_custody_handler)
]
