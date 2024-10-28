from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from apps.auth_app.api.serializers.serializers import (
    RegisterSerializer,
    InformationSerializer,
    LoginSerializer, GoogleSocialAuthSerializer,
    UpdateSerializer, ResetPasswordSerializer
)
from utils.expected_fields import check_required_key
from utils.renderers import UserRenderers
from utils.responses import bad_request_response, success_created_response, success_response, success_deleted_response
from utils.token import get_token_for_user


class GoogleSocialAuthView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleSocialAuthSerializer

    @swagger_auto_schema(request_body=GoogleSocialAuthSerializer,
                         operation_description="Login with google",
                         tags=['Google'],
                         responses={201: GoogleSocialAuthSerializer(many=False)})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class RegisterViews(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=RegisterSerializer,
                         operation_description="User create",
                         tags=['Sign Up'],
                         responses={201: RegisterSerializer(many=False)})
    def post(self, request):
        valid_fields = {"first_name", "last_name", 'photo', 'about', 'phone', 'email', 'groups', 'password'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.instance
            token = get_token_for_user(user)
            return success_created_response(token)
        return bad_request_response(serializer.errors)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer,
                         operation_description="User login",
                         tags=['Sign In'],
                         responses={201: LoginSerializer(many=False)})
    def post(self, request, *args, **kwargs):
        expected_fields = {"phone", "password"}
        received_fields = set(request.data.keys())
        unexpected_fields = received_fields - expected_fields

        if unexpected_fields:
            return bad_request_response(
                f"Unexpected fields: {', '.join(unexpected_fields)}"
            )

        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token = self.generate_user_token(user)

        return success_response(token)

    def get_serializer(self, *args, **kwargs):
        return LoginSerializer(*args, **kwargs)

    def generate_user_token(self, user):
        return get_token_for_user(user)


class ProfileViews(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]

    @swagger_auto_schema(operation_description="Retrieve a user",
                         tags=['Profile'],
                         responses={200: InformationSerializer(many=True)})
    def get(self, request):
        serializer = InformationSerializer(request.user, context={'request': request} )
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=RegisterSerializer,
                         operation_description="User update",
                         tags=['Profile'],
                         responses={200: RegisterSerializer(many=False)})
    def put(self, request):
        valid_fields = {"first_name", "last_name", 'photo', 'about', 'phone', 'email', 'password'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = UpdateSerializer(request.user, data=request.data, partial=True,
                                              context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    @swagger_auto_schema(operation_description="Delete a user",
                         tags=['Profile'],
                         responses={204: 'No content'})
    def delete(self, request):
        request.user.delete()
        return success_deleted_response("User deleted")


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=ResetPasswordSerializer,
                         operation_description="Reset Password",
                         tags=['Profile'],
                         responses={200: ResetPasswordSerializer(many=False)})
    def post(self, request, *args, **kwargs):
        valid_fields = {'email', 'password'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response('Password has been reset successfully.')
        return bad_request_response(serializer.errors)