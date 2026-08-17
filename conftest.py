import pytest
from fastapi.testclient import TestClient

from db import Base, engine, get_db
from main import app


@pytest.fixture(scope="session")
def _create_tables():
    Base.metadata.create_all(engine)


# `yield from` delegates into get_db(): forwards its single yielded session
# through to the test, then resumes it (running the `finally: db.close()`)
# once the test finishes - same lifecycle FastAPI's Depends() drives.
@pytest.fixture
def db_session(_create_tables):
    yield from get_db()


# Drives the real app in-process. dependency_overrides swaps FastAPI's
# get_db for the test's db_session, so requests hit the same session -
# and the same real Postgres - that the test inserts into. Overriding
# with a plain lambda (not a generator) is deliberate: FastAPI won't
# close a session it didn't open, leaving db_session's own lifecycle
# in charge.
@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
