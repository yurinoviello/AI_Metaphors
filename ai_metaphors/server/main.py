import logging
from fastapi import FastAPI

from ai_metaphors.server.api.endpoints import video, healthz
from ai_metaphors.server.settings.settings import settings
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
    force=True,
)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(healthz.router)
app.include_router(video.router)
