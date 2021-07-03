from . import models, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login


@api_view(["GET"])
def accounts_handler(request, account_type):
    if account_type == "Employees":
        accounts = models.User.objects.all().exclude(role="technician")
        account_serializer = serializers.AccountsSerializers(accounts, many=True)
        return Response(account_serializer.data)
    elif account_type == "Technicians":
        accounts = models.User.objects.filter(role="technician")
        account_serializer = serializers.AccountsSerializers(accounts, many=True)
        return Response(account_serializer.data)

    elif account_type == "Store-Keepers":
        accounts = models.User.objects.filter(role="store_keeper")
        account_serializer = serializers.AccountsSerializers(accounts, many=True)
        return Response(account_serializer.data)


@api_view(["POST"])
def email_username_lookup_handler(request):

    if models.User.objects.filter(
        email=request.data.get("email")
    ).count() > 0 and request.data.get("email"):
        return Response(data={"exist": True})
    elif models.User.objects.filter(
        username=request.data.get("username")
    ).count() > 0 and request.data.get("username"):
        return Response(data={"exist": True})
    else:
        return Response(data={"exist": False})


@api_view(["POST"])
def signup_handler(request):
    models.User.objects.create_user(
        first_name=request.data.get("firstName"),
        last_name=request.data.get("lastName"),
        email=request.data.get("email"),
        username=request.data.get("username"),
        phone_number=request.data.get("phoneNumber"),
        address=request.data.get("address"),
        gov_id=request.data.get("govId"),
        password=request.data.get("password"),
        role=request.data.get("userRole"),
        personal_pic=request.data.get("profilePic"),
        device_identifier="device_identifier",
    )
    return Response(status=status.HTTP_201_CREATED)


@api_view(["POST"])
def signin_handler(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user_to_be_authenticated = authenticate(
        request, username=username, password=password
    )
    if user_to_be_authenticated:
        user_serializer = serializers.AccountsSerializers(
            user_to_be_authenticated, many=False
        )
        login(request, user_to_be_authenticated)
        return Response(status=status.HTTP_200_OK, data=user_serializer.data)
