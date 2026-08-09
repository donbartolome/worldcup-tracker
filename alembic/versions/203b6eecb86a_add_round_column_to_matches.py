"""add round column to matches

Revision ID: 203b6eecb86a
Revises: 63cd79dc935b
Create Date: 2026-08-09 06:26:49.526659

Adds the knockout-stage column and backfills the 32 existing rows.
Autogenerate produced a straight `add_column(nullable=False)`, which fails
on a table that already has rows (23502: null value in column "round"
violates not-null constraint) - hand-edited into add-nullable -> backfill
-> set-NOT-NULL, the standard pattern for a required column on a live table.

The backfill derives each row's round from its kickoff date, not its id.
The six date windows below are disjoint (verified against the live data
while writing this migration) and match seed.py's own "window: ..."
comments, so this doesn't assume anything about insertion order or id
values that isn't already true of the data itself. It's still a
point-in-time assumption tied to this seed data - see the note in
seed.py/CLAUDE.md; a migration is a historical record of one transformation,
not code that stays in sync with future seed changes.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '203b6eecb86a'
down_revision: Union[str, Sequence[str], None] = '63cd79dc935b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('matches', sa.Column('round', sa.String(), nullable=True))

    # Compare on the UTC date, not the raw timestamptz, so the session's
    # TimeZone setting can't shift a boundary.
    op.execute(sa.text("""
        UPDATE matches SET round = CASE
            WHEN (kickoff_time AT TIME ZONE 'UTC')::date
                 BETWEEN DATE '2026-06-28' AND DATE '2026-07-03' THEN 'R32'
            WHEN (kickoff_time AT TIME ZONE 'UTC')::date
                 BETWEEN DATE '2026-07-04' AND DATE '2026-07-07' THEN 'R16'
            WHEN (kickoff_time AT TIME ZONE 'UTC')::date
                 BETWEEN DATE '2026-07-09' AND DATE '2026-07-12' THEN 'QF'
            WHEN (kickoff_time AT TIME ZONE 'UTC')::date
                 BETWEEN DATE '2026-07-14' AND DATE '2026-07-15' THEN 'SF'
            WHEN (kickoff_time AT TIME ZONE 'UTC')::date = DATE '2026-07-18'
                 THEN '3P'
            WHEN (kickoff_time AT TIME ZONE 'UTC')::date = DATE '2026-07-19'
                 THEN 'F'
        END
    """))

    # Any row the CASE above didn't match is still NULL, and this fails
    # loudly - better a failed migration than one silently mislabelled row.
    op.alter_column('matches', 'round', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('matches', 'round')
