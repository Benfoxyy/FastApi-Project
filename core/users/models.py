from config.database import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):
    __tablename__="users"
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String(50), nullable=False, unique=True, index=True)
    password = Column(String(250    ), nullable=False)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("TaskModel", back_populates="user")

    def set_password(self, plain_password: str) -> None:
        self.password = pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)