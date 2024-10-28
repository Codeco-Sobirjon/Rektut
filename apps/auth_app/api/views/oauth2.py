from rest_framework.authentication import TokenAuthentication

from apps.auth_app.api.serializers import google_serializers as auth_serializers
from apps.auth_app.api.serializers import serializers
from apps.auth_app.api.generic.generic_api_view import GenericAPIView
from apps.auth_app.api.services.serivices import OauthService
from apps.auth_app.models import CustomUser
# from apps.companies.services.users import AuthService, EmailService, OauthService, TokenService, UserService
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class GoogleModelViewSet(GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = auth_serializers.SocialAuthSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication]

    SERIALIZER = {
        "social_media_auth": {
            "request": auth_serializers.SocialAuthSerializer,
            "response": serializers.InformationSerializer,
        },
    }

    @swagger_auto_schema(
        request_body=SERIALIZER["social_media_auth"]["request"],
        responses={
            201: SERIALIZER["social_media_auth"]["response"],
            404: openapi.Response(
                description="Пример ответа при неверном логине или пароле",
                examples={"application/json": {"detail": CustomUser.Text.WRONG_PASSWORD_OR_LOGIN_ENTERED}},
            ),
        },
    )
    def social_media_auth(self, request, *args, **kwargs):
        """
        For social media authentication use this endpoint
        need to enter code and social_media_type
            code(get the field social media authentication url)
            social_media_type(need to enter social media type ['google_auth', 'yandex_auth', 'vk_auth', 'mail_ru_auth']

        Additional docs and url for get code:
            google_auth:
                - https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id=164988481338-dadkp1t0dnkiauagsiq088qm4a519cnu.apps.googleusercontent.com&scope=email&response_type=code&redirect_uri=https://example.com&access_type=offline
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            social_auth = OauthService(**serializer.data)
            user, is_created = social_auth.get_social_auth()
            data = self.get_serializer_response(user, context=self.get_serializer_context())
            return Response(data=data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response(data={"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST, exception=True)