from rest_framework import serializers
from apps.auth_app.api.serializers.serializers import BaseUserSerializer


class AuthLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class SocialAuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=250)
    social_media_type = serializers.ChoiceField(choices=["google_auth"])


class AuthSocialLoginSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields

