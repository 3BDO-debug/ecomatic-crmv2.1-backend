from rest_framework import serializers
from . import models
from Storage import serializers as Storage_Serializers


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(CategorySerializer, self).to_representation(instance)
        rep["related_brand_name"] = instance.related_brand.brand_name
        return rep


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = "__all__"


class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Distributor
        fields = "__all__"


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketType
        fields = "__all__"


class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketStatus
        fields = "__all__"


class TicketServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TicketService
        fields = "__all__"


class CommonDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommonDiagnostics
        fields = "__all__"


class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientCategory
        fields = "__all__"


class TechnicianAssignedCustodySerializer(serializers.ModelSerializer):
    assigned_custodies = Storage_Serializers.CustodySerializer(
        read_only=True, many=True
    )

    class Meta:
        model = models.TechnicianAssignedCustody
        fields = ("assigned_custodies", "created_at")


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.City
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = "__all__"

    def to_representation(self, instance):
        rep = super(RegionSerializer, self).to_representation(instance)
        rep["related_city_name"] = instance.related_city.city_name
        return rep


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Route
        fields = "__all__"
