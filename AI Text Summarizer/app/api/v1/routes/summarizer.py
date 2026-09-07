from fastapi import APIRouter, HTTPException, status

from app.schemas.summarizer import SummaryRequest, SummaryResponse
from app.services.summarizer import summarizer_service


router = APIRouter()


@router.post(
    "/summarize",
    response_model=SummaryResponse,
    status_code=status.HTTP_200_OK,
)
async def summarize_text(request: SummaryRequest) -> SummaryResponse:
    try:
        return await summarizer_service.summarize(
            text=request.text,
            min_length=request.min_length,
            max_length=request.max_length,
            style=request.style,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate summary.",
        ) from exc


@router.get("/health")
async def summarizer_health():
    return await summarizer_service.health()