import os
from collections.abc import Generator
from datetime import datetime

from sqlalchemy import DateTime, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


# One table for both fixtures and results: a fixture is a match whose scores
# aren't known yet, a result is the same match once it's been played.
# Nullable score columns capture that lifecycle without separate tables.
class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    home_team: Mapped[str]
    away_team: Mapped[str]
    kickoff_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    home_score: Mapped[int | None] = mapped_column(default=None)
    away_score: Mapped[int | None] = mapped_column(default=None)


# FastAPI dependency: `Depends(get_db)` gives a handler a session and closes
# it after the request, even if the handler raises. Not wired into any
# endpoint yet.
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(engine)
