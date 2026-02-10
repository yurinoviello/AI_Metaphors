import logging
import uuid
from typing import Optional
from sqlalchemy import Column, String, DateTime, func, Boolean, select
from sqlalchemy.exc import SQLAlchemyError

from ai_metaphors.server.db.base_class import Base
from ai_metaphors.server.db.session import async_session


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    @classmethod
    async def create(cls, **kwargs) -> Optional['User']:
        try:
            # Generate UUID if not provided
            if 'id' not in kwargs or kwargs['id'] is None:
                kwargs['id'] = str(uuid.uuid4())
            async with async_session() as session:
                user = cls(**kwargs)
                session.add(user)
                await session.commit()
                await session.refresh(user)
                logging.info(f"User with id {kwargs.get('id')} created successfully")
            return user
        except SQLAlchemyError as e:
            logging.error(f"Error creating User:\n{e}")
            return None

    @classmethod
    async def get(cls, user_id: str) -> Optional['User']:
        async with async_session() as session:
            return await session.get(cls, user_id)

    @classmethod
    async def get_by_email(cls, email: str) -> Optional['User']:
        async with async_session() as session:
            result = await session.execute(select(cls).where(cls.email == email))
            return result.scalars().first()
