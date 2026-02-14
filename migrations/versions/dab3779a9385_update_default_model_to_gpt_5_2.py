"""update default model to gpt-5-2

Revision ID: dab3779a9385
Revises: b14831acc358
Create Date: 2026-02-14 15:26:34.090405

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dab3779a9385'
down_revision: Union[str, Sequence[str], None] = 'b14831acc358'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('video_task', 'model', server_default='openai-gpt-5-2')


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('video_task', 'model', server_default='openai-gpt-4o')
