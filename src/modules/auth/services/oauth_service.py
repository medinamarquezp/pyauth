from requests_oauthlib import OAuth2Session

from src.config import OAUTH
from src.modules.shared.services import logger


class OAuthService:
    def get_redirect_url(self, provider: str):
        if provider == "google":
            return self._get_google_oauth_redirect_url()
        else:
            raise ValueError(f"Provider {provider} not supported")

    def process_callback(self, provider: str, callback: str):
        if provider == "google":
            return self._process_google_oauth_callback(callback)
        else:
            raise ValueError(f"Provider {provider} not supported")

    def _get_google_oauth_redirect_url(self):
        google = self._get_google_oauth_session()
        authorization_url, _ = google.authorization_url(
            OAUTH["GOOGLE"]["AUTHORIZATION_URL"], access_type="offline", prompt="select_account")
        return authorization_url

    def _process_google_oauth_callback(self, callback: str):
        logger.info(f"Processing Google OAuth callback")
        google = self._get_google_oauth_session()
        google.fetch_token(
            OAUTH["GOOGLE"]["TOKEN_URL"], client_secret=OAUTH["GOOGLE"]["CLIENT_SECRET"], authorization_response=callback)
        google_user_data = google.get(OAUTH["GOOGLE"]["USER_INFO_URL"]).json()
        user_data = {
            "email": google_user_data["email"],
            "name": google_user_data["given_name"],
            "last_name": google_user_data["family_name"],
        }
        logger.info(f"User info: {user_data}")
        return user_data

    def _get_google_oauth_session(self):
        return OAuth2Session(
            client_id=OAUTH["GOOGLE"]["CLIENT_ID"],
            redirect_uri=OAUTH["GOOGLE"]["REDIRECT_URI"],
            scope=OAUTH["GOOGLE"]["SCOPE"]
        )
