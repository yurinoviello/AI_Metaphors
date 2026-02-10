import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text

from ai_metaphors.server.db.base_class import Base
from ai_metaphors.server.db.session import engine
# Import models here to register them with SQLAlchemy Base.metadata.
# IMPORTANT: Do not remove these imports, otherwise the tables will not be created.
# noinspection PyUnusedImports
from ai_metaphors.server.models.video_task import VideoTask


async def create_tables(engine: AsyncEngine):
    """Create all tables in the database."""
    try:
        # Create tables
        async with engine.begin() as conn:
            logging.info(f"Registered tables in metadata: {list(Base.metadata.tables.keys())}")
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error creating database tables: {e}")
        raise


async def check_db_connection(engine: AsyncEngine, retries: int = 5, delay: int = 2):
    """Check if the database connection is working with retries."""
    for i in range(retries):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            logging.info("Database connection successful")
            return True
        except Exception as e:
            logging.warning(f"Database connection attempt {i+1}/{retries} failed: {e}")
            if i < retries - 1:
                await asyncio.sleep(delay)
    
    logging.error("Database connection failed after all retries")
    return False


async def init_db():
    """Initialize the database."""
    if await check_db_connection(engine):
        await create_tables(engine)
    else:
        logging.error("Failed to initialize database due to connection issues")


if __name__ == "__main__":
    # This allows running the script directly
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    asyncio.run(init_db())