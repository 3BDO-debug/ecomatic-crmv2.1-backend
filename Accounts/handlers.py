from . import models, serializers
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication


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
@authentication_classes([])
@permission_classes([])
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
@authentication_classes([])
@permission_classes([])
def signup_handler(request):
    print(request.data)
    models.User.objects.create_user(
        first_name=request.data.get("firstName"),
        last_name=request.data.get("lastName"),
        email=request.data.get("email"),
        username=request.data.get("username"),
        phone_number=request.data.get("phoneNumber"),
        address=request.data.get("address"),
        gov_id=request.data.get("govId"),
        password=request.data.get("password"),
        role=request.data.get("role"),
        personal_pic=request.data.get("profilePic")["preview"],
        device_identifier="device_identifier",
    )
    return Response(status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
def user_info_handler(request):
    user = models.User.objects.get(id=request.user.id)
    user_serializer = serializers.AccountsSerializers(user, many=False)
    return Response(user_serializer.data)


@api_view(["POST"])
def signout_handler(request):
    refresh_token = request.data.get("refresh_token")
    token = RefreshToken(refresh_token)
    token.blacklist()
    return Response(status=status.HTTP_205_RESET_CONTENT)


@api_view(["GET"])
def account_details_handler(request, account_id):
    user = models.User.objects.get(id=int(account_id))
    user_serializer = serializers.AccountsSerializers(user, many=False)
    return Response(user_serializer.data)
