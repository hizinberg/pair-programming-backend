from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

'''
Database setup and session management.
'''

DATABASE_URL = "sqlite:///./dev.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_session():
    return SessionLocal()
