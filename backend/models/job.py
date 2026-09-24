from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,JSON
from sqlalchemy import func
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime, timezone

class StoryJob(Base):
    __tablename__ = "story_jobs"
    id = Column(String, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True)
    session_id = Column(String, index=True )
    theme = Column(String)
    status = Column(String)
    story_id = Column(String, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True),  default=lambda: datetime.now(timezone.utc))
    compeleted_job = Column(DateTime(timezone=True), nullable = True)
    
    