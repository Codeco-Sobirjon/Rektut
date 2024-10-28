from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.ads.filter import filter_by_title, filter_by_category, filter_by_city, filter_is_top_ads, filter_is_pop_ads
from apps.ads.models import *
from apps.ads.api.serializers.serializers import (
    CategoryListSerializers,
    CountryListSerializers, CityListSerializers,
    OptionalFieldListSerializers, OptionalFieldThroughListSerializers,
    JobListSerializers, JobDetailSerializers, CategoryDetailSerializers
)
from utils.responses import (
    bad_request_response,
    success_response,
    success_created_response,
    success_deleted_response,
)
from utils.expected_fields import check_required_key
from utils.renderers import UserRenderers
from utils.pagination import PaginationMethod, StandardResultsSetPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class JobListView(APIView, PaginationMethod):
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "job_category",
        "title",
        "category",
        "city"
    ]

    job_category_param = openapi.Parameter('job_category', openapi.IN_QUERY, description="Filter by job category",
                                           type=openapi.TYPE_STRING)
    title_param = openapi.Parameter('title', openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING)
    category_param = openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category",
                                       type=openapi.TYPE_STRING)
    city_param = openapi.Parameter('city', openapi.IN_QUERY, description="Filter by city", type=openapi.TYPE_STRING)
    is_top_param = openapi.Parameter('isTop', openapi.IN_QUERY, description="Filter by top ads",
                                     type=openapi.TYPE_BOOLEAN)
    is_pop_param = openapi.Parameter('isPop', openapi.IN_QUERY, description="Filter by popular ads",
                                     type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(manual_parameters=[job_category_param, title_param, category_param, city_param, is_top_param,
                                            is_pop_param],
                         operation_description="Retrieve a list of jobs",
                         tags=['Ads'],
                         responses={200: JobListSerializers(many=True)})
    def get(self, request):
        queryset = Job.objects.all().order_by('-id')
        queryset = filter_by_title(queryset, request)
        queryset = filter_by_category(queryset, request)
        queryset = filter_by_city(queryset, request)
        queryset = filter_is_top_ads(queryset, request)
        queryset = filter_is_pop_ads(queryset, request)
        serializers = super().page(queryset, JobDetailSerializers, request)
        return success_response(serializers.data)

class MyAdsListViews(APIView):
    permission_classes = [IsAuthenticated, AllowAny]
    renderer_classes = [UserRenderers]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "job_category",
        "title",
        "category",
        "city"
    ]

    job_category_param = openapi.Parameter('job_category', openapi.IN_QUERY, description="Filter by job category",
                                           type=openapi.TYPE_STRING)
    title_param = openapi.Parameter('title', openapi.IN_QUERY, description="Filter by title", type=openapi.TYPE_STRING)
    category_param = openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category",
                                       type=openapi.TYPE_STRING)
    city_param = openapi.Parameter('city', openapi.IN_QUERY, description="Filter by city", type=openapi.TYPE_STRING)
    is_top_param = openapi.Parameter('isTop', openapi.IN_QUERY, description="Filter by top ads",
                                     type=openapi.TYPE_BOOLEAN)
    is_pop_param = openapi.Parameter('isPop', openapi.IN_QUERY, description="Filter by popular ads",
                                     type=openapi.TYPE_BOOLEAN)

    @swagger_auto_schema(manual_parameters=[job_category_param, title_param, category_param, city_param, is_top_param,
                                            is_pop_param],
                         operation_description="Retrieve a list of jobs",
                         tags=['MyAds'],
                         responses={200: JobListSerializers(many=True)})
    def get(self, request):
        queryset = Job.objects.select_related('user').filter(user=request.user).order_by('-id')
        queryset = filter_by_title(queryset, request)
        queryset = filter_by_category(queryset, request)
        queryset = filter_by_city(queryset, request)
        queryset = filter_is_top_ads(queryset, request)
        queryset = filter_is_pop_ads(queryset, request)
        serializers = super().page(queryset, JobDetailSerializers, request)
        return success_response(serializers.data)


class AdsCreateView(APIView):
    permission_classes = [IsAuthenticated, AllowAny]
    renderer_classes = [UserRenderers]

    @swagger_auto_schema(request_body=JobListSerializers,
                         operation_description="Ads Create",
                         tags=['Ads'],
                         responses={201: JobListSerializers(many=False)})
    def post(self, request):
        valid_fields = {'title', 'category', 'city', 'description', 'contact_number', 'email', 'name',
                        'user', 'status', 'photo', 'date_create', 'date_update', 'is_top', 'is_vip', 'additionally'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = JobListSerializers(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)
    

class AdsDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_description="Ads get by id",
                         tags=['Ads'],
                         responses={200: JobDetailSerializers(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(Job, pk=pk)
        serializers = JobDetailSerializers(queryset)
        return success_response(serializers.data)

    @swagger_auto_schema(request_body=JobListSerializers,
                         operation_description="Ads update",
                         tags=['Ads'],
                         responses={200: JobListSerializers(many=False)})
    def put(self, request, pk):
        queryset = get_object_or_404(Job, pk=pk)
        serializers = JobListSerializers(instance=queryset, data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    @swagger_auto_schema(operation_description="Delete a ads",
                         tags=['Ads'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(Job, pk=pk)
        queryset.delete()
        return success_response('Ads deleted')



