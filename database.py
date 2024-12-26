from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import *
from models import *  # noqa

SQLALCHEMY_ENGINE_OPTIONS = {
    "pool_pre_ping": True,
    "pool_size": 15,
    "max_overflow": 30,
    "pool_timeout": 100,
    "pool_recycle": 110,
}

engine = create_engine(POSTGRESQL_DB_URI, **SQLALCHEMY_ENGINE_OPTIONS)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
