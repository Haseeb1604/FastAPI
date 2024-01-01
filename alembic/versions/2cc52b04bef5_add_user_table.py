"""add user table

Revision ID: 2cc52b04bef5
Revises: 1167e72a76d0
Create Date: 2024-01-01 12:43:28.272427

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cc52b04bef5'
down_revision: Union[str, None] = '1167e72a76d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "created_At", 
            sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
        )
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
