from . import models
from rest_framework import serializers


class WarehouseSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Warehouse
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(WarehouseSerializers, self).to_representation(instance)
        rep["assigned_to_name"] = instance.assigned_to.username
        return rep





class ItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = "__all__"


class SparePartSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.SparePart
        fields = "__all__"


class CustodySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Custody
        fields = "__all__"


class TechnicianCustodySerializers(serializers.ModelSerializer):
    class Meta:
        model = models.TechnicianCustody
        fields = "__all__"
