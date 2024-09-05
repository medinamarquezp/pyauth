import os
from nicegui import ui
from src.app.pages import setup_auth_pages, setup_admin_pages

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

if __name__ in {'__main__', '__mp_main__'}:
    setup_auth_pages()
    setup_admin_pages()
    ui.run(storage_secret='secret')
