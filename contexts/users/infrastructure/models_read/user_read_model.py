from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from shared.infrastructure.db.base import Base

class UserReadModel(Base):
    __tablename__ = "users_read"

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
