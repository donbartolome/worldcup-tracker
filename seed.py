"""Seed the matches table with the 2026 World Cup knockout stage.

Destructive: deletes every row in `matches` before reloading, so the table
always exactly matches MATCHES below. Safe to re-run - the id sequence is
reset each time, so re-seeding always reproduces the same ids 1-32.

Round/stage isn't a column on Match, so it's tracked only via the comments
below (see CLAUDE.md).

kickoff_time values are dates only (no confirmed kickoff time), so every
match lands at 00:00 UTC - the date is real, the time isn't.
"""

from datetime import datetime, timezone

from sqlalchemy import delete, text

from db import Match, SessionLocal

MATCHES = [
    # Round of 32 (window: Jun 28 - Jul 3) — only South Africa/Canada date confirmed exact
    {"home_team": "South Africa", "away_team": "Canada", "home_score": 0, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-06-28"},  # exact
    {"home_team": "Germany", "away_team": "Paraguay", "home_score": 1, "away_score": 1,
     "home_penalties": 3, "away_penalties": 4, "kickoff_time": "2026-06-28"},  # approx
    {"home_team": "France", "away_team": "Sweden", "home_score": 3, "away_score": 0,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-06-28"},  # approx
    {"home_team": "Netherlands", "away_team": "Morocco", "home_score": 1, "away_score": 1,
     "home_penalties": 2, "away_penalties": 3, "kickoff_time": "2026-06-29"},  # approx
    {"home_team": "Portugal", "away_team": "Croatia", "home_score": 2, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-06-29"},  # approx
    {"home_team": "Spain", "away_team": "Austria", "home_score": 3, "away_score": 0,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-06-29"},  # approx
    {"home_team": "USA", "away_team": "Bosnia-Herz", "home_score": 2, "away_score": 0,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-06-30"},  # approx, AET
    {"home_team": "Belgium", "away_team": "Senegal", "home_score": 3, "away_score": 2,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-06-30"},  # approx, AET
    {"home_team": "Brazil", "away_team": "Japan", "home_score": 2, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-06-30"},  # approx
    {"home_team": "Ivory Coast", "away_team": "Norway", "home_score": 1, "away_score": 2,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-01"},  # approx
    {"home_team": "Mexico", "away_team": "Ecuador", "home_score": 2, "away_score": 0,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-01"},  # approx
    {"home_team": "England", "away_team": "Congo DR", "home_score": 2, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-01"},  # approx, AET
    {"home_team": "Argentina", "away_team": "Cape Verde", "home_score": 3, "away_score": 2,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-02"},  # approx, AET
    {"home_team": "Australia", "away_team": "Egypt", "home_score": 1, "away_score": 1,
     "home_penalties": 2, "away_penalties": 4, "kickoff_time": "2026-07-02"},  # approx
    {"home_team": "Switzerland", "away_team": "Algeria", "home_score": 2, "away_score": 0,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-03"},  # approx
    {"home_team": "Colombia", "away_team": "Ghana", "home_score": 1, "away_score": 0,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-03"},  # approx

    # Round of 16 (window: Jul 4 - Jul 7) — all approx
    {"home_team": "Paraguay", "away_team": "France", "home_score": 0, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-04"},  # approx
    {"home_team": "Canada", "away_team": "Morocco", "home_score": 0, "away_score": 3,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-04"},  # approx
    {"home_team": "Portugal", "away_team": "Spain", "home_score": 0, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-05"},  # approx
    {"home_team": "USA", "away_team": "Belgium", "home_score": 1, "away_score": 4,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-05"},  # approx
    {"home_team": "Brazil", "away_team": "Norway", "home_score": 1, "away_score": 2,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-06"},  # approx
    {"home_team": "Mexico", "away_team": "England", "home_score": 2, "away_score": 3,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-06"},  # approx
    {"home_team": "Argentina", "away_team": "Egypt", "home_score": 3, "away_score": 2,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-07"},  # approx
    {"home_team": "Switzerland", "away_team": "Colombia", "home_score": 0, "away_score": 0,
     "home_penalties": 4, "away_penalties": 3, "kickoff_time": "2026-07-07"},  # approx

    # Quarterfinals — exact
    {"home_team": "France", "away_team": "Morocco", "home_score": 2, "away_score": 0,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-09"},
    {"home_team": "Spain", "away_team": "Belgium", "home_score": 2, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-10"},
    {"home_team": "Norway", "away_team": "England", "home_score": 1, "away_score": 2,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-11"},  # AET
    {"home_team": "Argentina", "away_team": "Switzerland", "home_score": 3, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-12"},  # AET

    # Semifinals — exact
    {"home_team": "France", "away_team": "Spain", "home_score": 0, "away_score": 2,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-14"},
    {"home_team": "Argentina", "away_team": "England", "home_score": 2, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-15"},

    # 3rd place / Final — exact
    {"home_team": "France", "away_team": "England", "home_score": 4, "away_score": 6,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-18"},
    {"home_team": "Argentina", "away_team": "Spain", "home_score": 0, "away_score": 1,
     "home_penalties": None, "away_penalties": None, "kickoff_time": "2026-07-19"},  # AET
]

assert len(MATCHES) == 32, f"expected 32 matches, got {len(MATCHES)}"


def seed():
    with SessionLocal() as session:
        session.execute(delete(Match))
        session.execute(text("ALTER SEQUENCE matches_id_seq RESTART WITH 1"))
        session.add_all(
            Match(
                **{k: v for k, v in row.items() if k != "kickoff_time"},
                kickoff_time=datetime.fromisoformat(row["kickoff_time"]).replace(
                    tzinfo=timezone.utc
                ),
            )
            for row in MATCHES
        )
        session.commit()
    print(f"{len(MATCHES)} rows written")


if __name__ == "__main__":
    seed()
