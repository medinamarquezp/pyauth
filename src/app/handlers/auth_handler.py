from nicegui import ui
from src.modules.shared.di import auth_service


def handle_signin(email: str, password: str):
    if email and password:
        ui.notify('Iniciando sesión...', color='positive')
        # Aquí iría la lógica de autenticación


def handle_signup(name: str, email: str, password: str):
    if not name or not email or not password:
        ui.notify('Please fill in all fields', color='negative')
        return
    data = {
        'name': name,
        'email': email,
        'password': password
    }
    registered = auth_service.signup(data)
    if not registered:
        ui.notify('Something went wrong', color='negative')
        return
    ui.open('/auth/signin')


def handle_forgot_password(email: str):
    if email:
        ui.notify('Sending reset link...', color='positive')
        # Aquí iría la lógica de autenticación


def handle_reset_password(token: str, password: str):
    if token and password:
        ui.notify('Resetting password...', color='positive')
        # Aquí iría la lógica de autenticación


def handle_oauth_callback(provider: str, url: str):
    data = auth_service.oauth_callback('google', str(url))
    ui.label(str(data))
