"""add last few columns to posts table

Revision ID: b8fcd923c26b
Revises: 990a272e1c49
Create Date: 2024-06-26 00:06:22.547896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8fcd923c26b'
down_revision: Union[str, None] = '990a272e1c49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('post', 'published')
    op.drop_column('post', 'created_at')
    pass
