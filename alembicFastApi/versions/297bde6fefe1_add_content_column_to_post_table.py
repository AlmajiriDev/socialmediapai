"""add content column to post table

Revision ID: 297bde6fefe1
Revises: 99021c16b5a5
Create Date: 2024-06-25 23:25:42.557073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '297bde6fefe1'
down_revision: Union[str, None] = '99021c16b5a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
