import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException, BackgroundTasks

from ai_metaphors.server.models.video_task import VideoTask
from ai_metaphors.server.schemas.video import VideoResponse, VideoRequest, VideoTaskStatus, VideoTaskList, Status
from ai_metaphors.server.services.video_task_processor import VideoTaskProcessor

router = APIRouter()
video_task_processor = VideoTaskProcessor()


@router.post("/video", response_model=VideoResponse)
async def generate_video(
    request: VideoRequest,
    background_tasks: BackgroundTasks
):
    try:
        task_id = str(uuid4())

        await VideoTask.create_from_video_request(request, task_id)

        background_tasks.add_task(
            video_task_processor.process_video_generation_task,
            task_id,
        )

        return VideoResponse(task_id=task_id, status=Status.queued)
    except Exception as e:
        logging.error(f"Unexpected error in generate_video: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/video/tasks/{task_id}", response_model=VideoTaskStatus)
async def get_task_status(task_id: str):
    task = await VideoTask.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return VideoTaskStatus(
        task_id=task.id,
        status=task.status,
        created_at=task.created_at,
        video_url=task.s3_video_url if task.status == Status.completed else None
    )


@router.get("/video/tasks", response_model=VideoTaskList)
async def get_tasks_list(skip: int = 0, limit: int = 100):
    pagination_result = await VideoTask.all(skip=skip, limit=limit)

    return VideoTaskList(
        tasks=[
            VideoTaskStatus(
                task_id=task.id,
                status=task.status,
                created_at=task.created_at,
                video_url=task.s3_video_url if task.status == Status.completed else None
            )
            for task in pagination_result["items"]
        ],
        total=pagination_result["total"],
        skip=pagination_result["skip"],
        limit=pagination_result["limit"]
    )
