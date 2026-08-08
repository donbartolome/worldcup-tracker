from fastapi import Depends, FastAPI, HTTPException
from pydantic import AwareDatetime, BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from db import Match, get_db

app = FastAPI()


# Pydantic models describe the shape of request/response data and give
# FastAPI what it needs to validate input and generate the /docs schema.
# MatchBase holds the fields every match has; Fixture and Result each
# inherit from it and add only what's specific to them.
class MatchBase(BaseModel):
    # Lets Fixture/Result be built directly from SQLAlchemy Match objects
    # via .model_validate(), instead of only from dicts.
    model_config = ConfigDict(from_attributes=True)

    id: int
    home_team: str
    away_team: str
    kickoff_time: AwareDatetime


class Fixture(MatchBase):
    pass


class Result(MatchBase):
    home_score: int
    away_score: int


@app.get("/")
def read_root():
    return {"status": "ok"}


# The `-> list[Fixture]` return annotation doubles as FastAPI's response
# model: it validates the output and drives the schema shown in /docs.
# `Depends(get_db)` hands the handler a DB session and closes it after
# the request completes.
@app.get("/fixtures")
def get_fixtures(db: Session = Depends(get_db)) -> list[Fixture]:
    matches = db.scalars(
        select(Match).where(Match.home_score.is_(None))
    ).all()
    return [Fixture.model_validate(m) for m in matches]


@app.get("/fixtures/{fixture_id}")
def get_fixture(fixture_id: int, db: Session = Depends(get_db)) -> Fixture:
    match = db.get(Match, fixture_id)
    if match is None or match.home_score is not None:
        raise HTTPException(status_code=404, detail="Fixture not found")
    return Fixture.model_validate(match)


@app.get("/results")
def get_results(db: Session = Depends(get_db)) -> list[Result]:
    matches = db.scalars(
        select(Match).where(Match.home_score.is_not(None))
    ).all()
    return [Result.model_validate(m) for m in matches]
