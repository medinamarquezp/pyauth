from nicegui import ui, app
from fastapi import Request
from src.modules.shared.di import auth_service


def handle_status(request: Request):
    if request.query_params.get('pending') == 'true':
        ui.notify('Your account is pending activation', color='positive')
    if request.query_params.get('activated') == 'true':
        ui.notify('Your account has been activated', color='positive')
    if request.query_params.get('activated') == 'false':
        ui.notify('Something went wrong', color='negative')
    if request.query_params.get('reset') == 'true':
        ui.notify('Your password has been reset', color='positive')


def handle_signin(email: str, password: str):
    if not email or not password:
        ui.notify('Invalid email or password', color='negative')
        return
    data = {
        'email': email,
        'password': password
    }
    signed_in = auth_service.signin(data)
    if not signed_in:
        ui.notify('Invalid email or password', color='negative')
        return
    app.storage.user['auth'] = signed_in
    ui.open('/admin')


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
    ui.open('/auth/signin?pending=true')


def handle_activate(token: str):
    if not token:
        ui.open('/auth/signin')
    activated = auth_service.verify_signup(token)
    ui.open(f'/auth/signin?activated={str(activated).lower()}')


def handle_forgot_password(email: str):
    if not email:
        ui.notify('Please enter your email', color='negative')
        return
    forgot_password = auth_service.forgot_password(email)
    if not forgot_password:
        ui.notify('Something went wrong', color='negative')
        return
    ui.notify('Reset link sent to your email', color='positive')


def handle_reset_password(token: str, password: str):
    if not token or not password:
        ui.notify('Something went wrong', color='negative')
        return
    reset_password = auth_service.reset_password(token, password)
    if not reset_password:
        ui.notify('Something went wrong', color='negative')
        return
    ui.open('/auth/signin?reset=true')


def handle_oauth_callback(provider: str, url: str):
    data = auth_service.oauth_callback('google', str(url))
    app.storage.user['auth'] = data
    ui.open('/admin')


def handle_signout():
    token = app.storage.user['auth']['session']['token']
    if not token:
        ui.open('/auth/signin')
    auth_service.signout(token)
    app.storage.user.clear()
    ui.open('/auth/signin')
