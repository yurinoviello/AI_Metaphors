import logging
import datetime
from typing import Optional
from sqlalchemy import Column, String, Enum, DateTime, func, Integer, Boolean, Float, select
from sqlalchemy.exc import SQLAlchemyError

from ai_metaphors.common.core.utils.term_type import TermType
from ai_metaphors.server.schemas.video import VideoRequest, Status
from ai_metaphors.server.settings.settings import settings
from ai_metaphors.server.db.base_class import Base
from ai_metaphors.server.db.session import async_session

class VideoTask(Base):
    __tablename__ = 'video_task'

    id = Column(String, primary_key=True, index=True)
    status = Column(Enum(Status), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    term_name = Column(String, nullable=True)
    term_definition = Column(String, nullable=True)
    metaphor = Column(String, nullable=True)
    term_type = Column(Enum(TermType), nullable=False, default=TermType.DEFINITION_METAPHOR)

    use_dataset_example = Column(Integer, default=-1)

    generate_metaphor_text = Column(Boolean, default=True)
    animation_type = Column(String, default="basic")

    model = Column(String, default="openai-gpt-4o")
    model_classes = Column(String, default="default")
    model_manim = Column(String, default="default")
    temperature = Column(Float, default=0.1)

    vllm_fix = Column(Boolean, default=False)
    high_quality = Column(Boolean, default=False)

    s3_video_url = Column(String, nullable=True)

    @staticmethod
    async def create_from_video_request(request: VideoRequest, task_id: str):
        task_data = {
            "id": task_id,
            "status": Status.queued,
            **request.model_dump(exclude_unset=True)
        }

        await VideoTask.create(**task_data)

    @classmethod
    async def create(cls, **kwargs) -> Optional['VideoTask']:
        try:
            async with async_session() as session:
                task = cls(**kwargs)
                session.add(task)
                await session.commit()
                await session.refresh(task)
                logging.info(f"VideoTask with task_id {kwargs.get('id')} created successfully")
            return task
        except SQLAlchemyError as e:
            logging.error(f"Error creating VideoTask: {e}")
            return None

    @classmethod
    async def get(cls, task_id: str) -> Optional['VideoTask']:
        async with async_session() as session:
            return await session.get(cls, task_id)

    @classmethod
    async def update(cls, task_id: str, **kwargs) -> Optional['VideoTask']:
        async with async_session() as session:
            task = await session.get(cls, task_id)
            if task:
                for key, value in kwargs.items():
                    setattr(task, key, value)
                await session.commit()
                await session.refresh(task)
                logging.info(f"VideoTask with task_id {task_id} updated successfully")
            else:
                logging.error(f"VideoTask with task_id {task_id} not found")
            return task

    @classmethod
    async def all(cls, skip: int = 0, limit: int = 100):
        async with async_session() as session:
            non_expired_threshold = func.now() - datetime.timedelta(hours=settings.URL_EXPIRATION / 3600)
            count_query = select(func.count()).select_from(cls).where(cls.created_at >= non_expired_threshold)
            total_count = await session.execute(count_query)
            total = total_count.scalar()

            # Get paginated results
            query = select(cls).where(cls.created_at >= non_expired_threshold).order_by(cls.created_at.desc()).offset(skip).limit(limit)
            result = await session.execute(query)

            return {
                "items": result.scalars().all(),
                "total": total,
                "skip": skip,
                "limit": limit
            }
