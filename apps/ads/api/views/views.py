from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from apps.ads.models import *
from apps.ads.api.serializers.serializers import (
    CategoryListSerializers,
    CountryListSerializers, CityListSerializers,
    CategoryDetailSerializers, CitySerializer, OptionalFieldListSerializers
)
from utils.responses import (
    bad_request_response,
    success_response,
    success_created_response,
    success_deleted_response,
)

from utils.expected_fields import check_required_key
from drf_yasg.utils import swagger_auto_schema


class CategoryListView(APIView):
    permission_classes = [AllowAny]
    """ Category Get View """

    @swagger_auto_schema(operation_description="Retrieve a list of categories",
                         tags=['Categories'],
                         responses={200: CategoryListSerializers(many=True)})
    def get(self, request):
        queryset = Category.objects.all().order_by('-id')
        serializers = CategoryDetailSerializers(queryset, many=True,
                                              context={'request': request})
        return success_response(serializers.data)

    """ Category Post View """

    @swagger_auto_schema(request_body=CategoryListSerializers,
                         operation_description="Category create",
                         tags=['Categories'],
                         responses={201: CategoryListSerializers(many=False)})
    def post(self, request):
        valid_fields = {'name', 'subcategory', 'icon'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializers = CategoryListSerializers(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CategoryDetailView(APIView):
    permission_classes = [AllowAny]
    """ Category Get View """

    @swagger_auto_schema(operation_description="Retrieve a category",
                         tags=['Categories'],
                         responses={200: CategoryListSerializers(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(Category, pk=pk)
        serializers = CategoryDetailSerializers(queryset, context={'request': request})
        return success_response(serializers.data)

    """ Category Put View """

    @swagger_auto_schema(request_body=CategoryListSerializers,
                         operation_description="Category update",
                         tags=['Categories'],
                         responses={200: CategoryListSerializers(many=False)})
    def put(self, request, pk):
        valid_fields = {'name', 'subcategory', 'icon'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(Category, pk=pk)
        serializers = CategoryListSerializers(instance=queryset, data=request.data,
                                              context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    """ Category Delete View """

    @swagger_auto_schema(operation_description="Delete a category",
                         tags=['Categories'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(Category, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")


class CountryListView(APIView):
    permission_classes = [AllowAny]
    """ Category Get View """

    @swagger_auto_schema(operation_description="Retrieve a list of country",
                         tags=['Country'],
                         responses={200: CountryListSerializers(many=True)})
    def get(self, request):
        queryset = Country.objects.all().order_by('-id')
        serializers = CountryListSerializers(queryset, many=True,
                                              context={'request': request})
        return success_response(serializers.data)

    """ Category Post View """

    @swagger_auto_schema(request_body=CountryListSerializers,
                         operation_description="Country create",
                         tags=['Country'],
                         responses={201: CountryListSerializers(many=False)})
    def post(self, request):
        valid_fields = {'name'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializers = CountryListSerializers(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CountryDetailView(APIView):
    permission_classes = [AllowAny]
    """ Country Get View """

    @swagger_auto_schema(operation_description="Retrieve a country",
                         tags=['Country'],
                         responses={200: CategoryListSerializers(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(Country, pk=pk)
        serializers = CountryListSerializers(queryset, context={'request': request})
        return success_response(serializers.data)

    """ Country Put View """

    @swagger_auto_schema(request_body=CountryListSerializers,
                         operation_description="Country update",
                         tags=['Country'],
                         responses={200: CountryListSerializers(many=False)})
    def put(self, request, pk):
        valid_fields = {'name'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(Country, pk=pk)
        serializers = CountryListSerializers(instance=queryset, data=request.data,
                                              context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    """ Country Delete View """

    @swagger_auto_schema(operation_description="Delete a country",
                         tags=['Country'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(Country, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")


class CityListView(APIView):
    permission_classes = [AllowAny]
    """ City Get View """

    @swagger_auto_schema(operation_description="Retrieve a list of cities",
                         tags=['City'],
                         responses={200: CategoryListSerializers(many=True)})
    def get(self, request):
        queryset = City.objects.all().order_by('-id')
        serializers = CitySerializer(queryset, many=True,
                                              context={'request': request})
        return success_response(serializers.data)

    """ City Post View """

    @swagger_auto_schema(request_body=CountryListSerializers,
                         operation_description="City create",
                         tags=['City'],
                         responses={201: CountryListSerializers(many=False)})
    def post(self, request):
        valid_fields = {'name'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializers = CityListSerializers(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CityDetailViews(APIView):
    permission_classes = [AllowAny]
    """ City Get View """

    @swagger_auto_schema(operation_description="Retrieve a city",
                         tags=['City'],
                         responses={200: CityListSerializers(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(City, pk=pk)
        serializers = CitySerializer(queryset, context={'request': request})
        return success_response(serializers.data)

    """ City Put View """

    @swagger_auto_schema(request_body=CityListSerializers,
                         operation_description="City update",
                         tags=['City'],
                         responses={201: CityListSerializers(many=False)})
    def put(self, request, pk):
        valid_fields = {'name'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(City, pk=pk)
        serializers = CityListSerializers(instance=queryset, data=request.data,
                                              context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    """ City Delete View """

    @swagger_auto_schema(operation_description="Delete a city",
                         tags=['City'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(City, pk=pk)
        queryset.delete()
        return success_deleted_response("Successfully deleted")


class OptionalFieldListView(APIView):
    permission_classes = [AllowAny]
    """ OptionalField Get View """

    @swagger_auto_schema(operation_description="Retrieve a list of optional Field",
                         tags=['Optional Field'],
                         responses={200: OptionalFieldListSerializers(many=True)})
    def get(self, request):
        queryset = OptionalField.objects.all().order_by('-id')
        serializers = OptionalFieldListSerializers(queryset, many=True,
                                              context={'request': request})
        return success_response(serializers.data)
