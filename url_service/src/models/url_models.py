import uuid
from sqlalchemy import Column, String, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from src.db.postgres import Base


class URL(Base):
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String)
    short_url = Column(String, unique=True)
    timestamps = Column(ARRAY(DateTime))
