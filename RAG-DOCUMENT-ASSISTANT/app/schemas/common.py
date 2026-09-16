from datetime import datetime

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    application: str
    version: str
    timestamp: datetime


class MessageResponse(BaseModel):
    message: str