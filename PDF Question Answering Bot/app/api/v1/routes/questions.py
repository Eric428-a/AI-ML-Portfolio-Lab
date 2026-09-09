from fastapi import APIRouter, HTTPException, status

from app.schemas.question import (
    QuestionRequest,
    QuestionResponse,
)
from app.services.qa_service import qa_service

router = APIRouter()


@router.post(
    "/ask",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
)
async def ask_question(
    request: QuestionRequest,
) -> QuestionResponse:
    try:
        return qa_service.ask(
            question=request.question,
            document_id=request.document_id,
            top_k=request.top_k,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to answer the question.",
        ) from exc