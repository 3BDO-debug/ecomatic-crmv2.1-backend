from . import handlers
from django.urls import path

urlpatterns = [
    path("Email-Username-lookup", handlers.email_username_lookup_handler),
    path("Employees-Data/<str:account_type>", handlers.accounts_handler),
    path("Signup", handlers.signup_handler),
    path("Signin", handlers.signin_handler),
]
