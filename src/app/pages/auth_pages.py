from nicegui import ui
from typing import Optional
from fastapi import Request

from src.app.validations import (
    validate_email,
    validate_password,
    validate_min_length
)

from src.app.components import (
    common_styles,
    google_oauth_button,
    card_container,
    create_input,
    card_title,
    card_navigation,
    card_button
)

from src.app.handlers import (
    handle_signin,
    handle_signup,
    handle_status,
    handle_activate,
    handle_forgot_password,
    handle_reset_password,
    handle_oauth_callback
)


def setup_auth_pages():
    @ui.page('/auth')
    def auth():
        ui.open('/auth/signin')

    @ui.page('/auth/signin')
    def login(request: Request):
        common_styles()
        handle_status(request)
        with card_container():
            card_title('Welcome back')
            card_navigation("Don't have an account?",
                            "Sign up", '/auth/signup')
            google_oauth_button()
            ui.label('Or continue with your email')
            email = create_input('Email', validation={
                                 'Invalid email': lambda value: validate_email(value)})
            password = create_input('Password', is_password=True, validation={
                                    'Invalid password': lambda value: validate_min_length(value)})
            card_navigation("Forgot your password?",
                            "Password recovery", '/auth/forgot-password')
            card_button('Sign in', lambda: handle_signin(
                email.value, password.value))

    @ui.page('/auth/signup')
    def signup():
        common_styles()
        with card_container():
            card_title('Sign up')
            card_navigation("Already have an account?",
                            "Sign in", '/auth/signin')
            google_oauth_button()
            ui.label('Or register with your email')
            name = create_input('Name')
            email = create_input('Email', validation={
                                 'Invalid email': lambda value: validate_email(value)})
            password = create_input('Password', is_password=True, validation={
                                    'Invalid password': lambda value: validate_min_length(value) and validate_password(value)})
            card_button('Sign up', lambda: handle_signup(
                name.value, email.value, password.value))

    @ui.page('/auth/forgot-password')
    def forgot_password():
        common_styles()
        with card_container():
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
            return
        common_styles()
        with card_container():
            card_title('Reset password')
            ui.label('Enter your new password')
            password = create_input('Password', is_password=True, validation={
                                    'Invalid password': lambda value: validate_min_length(value) and validate_password(value)})
            create_input('Confirm password', is_password=True, validation={
                'Invalid password': lambda value: validate_min_length(value) and validate_password(value), 'Passwords do not match': lambda value: value == password.value})
            card_button('Reset password', lambda: handle_reset_password(
                str(token), password.value))

    @ui.page('/auth/google/callback')
    def callback(request: Request):
        url = request.url
        handle_oauth_callback('google', str(url))

    @ui.page('/auth/activate')
    def activate(token: Optional[str] = None):
        if not token:
            ui.open('/auth/signin')
            return
        handle_activate(str(token))
