import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends

from ai_metaphors.server.api.auth import unified_auth
from ai_metaphors.server.models.video_task import VideoTask
from ai_metaphors.server.schemas.video import VideoResponse, VideoRequest, VideoTaskStatus, VideoTaskList, Status
from ai_metaphors.server.services.video_task_processor import VideoTaskProcessor

router = APIRouter(
    dependencies=[Depends(unified_auth)]
)
video_task_processor = VideoTaskProcessor()


@router.post("/video", response_model=VideoResponse)
async def generate_video(
    request: VideoRequest,
    background_tasks: BackgroundTasks,
    auth: dict = Depends(unified_auth)
):
    try:
        task_id = str(uuid4())

        await VideoTask.create_from_video_request(
            request, 
            task_id, 
            user_id=auth.get("user_id"), 
            api_key=auth.get("api_key")
        )

        background_tasks.add_task(
            video_task_processor.process_video_generation_task,
            task_id,
        )

        return VideoResponse(task_id=task_id, status=Status.queued)
    except Exception as e:
        logging.error(f"Unexpected error in generate_video: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/video/tasks/{task_id}", response_model=VideoTaskStatus)
async def get_task_status(task_id: str, auth: dict = Depends(unified_auth)):
    task = await VideoTask.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check ownership
    if auth.get("user_id") and task.user_id != auth.get("user_id"):
        raise HTTPException(status_code=403, detail="Access forbidden")
    if auth.get("api_key") and task.api_key != auth.get("api_key"):
        raise HTTPException(status_code=403, detail="Access forbidden")

    return VideoTaskStatus(
        task_id=task.id,
        status=task.status,
        created_at=task.created_at,
        video_url=task.s3_video_url if task.status == Status.completed else None
    )


@router.get("/video/tasks", response_model=VideoTaskList)
async def get_tasks_list(skip: int = 0, limit: int = 100, auth: dict = Depends(unified_auth)):
    pagination_result = await VideoTask.all(
        skip=skip, 
        limit=limit, 
        user_id=auth.get("user_id"), 
        api_key=auth.get("api_key")
    )

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
