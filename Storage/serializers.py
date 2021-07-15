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


class CustodySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Custody
        fields = "__all__"


class CustodySparepartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustodySparepart
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(CustodySparepartSerializer, self).to_representation(instance)
        rep["related_custody_name"] = instance.related_custody.custody_name
        rep["assigned_sparepart_name"] = instance.assigned_sparepart.spare_part_name
        rep[
            "assigned_sparepart_model_number"
        ] = instance.assigned_sparepart.spare_part_model_number
        rep["assigned_sparepart_img"] = instance.assigned_sparepart.spare_part_img.name

        return rep
