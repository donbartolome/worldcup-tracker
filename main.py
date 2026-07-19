from datetime import datetime, timezone

from fastapi import FastAPI
from pydantic import AwareDatetime, BaseModel

app = FastAPI()


# Pydantic models describe the shape of request/response data and give
# FastAPI what it needs to validate input and generate the /docs schema.
# MatchBase holds the fields every match has; Fixture and Result each
# inherit from it and add only what's specific to them.
class MatchBase(BaseModel):
    id: int
    home_team: str
    away_team: str
    kickoff_time: AwareDatetime


class Fixture(MatchBase):
    pass


class Result(MatchBase):
    home_score: int
    away_score: int


FIXTURES = [
    Fixture(
        id=1,
        home_team="Team A",
        away_team="Team B",
        kickoff_time=datetime(2026, 7, 25, 18, 0, tzinfo=timezone.utc),
    ),
    Fixture(
        id=2,
        home_team="Team C",
        away_team="Team D",
        kickoff_time=datetime(2026, 7, 26, 21, 0, tzinfo=timezone.utc),
    ),
]

RESULTS = [
    Result(
        id=101,
        home_team="Team E",
        away_team="Team F",
        kickoff_time=datetime(2026, 6, 10, 18, 0, tzinfo=timezone.utc),
        home_score=2,
        away_score=1,
    ),
    Result(
        id=102,
        home_team="Team G",
        away_team="Team H",
        kickoff_time=datetime(2026, 6, 11, 15, 0, tzinfo=timezone.utc),
        home_score=0,
        away_score=0,
    ),
]


@app.get("/")
def read_root():
    return {"status": "ok"}


# The `-> list[Fixture]` return annotation doubles as FastAPI's response
# model: it validates the output and drives the schema shown in /docs.
@app.get("/fixtures")
def get_fixtures() -> list[Fixture]:
    return FIXTURES


@app.get("/results")
def get_results() -> list[Result]:
    return RESULTS
