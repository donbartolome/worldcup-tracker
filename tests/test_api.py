from datetime import datetime, timezone

from db import Match

KICKOFF_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_fixtures_filter_by_round(client, db_session):
    r32_match = Match(
        home_team="Round Test A",
        away_team="Round Test B",
        round="R32",
        kickoff_time=KICKOFF_TIME,
    )
    sf_match = Match(
        home_team="Round Test C",
        away_team="Round Test D",
        round="SF",
        kickoff_time=KICKOFF_TIME,
    )
    db_session.add_all([r32_match, sf_match])
    db_session.commit()

    try:
        response = client.get("/fixtures", params={"round": "R32"})
        assert response.status_code == 200
        matches = response.json()
        teams = [(m["home_team"], m["away_team"]) for m in matches]
        assert ("Round Test A", "Round Test B") in teams
        assert ("Round Test C", "Round Test D") not in teams
        for m in matches:
            assert m["round"] == "R32"
    finally:
        db_session.delete(r32_match)
        db_session.delete(sf_match)
        db_session.commit()


def test_results_filter_by_round(client, db_session):
    r32_match = Match(
        home_team="Round Test A",
        away_team="Round Test B",
        round="R32",
        kickoff_time=KICKOFF_TIME,
        home_score=1,
        away_score=0,
    )
    sf_match = Match(
        home_team="Round Test C",
        away_team="Round Test D",
        round="SF",
        kickoff_time=KICKOFF_TIME,
        home_score=2,
        away_score=2,
    )
    db_session.add_all([r32_match, sf_match])
    db_session.commit()

    try:
        response = client.get("/results", params={"round": "R32"})
        assert response.status_code == 200
        matches = response.json()
        teams = [(m["home_team"], m["away_team"]) for m in matches]
        assert ("Round Test A", "Round Test B") in teams
        assert ("Round Test C", "Round Test D") not in teams
        for m in matches:
            assert m["round"] == "R32"
    finally:
        db_session.delete(r32_match)
        db_session.delete(sf_match)
        db_session.commit()


def test_fixtures_without_round_returns_all_rounds(client, db_session):
    r32_match = Match(
        home_team="Round Test A",
        away_team="Round Test B",
        round="R32",
        kickoff_time=KICKOFF_TIME,
    )
    sf_match = Match(
        home_team="Round Test C",
        away_team="Round Test D",
        round="SF",
        kickoff_time=KICKOFF_TIME,
    )
    db_session.add_all([r32_match, sf_match])
    db_session.commit()

    try:
        response = client.get("/fixtures")
        assert response.status_code == 200
        teams = [(m["home_team"], m["away_team"]) for m in response.json()]
        assert ("Round Test A", "Round Test B") in teams
        assert ("Round Test C", "Round Test D") in teams
    finally:
        db_session.delete(r32_match)
        db_session.delete(sf_match)
        db_session.commit()


def test_unknown_round_returns_empty(client):
    fixtures_response = client.get("/fixtures", params={"round": "NOPE"})
    assert fixtures_response.status_code == 200
    assert fixtures_response.json() == []

    results_response = client.get("/results", params={"round": "NOPE"})
    assert results_response.status_code == 200
    assert results_response.json() == []
