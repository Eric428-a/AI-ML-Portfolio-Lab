from typing import Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = ""
    data: T | None = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: str | None = None


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    vector_store: str
    embedding_provider: str
    llm_provider: str


class DeleteResponse(BaseModel):
    success: bool = True
    message: str
    deleted_id: str


class Pagination(BaseModel):
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total: int = Field(ge=0)
    pages: int = Field(ge=0)