from datetime import datetime

from uuid import UUID

from pydantic import BaseModel


class URLCashTimestamp(BaseModel):
    id: UUID
    timestamp: datetime
