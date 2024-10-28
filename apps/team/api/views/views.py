from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.team.models import *
from apps.team.api.serializers.serializers import (
    TeamRoleListSerializers,
    TeamListSerializers,
    TeamDetailSerializers
)
from utils.responses import (
    bad_request_response,
    success_response,
    success_created_response,
    success_deleted_response,
)
from utils.expected_fields import check_required_key
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class TeamRoleListViews(APIView):
    permission_classes = [AllowAny]

    """ Team Role Get View """

    @swagger_auto_schema(operation_description="Retrieve a list of team role",
                         tags=['Team Role'],
                         responses={200: TeamRoleListSerializers(many=True)})
    def get(self, request):
        queryset = TeamRole.objects.all().order_by('-id')
        serializer = TeamRoleListSerializers(queryset, many=True)
        return success_response(serializer.data)

    """ Team Role Post View """

    @swagger_auto_schema(request_body=TeamRoleListSerializers,
                         operation_description="Team Role create",
                         tags=['Team Role'],
                         responses={201: TeamRoleListSerializers(many=False)})
    def post(self, request):
        valid_fields = {"name"}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = TeamRoleListSerializers(data=request.data,
                                             context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_created_response(serializer.data)
        return bad_request_response(serializer.errors)


class TeamRoleDetailsViews(APIView):
    permission_classes = [AllowAny]

    """ Team Role Get View """

    @swagger_auto_schema(operation_description="Retrieve a team role",
                         tags=['Team Role'],
                         responses={200: TeamRoleListSerializers(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(TeamRole, pk=pk)
        serializer = TeamRoleListSerializers(queryset)
        return success_response(serializer.data)

    """ Team Role Put View """

    @swagger_auto_schema(request_body=TeamRoleListSerializers,
                         operation_description="Team Role update",
                         tags=['Team Role'],
                         responses={200: TeamRoleListSerializers(many=False)})
    def put(self, request, pk):
        valid_fields = {"name"}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(TeamRole, pk=pk)
        serializer = TeamRoleListSerializers(
            instance=queryset, data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    """ Team Role Delete View """

    @swagger_auto_schema(operation_description="Delete a Team Role",
                         tags=['Team Role'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(TeamRole, pk=pk)
        queryset.delete()
        return success_deleted_response('Successfully deleted')


class TeamListViews(APIView):
    permission_classes = [AllowAny]

    """ Team Get View """

    @swagger_auto_schema(operation_description="Retrieve a list of Team",
                         tags=['Team'],
                         responses={200: TeamDetailSerializers(many=True)})
    def get(self, request):
        queryset = Team.objects.all().order_by('-id')
        serializer = TeamDetailSerializers(queryset, many=True)
        return success_response(serializer.data)

    """ Team Post View """

    @swagger_auto_schema(request_body=TeamListSerializers,
                         operation_description="Team create",
                         tags=['Team'],
                         responses={201: TeamListSerializers(many=False)})
    def post(self, request):
        valid_fields = {'name', 'description', 'photo', 'role'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = TeamListSerializers(data=request.data,
                                             context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_created_response(serializer.data)
        return bad_request_response(serializer.errors)


class TeamDetailsViews(APIView):
    permission_classes = [AllowAny]

    """ Team Get View """

    @swagger_auto_schema(operation_description="Retrieve a Team",
                         tags=['Team'],
                         responses={200: TeamDetailSerializers(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(Team, pk=pk)
        serializer = TeamDetailSerializers(queryset)
        return success_response(serializer.data)

    """ Team Put View """

    @swagger_auto_schema(request_body=TeamListSerializers,
                         operation_description="Team update",
                         tags=['Team'],
                         responses={200: TeamListSerializers(many=False)})
    def put(self, request, pk):
        valid_fields = {'name', 'description', 'photo', 'role'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        queryset = get_object_or_404(Team, pk=pk)
        serializer = TeamListSerializers(
            instance=queryset, data=request.data, context={'request': request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    """ Team Delete View """

    @swagger_auto_schema(operation_description="Delete a Team",
                         tags=['Team'],
                         responses={204: 'No content'})
    def delete(self, request, pk):
        queryset = get_object_or_404(Team, pk=pk)
        queryset.delete()
        return success_deleted_response('Successfully deleted')


