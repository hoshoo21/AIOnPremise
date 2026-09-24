from typing import List,Optional, Dict
from datetime import datetime
from pydantic import BaseModel

class StoryJobBase(BaseModel):
    theme:str

class StoryJobResponse(BaseModel):
    job_id:str 
    status:str
    session_id :str 
    created_at :datetime
    story_id :Optional[str] = None
    completed_at:Optional[datetime] = None
    error: Optional[str] = None
    
    class Config:
        from_attribute = True

class StoryJobCreate(StoryJobBase):
    pass