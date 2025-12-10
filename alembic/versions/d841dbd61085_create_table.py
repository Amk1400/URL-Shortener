"""Create urls table

Revision ID: d841dbd61085
Revises:
Create Date: 2025-12-10 22:28:38.867522

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd841dbd61085'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'urls',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, index=True),
        sa.Column('original_url', sa.String, nullable=False),
        sa.Column('short_code', sa.String(10), nullable=False, unique=True, index=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('expired_at', sa.DateTime, nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('urls')
