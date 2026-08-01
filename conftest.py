import pytest

from db import Base, engine, get_db


@pytest.fixture(scope="session", autouse=True)
def _create_tables():
    Base.metadata.create_all(engine)


# `yield from` delegates into get_db(): forwards its single yielded session
# through to the test, then resumes it (running the `finally: db.close()`)
# once the test finishes - same lifecycle FastAPI's Depends() drives.
@pytest.fixture
def db_session():
    yield from get_db()
