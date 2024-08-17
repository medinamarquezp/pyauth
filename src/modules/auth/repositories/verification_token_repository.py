from sqlalchemy.orm import Session
from src.modules.shared.sql import BaseRepository
from src.modules.auth.models import VerificationTokenModel

class VerificationTokenRepository(BaseRepository[VerificationTokenModel]):
    def __init__(self, session: Session):
        super().__init__(session, VerificationTokenModel)
