from . import models
from rest_framework import serializers


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(ClientsSerializer, self).to_representation(instance)
        rep["client_category_name"] = instance.client_category.client_category
        rep["client_city_name"] = instance.client_city.city_name
        rep["client_region_name"] = instance.client_region.region_name

        return rep


class ClientDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientDevice
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(ClientDeviceSerializer, self).to_representation(instance)
        rep["device_brand"] = instance.related_storage_item.brand
        rep["device_category"] = instance.related_storage_item.category
        rep["device_model_number"] = instance.related_storage_item.item_model_number
        rep["related_branch_name"] = instance.related_branch
        rep["related_distributor_name"] = instance.related_distributor
        return rep
