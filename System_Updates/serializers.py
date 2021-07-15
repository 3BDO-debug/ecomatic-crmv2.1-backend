from rest_framework import serializers
from . import models


class UpdateTicketStatusRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UpdateTicketStatusRequest
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(UpdateTicketStatusRequestSerializer, self).to_representation(
            instance
        )
        rep["related_ticket_id"] = instance.related_ticket.id
        return rep


class TicketLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketLog
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(TicketLogSerializer, self).to_representation(instance)
        rep[
            "created_by_name"
        ] = f"{instance.created_by.first_name} {instance.created_by.last_name}"
        rep["created_by_role"] = instance.created_by.role
        return rep


class SparepartRequest(serializers.ModelSerializer):
    class Meta:
        model = models.SparepartRequest
        fields = "__all__"


class MissingDataRequest(serializers.ModelSerializer):
    class Meta:
        model = models.MissingDataRequest
        fields = "__all__"
