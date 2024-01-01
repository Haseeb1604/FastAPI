"""Add content column to  post table

Revision ID: 1167e72a76d0
Revises: 0d6554bbb866
Create Date: 2024-01-01 12:22:15.635465

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1167e72a76d0'
down_revision: Union[str, None] = '0d6554bbb866'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
