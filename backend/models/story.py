from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey,JSON
from sqlalchemy import func
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime, timezone
class Story (Base):
    __tablename__ = "Stories"
    id =Column(String,primary_key=True, index=True)
    title = Column(String, index=True)
    session = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    nodes = relationship("StoryNode", back_populates="story")
        
class StoryNode(Base):
    __tablename__="Story_Nodes"
    id=Column(String, primary_key=True, index=True)
    story_id = Column(Integer,ForeignKey("Stories.id"), index=True)
    content = Column(String)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False) 
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON, default=list)
    story = relationship("Story", back_populates="nodes")
       
