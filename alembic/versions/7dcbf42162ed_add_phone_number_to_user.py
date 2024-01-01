"""Add phone number to user

Revision ID: 7dcbf42162ed
Revises: 748df57a5f67
Create Date: 2024-01-01 14:43:01.435773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7dcbf42162ed'
down_revision: Union[str, None] = '748df57a5f67'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
