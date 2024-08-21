from requests_oauthlib import OAuth2Session

from src.config import OAUTH
from src.modules.shared.services import logger
from src.modules.user.services import UserService
from src.modules.auth.services.session_service import SessionService

class OAuthService: 
    def __init__(
        self,
        user_service: UserService,
        session_service: SessionService
    ):
        self.session_service = session_service
    
    def get_google_oauth_redirect_url(self):
        data = self._prepare_google_oauth_data()
        logger.info(f"Getting Google OAuth redirect URL for client_id: {data['client_id']}")
        google = OAuth2Session(
            client_id=data["client_id"],
            redirect_uri=data["redirect_uri"],
            scope=data["scope"]
        )
        authorization_url, state = google.authorization_url(data["authorization_url"], access_type="offline", prompt="consent")
        logger.info(f"Authorization URL: {authorization_url}")
        logger.info(f"State: {state}")
        return authorization_url

    def process_google_oauth_callback(self, response):
        logger.info(f"Processing Google OAuth callback")
        data = self._prepare_google_oauth_data()
        google = OAuth2Session(
            client_id=data["client_id"],
            redirect_uri=data["redirect_uri"]
        )
        token = google.fetch_token(data["token_url"], client_secret=data["client_secret"], authorization_response=response)
        logger.info(f"Token: {token}")
        user_info = google.get(data["user_info_url"]).json()
        logger.info(f"User info: {user_info}")
        return user_info
    
    def _prepare_google_oauth_data(self):
        return {
            "client_id": OAUTH["GOOGLE"]["CLIENT_ID"],
            "client_secret": OAUTH["GOOGLE"]["CLIENT_SECRET"],
            "redirect_uri": OAUTH["GOOGLE"]["REDIRECT_URI"],
            "scope": ['https://www.googleapis.com/auth/gmail.readonly'],
            "authorization_url": "https://accounts.google.com/o/oauth2/auth",
            "token_url": "https://accounts.google.com/o/oauth2/token",
            "user_info_url": "https://www.googleapis.com/oauth2/v3/userinfo"
        }