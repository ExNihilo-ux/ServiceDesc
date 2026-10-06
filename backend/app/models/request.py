# backend/app/models/request.py
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Request(Base):
    __tablename__ = "requests"
    
    id: Mapped[str] = mapped_column(String(50), primary_key=True)