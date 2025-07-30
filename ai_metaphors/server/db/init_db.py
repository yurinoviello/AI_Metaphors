import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text

from ai_metaphors.server.db.base_class import Base
from ai_metaphors.server.db.session import engine

from ai_metaphors.server.models.video_task import VideoTask

async def create_tables(engine: AsyncEngine):
    """Create all tables in the database."""
    try:
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        raise


async def check_db_connection(engine: AsyncEngine):
    """Check if the database connection is working."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logging.info("Database connection successful")
        return True
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        return False


async def init_db():
    """Initialize the database."""
    if await check_db_connection(engine):
        await create_tables(engine)
    else:
        logging.error("Failed to initialize database due to connection issues")


if __name__ == "__main__":
    # This allows running the script directly
    logging.basicConfig(level=logging.INFO)
    asyncio.run(init_db())