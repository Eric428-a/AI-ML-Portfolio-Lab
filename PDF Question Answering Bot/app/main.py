from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging, get_logger
from app.core.security import SecurityHeadersMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()

    Path(settings.UPLOAD_DIRECTORY).mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(settings.PROCESSED_DIRECTORY).mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(settings.CHROMA_PERSIST_DIRECTORY).mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info(
        "%s starting in %s mode.",
        settings.PROJECT_NAME,
        settings.APP_ENV,
    )

    yield

    logger.info(
        "%s shutting down.",
        settings.PROJECT_NAME,
    )


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SecurityHeadersMiddleware
)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)


@app.get(
    "/health",
    tags=["System"],
)
async def system_health() -> dict[str, str]:
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
    }


@app.get(
    "/",
    tags=["System"],
)
async def root() -> dict[str, str]:
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "docs": "/docs",
    }


frontend_directory = Path("frontend")

if frontend_directory.exists():
    app.mount(
        "/",
        StaticFiles(
            directory=str(frontend_directory),
            html=True,
        ),
        name="frontend",
    )