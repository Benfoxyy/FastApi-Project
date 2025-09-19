from config.database import Base
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    created_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    user = relationship("UserModel", back_populates="tasks", uselist=False)