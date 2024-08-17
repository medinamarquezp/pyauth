from sqlalchemy.orm import Session
from src.modules.auth.models import SessionModel
from src.modules.shared.sql import BaseRepository

class SessionRepository(BaseRepository[SessionModel]):
    def __init__(self, session: Session):
        super().__init__(session, SessionModel)
