# One-off check that get_db() works end-to-end: insert, query, clean up.
# Not permanent scaffolding - run with `python3 -m scripts.verify_db` from
# the repo root (db.py isn't a package, so plain script invocation can't
# import it).
from datetime import datetime, timezone

from db import Match, get_db

for session in get_db():
    match = Match(
        home_team="Test A",
        away_team="Test B",
        kickoff_time=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    session.add(match)
    session.commit()

    fetched = session.get(Match, match.id)
    print(f"Fetched: id={fetched.id} {fetched.home_team} vs {fetched.away_team} at {fetched.kickoff_time}")

    session.delete(fetched)
    session.commit()
