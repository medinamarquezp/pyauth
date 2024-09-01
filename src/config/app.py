from os import getenv
from dotenv import load_dotenv

ENV = getenv("ENV")

if ENV == "test":
    load_dotenv(".env.test", override=True)
else:
    load_dotenv(".env", override=True)

DATABASE_URL = getenv("DATABASE_URL") or "sqlite:///app.db"

APP = {
    "FRONTEND_URL": getenv("FRONTEND_URL"),
}

EMAIL_SMTP = {
    "SERVER": getenv("EMAIL_SMTP_SERVER"),
    "PORT": getenv("EMAIL_SMTP_PORT"),
    "USERNAME": getenv("EMAIL_SMTP_USERNAME"),
    "PASSWORD": getenv("EMAIL_SMTP_PASSWORD"),
    "FROM": getenv("EMAIL_SMTP_FROM"),
}

OAUTH = {
    "GOOGLE": {
        "CLIENT_ID": getenv("OAUTH_GOOGLE_CLIENT_ID"),
        "CLIENT_SECRET": getenv("OAUTH_GOOGLE_CLIENT_SECRET"),
        "REDIRECT_URI": getenv("OAUTH_GOOGLE_REDIRECT_URI"),
        "TOKEN_URL": "https://accounts.google.com/o/oauth2/token",
        "USER_INFO_URL": "https://www.googleapis.com/oauth2/v3/userinfo",
        "AUTHORIZATION_URL": "https://accounts.google.com/o/oauth2/auth",
        "SCOPE": [
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'openid'
        ],
    }
}
