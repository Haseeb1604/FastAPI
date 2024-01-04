"""remove phone number from user table

Revision ID: 6d7f37c19d8b
Revises: 7dcbf42162ed
Create Date: 2024-01-04 22:14:46.322666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d7f37c19d8b'
down_revision: Union[str, None] = '7dcbf42162ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
