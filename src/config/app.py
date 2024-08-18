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
