from nicegui import ui
from src.modules.shared.di import auth_service


def redirect_to_oauth():
    url = auth_service.oauth_redirect('google')
    ui.open(url)


def common_styles():
    ui.add_head_html(
        '<link href="https://unpkg.com/eva-icons@1.1.3/style/eva-icons.css" rel="stylesheet" />')
    ui.add_body_html('<style>body { background-color: #f0f0f0; }</style>')


def google_oauth_button():
    return ui.button('Continue with Google', on_click=redirect_to_oauth, icon="eva-google").classes('w-full mb-4')


def create_input(label, is_password=False, validation=None):
    return ui.input(label, password=is_password, password_toggle_button=is_password, validation=validation).props('filled').classes('w-full mb-2')


def card_title(title):
    return ui.label(title).classes('text-3xl font-bold text-center -mb-2')


def card_navigation(alternate_action, alternate_text, alternate_link):
    with ui.row().classes('mb-2 inline-flex gap-1'):
        ui.label(alternate_action).classes('text-sm')
        ui.link(alternate_text, alternate_link).classes(
            'text-blue-500 text-sm')


def card_button(text, on_click):
    return ui.button(text, on_click=on_click).classes('w-full mt-4 bg-blue-500 text-white')
