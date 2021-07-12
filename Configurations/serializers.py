from rest_framework import serializers
from . import models


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


class CommonDiagnosticSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CommonDiagnostics
        fields = "__all__"


class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ClientCategory
        fields = "__all__"
