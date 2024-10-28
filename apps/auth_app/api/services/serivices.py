import uuid

from apps.auth_app.api.adapets import di_container
from apps.auth_app.models import CustomUser
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.db import IntegrityError, transaction

from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import RefreshToken
from utils.data_generation import generator_password
from utils.main import object_get_or_none
import logging
from django.utils.timezone import now

logger = logging.getLogger(__name__)  # Configure your logger accordingly


class TokenService:
    @staticmethod
    def get_token(user: CustomUser) -> dict:
        """Получение токена"""

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def refresh_token(self, token_refresh) -> dict:
        """Обновление токена"""

        valid_data = TokenBackend(
            algorithm=settings.SIMPLE_JWT["ALGORITHM"], signing_key=settings.SIMPLE_JWT["SIGNING_KEY"]
        ).decode(token_refresh, verify=True)

        user_id = valid_data.get("user_id")
        user = CustomUser.objects.get(id=user_id)
        return self.get_token(user)


class UserService:
    @staticmethod
    # FIXME: изменить обращение к create_user (Нужно передать датакласс)
    # Пример:
    def create_user(**kwargs) -> CustomUser:
        """
        Создание пользователя.
        FIXME: изменить обращение к create_user (Нужно через датакласс)
        def create_user(self, user_data: UserDataClass) -> User:
            user = User(email=user_data.email, name=user_data.name)
            user.set_password(user_data.password)
            user.save()
            return user
        """
        if not kwargs.get("email"):
            kwargs["email"] = uuid.uuid4()
        user = CustomUser.objects.create_user(**kwargs)
        return user

    @staticmethod
    def user_exists(email, auth_type=CustomUser.AuthType.LOGIN_PASSWORD_AUTH) -> bool:
        """Проверка существования пользователя по email"""

        return CustomUser.objects.filter(email=email).exists()

    @staticmethod
    def get_user(email) -> CustomUser:
        """Получение пользователя по email"""

        return CustomUser.objects.get(email=email)

    @staticmethod
    def get_user_by_id(user_id) -> CustomUser:
        """Получение пользователя по id"""

        return CustomUser.objects.get(id=user_id)


class AuthService:
    @staticmethod
    @transaction.atomic
    def register_user(**kwargs) -> CustomUser:
        """Регистрация пользователя"""
        user_service = UserService()
        if user_service.user_exists(kwargs.get("email")):
            raise ValueError(CustomUser.Text.USER_WITH_SUCH_EMAIL_ALREADY_EXISTS)
        user = user_service.create_user(**kwargs)
        return user

    @staticmethod
    def authenticate_user(email, password) -> CustomUser:
        """Аутентификация пользователя"""
        user = object_get_or_none(CustomUser, email=email)
        if user and user.check_password(password):
            return user
        raise ValueError(CustomUser.Text.WRONG_PASSWORD_OR_LOGIN_ENTERED)


class OauthService:
    """Сервис для авторизации через социальные сети"""

    auth_service = AuthService()

    def __init__(self, code: str, social_media_type: str):
        self.container = di_container.container
        self.code = code
        self.social_media_type = social_media_type

    def get_social_auth(self) -> (CustomUser, bool):
        """
        Возвращает объект Пользователя и информацию о том, был ли создан новый пользователь
        :return: [User, bool]
        """
        try:
            social_auth_class = self.container.get(self.social_media_type)
            social_auth = social_auth_class(self.code)
            social_user_id, social_user_email = social_auth.auth()

            user = object_get_or_none(CustomUser, social_auth_uid=social_user_id)

            if not social_user_id or not social_user_email:
                raise ValueError("Failed to obtain user information from social provider.")

            if user is None:
                user = self.auth_service.register_user(
                    email=social_user_email,
                    social_auth_uid=social_user_id,
                )
                return user, True  # Assuming you want to return a tuple indicating the user and whether they were newly created
            else:
                return user, False
        except ValueError as err:
            print(f"Error during OAuth process: {err}")
            # Handle the specific error appropriately. You might want to log it or send a more user-friendly message to the frontend.
            raise ValueError(f"OAuth error: {err}")
