from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import models, serializers


@api_view(["GET"])
def brands_handlers(request):
    brands = models.Brand.objects.all()
    brands_serializer = serializers.BrandSerializer(brands, many=True)
    return Response(brands_serializer.data)


@api_view(["GET"])
def categories_handlers(request):
    categories = models.Category.objects.all()
    categories_serializer = serializers.CategorySerializer(categories, many=True)
    return Response(categories_serializer.data)


@api_view(["GET"])
def branches_handler(request):
    branches = models.Branch.objects.all()
    branches_serializer = serializers.BranchSerializer(branches, many=True)
    return Response(branches_serializer.data)


@api_view(["GET"])
def distributors_handler(request):
    distributors = models.Distributor.objects.all()
    distributors_serializer = serializers.DistributorSerializer(distributors, many=True)
    return Response(distributors_serializer.data)


@api_view(["GET"])
def ticket_types_handler(request):
    ticket_types = models.TicketType.objects.all()
    ticket_types_serializer = serializers.TicketTypeSerializer(ticket_types, many=True)
    return Response(ticket_types_serializer.data)


@api_view(["GET"])
def ticket_status_handler(request):
    ticket_status = models.TicketStatus.objects.all()
    ticket_status_serializer = serializers.TicketStatusSerializer(
        ticket_status, many=True
    )
    return Response(ticket_status_serializer.data)


@api_view(["GET"])
def common_diagnostics_handler(request, category_name):
    common_diagnostics = models.CommonDiagnostics.objects.filter(
        related_category=models.Category.objects.get(category_name=category_name)
    )
    common_diagnostics_serializer = serializers.CommonDiagnosticSerializer(
        common_diagnostics, many=True
    )
    return Response(common_diagnostics_serializer.data)


@api_view(["GET"])
def clients_categories_handler(request):
    clients_categories = models.ClientCategory.objects.all()
    clients_categories_serializer = serializers.ClientCategorySerializer(
        clients_categories, many=True
    )
    return Response(data=clients_categories_serializer.data)
