"""db: enforce unique booking per date and time

Revision ID: 90f541639493
Revises: 5b82075df3f6
Create Date: 2026-01-23
"""

from alembic import op

# Revision identifiers, used by Alembic.
revision = "90f541639493"
down_revision = "5b82075df3f6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Prevent double-booking by enforcing uniqueness on (date, time)
    op.create_unique_constraint(
        "uq_bookings_date_time",
        "bookings",
        ["date", "time"],
    )


def downgrade() -> None:
    # Remove the unique constraint
    op.drop_constraint(
        "uq_bookings_date_time",
        "bookings",
        type_="unique",
    )
