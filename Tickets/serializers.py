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
        rep["client_address"] = instance.related_client.client_address
        rep["client_city"] = instance.related_client.client_city.city_name
        rep["client_region"] = instance.related_client.client_region.region_name
        rep["client_building_no"] = instance.related_client.client_building_no
        rep["client_apartment_no"] = instance.related_client.client_apartment_no
        rep["client_floor_no"] = instance.related_client.client_floor_no
        rep["client_landmark"] = instance.related_client.client_address_landmark

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
            "device_model_number"
        ] = instance.related_client_device.related_storage_item.item_model_number
        rep["device_brand"] = instance.related_client_device.related_storage_item.brand
        rep[
            "device_category"
        ] = instance.related_client_device.related_storage_item.category
        rep[
            "device_feeding_source"
        ] = instance.related_client_device.device_feeding_source
        rep["manufacturing_date"] = instance.related_client_device.manufacturing_date
        rep["purchasing_date"] = instance.related_client_device.purchasing_date
        rep["installation_date"] = instance.related_client_device.installation_date
        rep[
            "expected_warranty_start_date"
        ] = instance.related_client_device.expected_warranty_start_date
        rep["warranty_start_date"] = instance.related_client_device.warranty_start_date
        rep["in_warranty"] = instance.related_client_device.in_warranty
        rep[
            "installed_through_the_company"
        ] = instance.related_client_device.installed_through_the_company
        rep[
            "device_invoice_or_manufacturer_label"
        ] = instance.related_client_device.device_invoice_or_manufacturer_label.name
        return rep


class TicketDeviceSparepartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketDeviceSpareparts
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(TicketDeviceSparepartsSerializer, self).to_representation(instance)
        rep[
            "spare_part_model_number"
        ] = instance.assigned_sparepart.spare_part_model_number
        rep["spare_part_price"] = instance.assigned_sparepart.spare_part_price
        return rep


class TicketDeviceServicepartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketDeviceService
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(TicketDeviceServicepartsSerializer, self).to_representation(
            instance
        )
        rep["service_name"] = instance.assigned_service.service_name
        rep["service_price"] = instance.assigned_service.service_price

        return rep


class TicketFollowbackCallRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketFollowbackCallRating

        fields = "__all__"


""" Ticket Completion Forms """


class GasOvenInstallationRequirementsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GasOvenInstallationRequirementsForm
        fields = "__all__"


class ElectricOvenInstallationRequirementsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ElectricOvenInstallationRequirementsForm
        fields = "__all__"


class SlimHobInstallationRequirementsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SlimHobInstallationRequirementsForm
        fields = "__all__"


class CookerInstallationRequirementsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CookerInstallationRequirementsForm
        fields = "__all__"


class HoodInstallationRequirementsFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HoodInstallationRequirementsForm
        fields = "__all__"


""" End Ticket Completeion Forms """
