import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session
import asyncio
from db.database import get_db, SessionLocal

from models.story import Story, StoryNode

from models.job import StoryJob
from schemas.story import CompleteStoryResponse,CompleteStoryNodeResponse, CreateStoryRequest
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator

router = APIRouter(prefix="/stories", tags=["stories"])

def get_session_id(session_id:Optional[str]= Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(request:CreateStoryRequest, 
                 background_tasks:BackgroundTasks,
                 response:Response,
                 session_id = Depends(get_session_id),
                 db:Session= Depends(get_db)):
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    
    job_id = str(uuid.uuid4())
    job =StoryJob(
        id=  str(uuid.uuid4()),
        job_id = job_id,
        session_id = session_id,
        
        theme = request.theme,
        status = "Pedning"
    )
    
    print (job_id)
    db.add(job)
    db.commit()
    background_tasks.add_task(generate_story_task, job_id= job_id, theme=request.theme, session_id = session_id)
    return job 

def generate_story_task(job_id:str,  theme:str, session_id:str):
    
    db = SessionLocal()
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        if not job:
            return 
        try :
            job.status ="processing"
            db.commit()
            
            story_db = asyncio.run(
                StoryGenerator.generate_story(db, session_id=session_id, theme=theme)
            )
            job.story_id = story_db.id
            job.status = "completed"
            job.completed_at =datetime.now()
            db.commit()
        except Exception as ex:
            import traceback
            traceback.print_exc()  # add this — prints full stack trace to terminal
            job.status = "failed"
            job.story_id = 1
            job.status = "failed"
            job.completed_at =datetime.now()
            job.error =str(ex)
            db.commit()
    finally:
        db.close()            


@router.get("/{session}/complete", response_model=CompleteStoryResponse)
def get_complete_story(session:str, db:Session=Depends(get_db) ):
    print(session)
    story = db.query(Story).filter(Story.session == session).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story Not found")
    complete_story = build_complete_story_tree(db, story=story)
    return complete_story    

def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    print (story.id)
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()
    print (len(nodes))
    node_dict = {}
    for node in nodes:
        if node.is_root:
            print ("node is root")
        node_response = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            is_ending=node.is_ending,
            is_winning_ending=node.is_winning_ending,
            options=node.options,
            is_root = node.is_root
        )
        node_dict[node.id] = node_response

    root_node = next((node for node in nodes if node.is_root), None)
    if not root_node:
        print("story root not found")
        raise HTTPException(status_code=500, detail="Story root node not found")

    return CompleteStoryResponse(
        id=story.id,
        title= story.title,
        session=story.session,
        created_at=story.created_at,
        root_node=node_dict[root_node.id],
        all_nodes=node_dict
    )