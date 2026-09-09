from fastapi import APIRouter

from app.api.v1.routes.documents import router as documents_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.questions import router as questions_router

api_router = APIRouter()

api_router.include_router(
    documents_router,
    prefix="/documents",
    tags=["Documents"],
)

api_router.include_router(
    questions_router,
    prefix="/questions",
    tags=["Questions"],
)

api_router.include_router(
    health_router,
    tags=["Health"],
)