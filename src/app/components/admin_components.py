from nicegui import ui


def navbar():
    with ui.header(elevated=True).classes('bg-blue-500 text-white'):
        with ui.row().classes('w-full'):
            ui.label('Dashboard').classes('text-xl')
            with ui.row().classes('items-center ml-auto'):
                avatar = ui.avatar(icon='person').classes(
                    'cursor-pointer text-4xl')
                with ui.menu() as menu:
                    ui.menu_item('Cerrar sesión', on_click=lambda: ui.notify(
                        'Cerrando sesión...'))
                avatar.on('click', menu.open)
