from fastapi import APIRouter

from app.core.config import settings
from app.schemas.response import HealthResponse
from app.services.llm_service import llm_service
from app.services.vector_store import vector_store

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health() -> HealthResponse:
    llm_health = await llm_service.health()

    return HealthResponse(
        status="healthy",
        service=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.APP_ENV,
        vector_store=(
            f"{settings.VECTOR_STORE}:"
            f"{vector_store.count()} vectors"
        ),
        embedding_provider=settings.EMBEDDING_PROVIDER,
        llm_provider=(
            f"{settings.LLM_PROVIDER}:"
            f"{'configured' if llm_health['configured'] else 'not-configured'}"
        ),
    )