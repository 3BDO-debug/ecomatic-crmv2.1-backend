from . import handlers
from django.urls import path

urlpatterns = [
    path("Email-Username-lookup", handlers.email_username_lookup_handler),
    path("Employees-Data/<str:account_type>", handlers.accounts_handler),
    path("Signup", handlers.signup_handler),
    path("User-Info", handlers.user_info_handler),
    path("Signout", handlers.signout_handler),
    path("Account-Details/<int:account_id>", handlers.account_details_handler),
]
