from datetime import datetime, timezone

from db import Match

KICKOFF_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_insert_and_query_match(db_session):
    match = Match(
        home_team="Test A",
        away_team="Test B",
        kickoff_time=KICKOFF_TIME,
    )
    db_session.add(match)
    db_session.commit()

    try:
        fetched = db_session.get(Match, match.id)
        assert fetched is not None
        assert fetched.home_team == "Test A"
        assert fetched.away_team == "Test B"
        assert fetched.kickoff_time == KICKOFF_TIME
        assert fetched.home_penalties is None
        assert fetched.away_penalties is None
    finally:
        db_session.delete(match)
        db_session.commit()


def test_insert_penalty_decided_match(db_session):
    match = Match(
        home_team="Test A",
        away_team="Test B",
        kickoff_time=KICKOFF_TIME,
        home_score=1,
        away_score=1,
        home_penalties=4,
        away_penalties=3,
    )
    db_session.add(match)
    db_session.commit()

    try:
        fetched = db_session.get(Match, match.id)
        assert fetched is not None
        assert fetched.home_score == 1
        assert fetched.away_score == 1
        assert fetched.home_penalties == 4
        assert fetched.away_penalties == 3
    finally:
        db_session.delete(match)
        db_session.commit()
