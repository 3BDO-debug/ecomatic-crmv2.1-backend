from . import models
from rest_framework import serializers


class TicketSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(TicketSerializers, self).to_representation(instance)
        rep["client_name"] = instance.related_client.client_full_name
        rep["client_phone_number_1"] = instance.related_client.client_phone_number_1
        rep["client_phone_number_2"] = instance.related_client.client_phone_number_2
        rep["client_landline_number"] = instance.related_client.client_landline_number
        rep["client_address_1"] = instance.related_client.client_address_1
        rep["client_address_2"] = instance.related_client.client_address_2
        rep["technician_name"] = (
            f"{instance.related_technician.first_name} {instance.related_technician.last_name}"
            if instance.related_technician
            else "Technician Not Selected Yet"
        )
        rep["technician_profile_pic"] = (
            instance.related_technician.personal_pic.name
            if instance.related_technician
            else "Technician Not Selected Yet"
        )
        return rep


class TicketDeviceSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.TicketDevice
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(TicketDeviceSerializers, self).to_representation(instance)
        rep[
            "device_name"
        ] = instance.related_client_device.related_storage_item.item_name
        rep[
            "device_model_number"
        ] = instance.related_client_device.related_storage_item.item_model_number
        rep["device_brand"] = instance.related_client_device.related_storage_item.brand
        rep[
            "device_category"
        ] = instance.related_client_device.related_storage_item.category
        rep[
            "device_feeding_source"
        ] = instance.related_client_device.device_feeding_source

        return rep


class TicketDeviceSparepartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketDeviceSpareparts
        fields = "__all__"


class TicketUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.TicketUpdate
        fields = "__all__"
