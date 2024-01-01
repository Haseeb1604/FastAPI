"""Create Post Table

Revision ID: 0d6554bbb866
Revises: 
Create Date: 2024-01-01 12:02:22.198198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d6554bbb866'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
