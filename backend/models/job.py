from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
from enum import Enum as PythonEnum
from db.database import Base

class JobStatus(PythonEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class StoryJob(Base):
    __tablename__ = "story_jobs"
    __table_args__ = {'extend_existing': True}  
    job_id = Column(String, primary_key=True, index=True)  
    session_id = Column(String, nullable=False)
    theme = Column(String, nullable=False)
    status = Column(SQLEnum(JobStatus), default=JobStatus.PENDING)
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    error = Column(String, nullable=True)
    story_id = Column(Integer, nullable=True)