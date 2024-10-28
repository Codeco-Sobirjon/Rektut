from base64 import b64encode

import requests
from apps.auth_app.api.adapets import oauth_settings

from apps.auth_app.api.adapets.oauth_interfaces import SocialAuthAbstract
from apps.auth_app.models import CustomUser


class GoogleAuth(SocialAuthAbstract):
    """Authorization via Google"""

    def __init__(self, code: str) -> None:
        super().__init__(code, oauth_settings.GOOGLE_CLIENT_ID, oauth_settings.GOOGLE_CLIENT_SECRET)

    def get_access_token(self) -> str:
        """Obtains the Google OAuth2 access token"""
        proxies = {"http": None, "https": None}
        url = "https://oauth2.googleapis.com/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": self.code,
            "grant_type": "authorization_code",
            "redirect_uri": oauth_settings.REDIRECT_URL,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=data, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            # Log or print the actual error message for better debugging
            error_message = response.json().get('error_description', 'Unknown error')
            raise ValueError(f"Failed to obtain access token: {error_message}")

    def get_user_info(self, access_token: str) -> (str, str):
        """Fetches the user's Google ID and email"""
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            return user_info.get("id"), user_info.get("email")
        else:
            error_message = response.json().get('error_description', 'Unknown error')
            raise ValueError(f"Failed to fetch user info: {error_message}")

