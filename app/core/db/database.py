from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import DateTime, Column, func

DATABASE_URL = "postgresql://developer:devpassword@127.0.0.1:5432/developer"
DATABASE_URL_ = "postgresql://developer:devpassword@board_fastapi-postgres-1:5432/developer"
engine = create_engine(DATABASE_URL_)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DateTimeBase:
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
