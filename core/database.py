from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./sqlite.db'
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# for postgres or other relational databases
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30))
    description = Column(Text)
    is_done = Column(Boolean, default=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()