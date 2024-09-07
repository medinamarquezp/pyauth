import json
from nicegui import app
from functools import wraps
from fastapi.responses import RedirectResponse
from src.modules.shared.di import verification_token_service


def require_auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        auth = app.storage.user.get('auth')
        if auth:
            try:
                token = auth['session']['token']
                if token and verification_token_service.verify_token(token):
                    return func(*args, **kwargs)
            except json.JSONDecodeError:
                pass

        return RedirectResponse(url='/auth')

    return wrapper


def redirect_if_authenticated(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        auth = app.storage.user.get('auth')
        if auth:
            try:
                token = auth['session']['token']
                if token and verification_token_service.verify_token(token):
                    return RedirectResponse(url='/admin')
            except json.JSONDecodeError:
                pass

        return func(*args, **kwargs)

    return wrapper
