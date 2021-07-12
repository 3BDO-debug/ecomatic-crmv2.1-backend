from . import models
from rest_framework import serializers


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(ClientsSerializer, self).to_representation(instance)
        rep["client_category_name"] = instance.client_category.client_category

        return rep


class ClientDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientDevice
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(ClientDeviceSerializer, self).to_representation(instance)
        rep["device_brand"] = instance.related_storage_item.brand
        rep["device_category"] = instance.related_storage_item.category
        rep["device_name"] = instance.related_storage_item.item_name
        rep["device_model_number"] = instance.related_storage_item.item_model_number
        rep["related_branch_name"] = instance.related_branch.branch_name
        rep["related_distributor_name"] = instance.related_distributor.distributor_name
        return rep
