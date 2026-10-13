from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CollectionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=2000)


class CollectionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    description: str | None = Field(default=None, max_length=2000)


class CollectionResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    created_at: datetime
    document_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class CollectionListResponse(BaseModel):
    items: list[CollectionResponse]
    total: int