from abc import ABC, abstractmethod


class SocialAuthAbstract(ABC):
    """Abstract class for authorization via social media networks"""

    def __init__(self, code: str, client_id: str, client_secret: str) -> None:
        self.code = code
        self.client_id = client_id
        self.client_secret = client_secret

    @abstractmethod
    def get_access_token(self) -> str:
        """Returns access_token"""
        pass

    @abstractmethod
    def get_user_info(self, access_token: str) -> (int, str):
        """Returns the user_id and email of the user"""
        pass

    def auth(self) -> (int, str):
        """Authenticates the user and returns their ID and email"""
        access_token = self.get_access_token()
        return self.get_user_info(access_token)