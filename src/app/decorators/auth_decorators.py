import json
from fastapi import Request
from functools import wraps
from fastapi.responses import RedirectResponse
from src.modules.shared.di import verification_token_service


def require_auth(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth_cookie = request.cookies.get('auth')
        if auth_cookie:
            try:
                auth_data = json.loads(auth_cookie)
                token = auth_data.get('token')
                if token and verification_token_service.verify_token(token):
                    return await func(request, *args, **kwargs)
            except json.JSONDecodeError:
                pass

        return RedirectResponse(url='/auth')

    return wrapper


def redirect_if_authenticated(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        auth_cookie = request.cookies.get('auth')
        if auth_cookie:
            try:
                auth_data = json.loads(auth_cookie)
                token = auth_data.get('token')
                if token and verification_token_service.verify_token(token):
                    return RedirectResponse(url='/admin')
            except json.JSONDecodeError:
                pass

        return await func(request, *args, **kwargs)

    return wrapper
