"""Add few more columns to posts

Revision ID: 211117ed291b
Revises: d474d8ce54ec
Create Date: 2024-01-01 14:16:29.188886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '211117ed291b'
down_revision: Union[str, None] = 'd474d8ce54ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean, server_default="TRUE", nullable=False))
    op.add_column("posts", sa.Column("created_At",
        sa.TIMESTAMP(timezone=True), nullable=False, 
        server_default=sa.text('now()')
        )
    )
    pass


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_At")
    pass
