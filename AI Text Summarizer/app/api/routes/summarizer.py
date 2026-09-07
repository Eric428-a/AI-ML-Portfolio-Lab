from fastapi import APIRouter, HTTPException, status

from app.schemas.summarizer import (
    SummaryResponse,
    SummaryRequest,
)
from app.services.summarizer import summarizer_service


router = APIRouter(
    prefix="/summarizer",
    tags=["Summarizer"],
)


@router.get("/health")
async def summarizer_health():
    return {
        "service": "summarizer",
        "status": "ready",
    }


@router.post(
    "/summarize",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def summarize_text(request: SummaryRequest):
    try:
        return await summarizer_service.summarize(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length,
            style=request.style,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to summarize the provided text.",
        ) from exc