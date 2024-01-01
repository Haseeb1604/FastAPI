"""Add Foreign key to post table

Revision ID: d474d8ce54ec
Revises: 2cc52b04bef5
Create Date: 2024-01-01 13:40:59.126904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd474d8ce54ec'
down_revision: Union[str, None] = '2cc52b04bef5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk", 
        source_table="posts", referent_table="users", 
        local_cols=["owner_id"], remote_cols=["id"], 
        ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
