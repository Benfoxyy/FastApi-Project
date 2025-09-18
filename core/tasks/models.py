from config.database import Base
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, func

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)