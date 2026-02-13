import logging
from uuid import uuid4
from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends

from ai_metaphors.server.api.auth import unified_auth, get_current_user
from ai_metaphors.server.models.user import User
from ai_metaphors.server.models.video_task import VideoTask
from ai_metaphors.server.models.status import Status
from ai_metaphors.server.schemas.video import VideoResponse, VideoRequest, VideoTaskStatus, VideoTaskList
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
            user_id=auth.get("user_id")
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
async def get_task_status(
    task_id: str, 
    auth: dict = Depends(unified_auth),
    current_user: User | None = Depends(get_current_user)
):
    result = await VideoTask.get_with_user(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task, user_name = result
    
    # Check ownership: 
    # - If API Key is used (auth.api_key is set), it's an admin, access allowed.
    # - If it's a JWT user, check if they are the owner OR an admin.
    is_admin = auth.get("api_key") is not None or (current_user and current_user.is_admin)
    
    if not is_admin and task.user_id != auth.get("user_id"):
        raise HTTPException(status_code=403, detail="Access forbidden")

    return VideoTaskStatus.from_orm_model(task, user_name=user_name)


@router.get("/video/tasks", response_model=VideoTaskList)
async def get_tasks_list(
    skip: int = 0, 
    limit: int = 100, 
    auth: dict = Depends(unified_auth),
    current_user: User | None = Depends(get_current_user)
):
    # Admins see everything
    is_admin = auth.get("api_key") is not None or (current_user and current_user.is_admin)
    user_id_filter = None if is_admin else auth.get("user_id")

    pagination_result = await VideoTask.all_with_users(
        skip=skip, 
        limit=limit, 
        user_id=user_id_filter
    )

    return VideoTaskList(
        tasks=[
            VideoTaskStatus.from_orm_model(task, user_name=user_name)
            for task, user_name in pagination_result["items"]
        ],
        total=pagination_result["total"],
        skip=pagination_result["skip"],
        limit=pagination_result["limit"]
    )
