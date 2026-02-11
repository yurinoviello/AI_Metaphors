import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from ai_metaphors.server.db.base_class import Base
from ai_metaphors.server.settings.settings import settings

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# VideoTask Status and TermType Enums
# We define them here to avoid importing models which might fail due to missing dependencies
class Status(sa.Enum):
    pass

class TermType(sa.Enum):
    pass

# manually define models metadata
def register_models():
    # VideoTask
    sa.Table(
        'video_task',
        Base.metadata,
        sa.Column('id', sa.String, primary_key=True, index=True),
        sa.Column('status', postgresql.ENUM('queued', 'processing', 'completed', 'failed', name='status', create_type=False), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
        sa.Column('term_name', sa.String, nullable=True),
        sa.Column('term_definition', sa.String, nullable=True),
        sa.Column('metaphor', sa.String, nullable=True),
        sa.Column('term_type', postgresql.ENUM('DEFINITION_METAPHOR', 'CODE_METAPHOR', 'ACADEMIC_DEFINITION', name='termtype', create_type=False), nullable=False),
        sa.Column('use_dataset_example', sa.Integer, default=-1),
        sa.Column('generate_metaphor_text', sa.Boolean, default=True),
        sa.Column('animation_type', sa.String, default="basic"),
        sa.Column('model', sa.String, default="openai-gpt-4o"),
        sa.Column('model_classes', sa.String, default="default"),
        sa.Column('model_manim', sa.String, default="default"),
        sa.Column('temperature', sa.Float, default=0.1),
        sa.Column('vllm_fix', sa.Boolean, default=False),
        sa.Column('high_quality', sa.Boolean, default=False),
        sa.Column('s3_video_url', sa.String, nullable=True),
        sa.Column('user_id', sa.String, nullable=True, index=True),
        sa.Column('api_key', sa.String, nullable=True, index=True),
    )
    
    # User
    sa.Table(
        'users',
        Base.metadata,
        sa.Column('id', sa.String, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, nullable=False, index=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('password_hash', sa.String, nullable=False),
        sa.Column('is_active', sa.Boolean, default=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True)),
    )

register_models()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Set sqlalchemy.url from settings
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://'))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
