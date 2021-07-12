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


class SparepartRequest(serializers.ModelSerializer):
    class Meta:
        model = models.SparepartRequest
        fields = "__all__"
