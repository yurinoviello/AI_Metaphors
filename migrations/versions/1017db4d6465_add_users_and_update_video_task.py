"""Add users and update video_task

Revision ID: 1017db4d6465
Revises: 
Create Date: 2026-02-11 12:06:02.982232

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '1017db4d6465'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Create status enum if not exists
    op.execute("DO $$ BEGIN CREATE TYPE status AS ENUM ('queued', 'processing', 'completed', 'failed'); EXCEPTION WHEN duplicate_object THEN null; END $$;")
    
    # 2. Create termtype enum if not exists
    op.execute("DO $$ BEGIN CREATE TYPE termtype AS ENUM ('DEFINITION_METAPHOR', 'CODE_METAPHOR', 'ACADEMIC_DEFINITION'); EXCEPTION WHEN duplicate_object THEN null; END $$;")

    # 3. Create video_task table if not exists
    op.execute("""
    CREATE TABLE IF NOT EXISTS video_task (
        id VARCHAR PRIMARY KEY,
        status status NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        term_name VARCHAR,
        term_definition VARCHAR,
        metaphor VARCHAR,
        term_type termtype NOT NULL,
        use_dataset_example INTEGER DEFAULT -1,
        generate_metaphor_text BOOLEAN DEFAULT TRUE,
        animation_type VARCHAR DEFAULT 'basic',
        model VARCHAR DEFAULT 'openai-gpt-4o',
        model_classes VARCHAR DEFAULT 'default',
        model_manim VARCHAR DEFAULT 'default',
        temperature FLOAT DEFAULT 0.1,
        vllm_fix BOOLEAN DEFAULT FALSE,
        high_quality BOOLEAN DEFAULT FALSE,
        s3_video_url VARCHAR
    )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_video_task_id ON video_task (id)")

    # 4. Create users table if not exists
    op.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR PRIMARY KEY,
        email VARCHAR UNIQUE NOT NULL,
        name VARCHAR NOT NULL,
        password_hash VARCHAR NOT NULL,
        is_active BOOLEAN DEFAULT TRUE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    )
    """)
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_id ON users (id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_users_email ON users (email)")

    # 5. Add columns to video_task if not exists (for backward compatibility if table existed but without these)
    # user_id
    op.execute("ALTER TABLE video_task ADD COLUMN IF NOT EXISTS user_id VARCHAR")
    op.execute("CREATE INDEX IF NOT EXISTS ix_video_task_user_id ON video_task (user_id)")
    
    # api_key
    op.execute("ALTER TABLE video_task ADD COLUMN IF NOT EXISTS api_key VARCHAR")
    op.execute("CREATE INDEX IF NOT EXISTS ix_video_task_api_key ON video_task (api_key)")


def downgrade() -> None:
    """Downgrade schema."""
    # We generally don't want to drop columns/tables in downgrade if we used IF NOT EXISTS in upgrade,
    # but for completeness:
    op.drop_index('ix_video_task_api_key', table_name='video_task')
    op.drop_column('video_task', 'api_key')
    op.drop_index('ix_video_task_user_id', table_name='video_task')
    op.drop_column('video_task', 'user_id')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')
