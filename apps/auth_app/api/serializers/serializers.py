import os

from django.conf import settings
from django.core.validators import MaxLengthValidator
from jsonschema._keywords import required
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from apps.auth_app.api.register import register_social_user
from apps.auth_app.email_utils import Util
from apps.auth_app.generate_password import generate_random_string
from apps.auth_app.models import (
    CustomUser,
)
from apps.auth_app.api import google


class IncorrectCredentialsError(serializers.ValidationError):
    pass


class UnverifiedAccountError(serializers.ValidationError):
    pass


class GroupsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name']


class BaseUserSerializer(serializers.ModelSerializer):
    phone = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    groups = GroupsSerializers(read_only=True, many=True)

    class Meta:
        model = get_user_model()
        fields = ["id", "email", "phone", "groups",]


class RegisterSerializer(serializers.ModelSerializer):
    groups = serializers.IntegerField(required=True)
    photo = serializers.ImageField(required=False, default=None)
    password = serializers.CharField(max_length=50, min_length=1, write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ["first_name", "last_name", 'about', 'photo', 'password']
        extra_kwargs = {
            "password": {"required": True},
        }

    def create(self, validated_data):
        groups_data = validated_data.pop("groups", None)
        user = CustomUser.objects.create_user(**validated_data)
        user.avatar = validated_data['photo']
        user.set_password(validated_data['password'])
        user.photo = validated_data['photo']
        if groups_data:
            try:
                role = Group.objects.get(id=groups_data)
                user.groups.add(role)
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'groups': "Invalid group ID"})
        user.save()
        return user


class UpdateSerializer(BaseUserSerializer):
    first_name = serializers.CharField(max_length=50, validators=[
        MaxLengthValidator(limit_value=50, message="First name cannot exceed 50 characters.")])
    last_name = serializers.CharField(max_length=50, validators=[
        MaxLengthValidator(limit_value=50, message="Last name cannot exceed 50 characters.")])
    password = serializers.CharField(max_length=50, required=False)
    photo = serializers.ImageField(write_only=False, required=False)
    phone = serializers.CharField(max_length=50, required=False)
    email = serializers.EmailField(required=False)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ["first_name", "last_name", 'photo',
                                                   'password',]  # Removed 'categories'

    def validate(self, attrs):
        phone = attrs.get('phone', None)
        email = attrs.get('email', None)

        if not phone and not email:
            raise serializers.ValidationError("Either a phone number or an email must be provided.")

        if phone and CustomUser.objects.filter(phone=phone).exists():
            raise serializers.ValidationError("This phone number is already in use.")

        if email and CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already in use.")

        return attrs

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            validated_data.pop('password')
        if 'photo' in validated_data:
            instance.photo = validated_data.get('photo', instance.photo)

        instance = super(UpdateSerializer, self).update(instance, validated_data)
        instance.save()
        return instance


class InformationSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ["first_name", "last_name",
                                                   'is_agree_terms', 'photo', 'about', 'update_about',]


class LoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=50, min_length=2)
    password = serializers.CharField(max_length=50, min_length=1)

    class Meta:
        model = get_user_model()
        fields = ("phone", "password")

    def validate(self, data):
        phone = data.get("phone")
        password = data.get("password")
        user = self.authenticate_user(phone, password)

        self.validate_user(user)

        data["user"] = user
        data['password'] = password
        return data

    def authenticate_user(self, phone, password):
        user = authenticate(phone=phone, password=password)
        return user

    def validate_user(self, user):
        if not user or not user.is_active:
            raise IncorrectCredentialsError({"error": "Incorrect phone or password"})


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:

            raise AuthenticationFailed('oops, who are you?')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, user_id=user_id, email=email, name=name)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_phone(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

    def save(self):
        email = self.validated_data['email']
        generate_password = generate_random_string()
        user = CustomUser.objects.get(email=email)
        user.set_password(generate_password)
        user.save()
        self.send_verification_email(user, generate_password)

    def send_verification_email(self, user_instance, generate_password):
        email_body = f"Hi {user_instance.first_name} {user_instance.last_name},\nThis is your new generation password: {generate_password} \n Thanks..."
        email_data = {
            "email_body": email_body,
            "to_email": user_instance.email,
            "email_subject": "Reset password",
        }
        Util.send(email_data)

