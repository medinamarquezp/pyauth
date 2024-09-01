import os
from nicegui import ui
from typing import Optional
from fastapi import Request
from src.modules.shared.di import auth_service

from src.app.validations.auth_validations import (
    validate_email,
    validate_password
)
from src.app.components.auth_components import (
    common_styles,
    google_oauth_button,
    create_input,
    card_title,
    card_navigation,
    card_button
)

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def handle_signin(email: str, password: str):
    if email and password:
        ui.notify('Iniciando sesión...', color='positive')
        # Aquí iría la lógica de autenticación


def handle_signup(name: str, email: str, password: str):
    if name and email and password:
        ui.notify('Registrando...', color='positive')
        # Aquí iría la lógica de autenticación


def handle_forgot_password(email: str):
    if email:
        ui.notify('Sending reset link...', color='positive')
        # Aquí iría la lógica de autenticación


def handle_reset_password(token: str, password: str):
    if token and password:
        ui.notify('Resetting password...', color='positive')
        # Aquí iría la lógica de autenticación


@ui.page('/auth')
def auth():
    ui.open('/auth/signin')


@ui.page('/auth/signin')
def login():
    common_styles()
    with ui.card().classes('w-full max-w-lg mx-auto mt-10 p-12'):
        card_title('Welcome back')
        card_navigation("Don't have an account?", "Sign up", '/auth/signup')
        google_oauth_button()
        ui.label('Or continue with your email')
        email = create_input('Email', validation={
                             'Invalid email': lambda value: validate_email(value)})
        password = create_input('Password', is_password=True, validation={
                                'Invalid password': lambda value: validate_password(value)})
        card_navigation("Forgot your password?",
                        "Password recovery", '/auth/forgot-password')
        card_button('Sign in', lambda: handle_signin(
            email.value, password.value))


@ui.page('/auth/signup')
def signup():
    common_styles()
    with ui.card().classes('w-full max-w-lg mx-auto mt-10 p-12'):
        card_title('Sign up')
        card_navigation("Already have an account?", "Sign in", '/auth/signin')
        google_oauth_button()
        ui.label('Or register with your email')
        name = create_input('Name')
        email = create_input('Email', validation={
                             'Invalid email': lambda value: validate_email(value)})
        password = create_input('Password', is_password=True, validation={
                                'Invalid password': lambda value: validate_password(value)})
        card_button('Sign up', lambda: handle_signup(
            name.value, email.value, password.value))


@ui.page('/auth/forgot-password')
def forgot_password():
    common_styles()
    with ui.card().classes('w-full max-w-lg mx-auto mt-10 p-12'):
        card_title('Password recovery')
        card_navigation("Back to", "sign in", '/auth/signin')
        ui.label('Enter your email to reset your password')
        email = create_input('Email', validation={
                             'Invalid email': lambda value: validate_email(value)})
        card_button('Reset password', lambda: handle_forgot_password(
            email.value))


@ui.page('/auth/reset-password')
def reset_password(token: Optional[str] = None):
    if not token:
        ui.open('/auth/forgot-password')
    common_styles()
    with ui.card().classes('w-full max-w-lg mx-auto mt-10 p-12'):
        card_title('Reset password')
        ui.label('Enter your new password')
        password = create_input('Password', is_password=True, validation={
                                'Invalid password': lambda value: validate_password(value)})
        create_input('Confirm password', is_password=True, validation={
            'Invalid password': lambda value: validate_password(value), 'Passwords do not match': lambda value: value == password.value})
        card_button('Reset password', lambda: handle_reset_password(
            str(token), password.value))


@ui.page('/auth/google/callback')
def callback(request: Request):
    url = request.url
    data = auth_service.oauth_callback('google', str(url))
    ui.label(str(data))


if __name__ in {'__main__', '__mp_main__'}:
    ui.run(storage_secret='secret')
