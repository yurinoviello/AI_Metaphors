import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_metaphors.server.api.endpoints import video, healthz, users
from ai_metaphors.server.settings.settings import settings

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: %(message)s (%(filename)s:%(lineno)d)",
    force=True,
)
logging.getLogger("pytoon").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("moviepy").setLevel(logging.INFO)
logging.getLogger("proglog").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logging.getLogger("httpcore").setLevel(logging.INFO)
logging.getLogger("openai").setLevel(logging.INFO)

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
app.include_router(users.router)
