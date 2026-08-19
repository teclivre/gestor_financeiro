from app.db.base import Base
from app.db.session import engine
from app.models.user import User
from app.models.categoria import Categoria
from app.models.transacao import Transacao


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
