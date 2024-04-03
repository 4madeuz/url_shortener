from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class URL(BaseModel):

    id: UUID
    original_url: str
    short_url: str
    timestamps: list[datetime] | None

    class Config:
        from_attributes = True


class URLCreate(BaseModel):
    original_url: str


class URLCreateFull(BaseModel):
    original_url: str
    short_url: str
    timestamps: list[datetime] = []


class URLCashTimestamp(BaseModel):
    id: UUID
    timestamp: datetime
