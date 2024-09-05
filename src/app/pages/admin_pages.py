from nicegui import ui

from src.app.components import navbar


def setup_admin_pages():
    @ui.page('/admin')
    def admin():
        ui.open('/admin/dashboard')

    @ui.page('/admin/dashboard')
    def dashboard():
        navbar()
        with ui.column().classes('w-full h-full flex items-center justify-center my-10'):
            ui.label('Welcome to the admin dashboard').classes(
                'text-3xl font-bold')
