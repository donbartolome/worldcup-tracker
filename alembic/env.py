from logging.config import fileConfig

from alembic import context

from db import Base, engine

# Interpret the config file for Python logging. Without this the CLI is
# completely silent - Alembic's "Running upgrade ..." output goes through
# logging at INFO level, and with no handler configured it's swallowed.
if context.config.config_file_name is not None:
    fileConfig(context.config.config_file_name)

# What --autogenerate diffs the database against.
target_metadata = Base.metadata

# Reuses the engine already defined in db.py rather than reading
# DATABASE_URL or building a second engine here, so there's exactly one
# place that knows how to connect. `prepend_sys_path = .` in alembic.ini is
# what makes `from db import ...` work - run `alembic` from the repo root.
with engine.connect() as connection:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
