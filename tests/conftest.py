import os
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from src.config.app import DATABASE_URL

@pytest.fixture(scope='session', autouse=True)
def initialize_database():
    DATABASE_NAME = DATABASE_URL.split('sqlite:///')[-1]
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), DATABASE_NAME)
    
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
    
    create_engine(DATABASE_URL)
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    
    yield
    
    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)