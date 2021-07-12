from . import models
from rest_framework import serializers


class AccountsSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
