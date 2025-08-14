import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.job import StoryJob, JobStatus 
from models.story import Story, StoryNode  
from schemas.story import CompleteStoryResponse, CreateStoryRequest, CompleteStoryNodeResponse  # Added CompleteStoryNodeResponse
from schemas.job import StoryJobResponse
from core.story_generator import StoryGenerator

router = APIRouter(prefix="/stories", tags=["stories"])


def get_session_id(session_id: Optional[str] = Cookie(None)):
    return session_id or str(uuid.uuid4())


@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db)
):
    # Set session cookie
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    # Create job in DB
    job = StoryJob(
        job_id=job_id,
        session_id=session_id,
        theme=request.theme,
        status=JobStatus.PENDING,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Run background task
    background_tasks.add_task(
        generate_story_tasks,
        job_id=job_id,
        theme=request.theme,
        session_id=session_id
    )

    return job


def generate_story_tasks(job_id: str, theme: str, session_id: str):
    db = SessionLocal()  # New session for background task
    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()
        if not job:
            return

        try:
            job.status = JobStatus.PROCESSING
            db.commit()

            # Generate story
            story = StoryGenerator.generate_story(db, session_id, theme)

            job.story_id = story.id
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now()
            db.commit()

        except Exception as e:
            db.rollback()
            job.status = JobStatus.FAILED
            job.completed_at = datetime.now()
            job.error = f"{type(e).__name__}: {str(e)}"  # Clear error message
            db.commit()

    except Exception as outer_e:
        print(f"Unexpected error in background task: {outer_e}")
    finally:
        db.close()  # Always close session


@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")

    # Build and return the full response
    return build_complete_story_tree(db, story)


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    # Fetch all nodes for this story
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    # Build all_nodes: dict of {node_id: CompleteStoryNodeResponse}
    all_nodes = {}
    for node in nodes:
        # Convert DB node to Pydantic schema
        node_response = CompleteStoryNodeResponse.model_validate(node)
        all_nodes[node.id] = node_response

    # Build root_nodes: list of root nodes
    root_nodes = [all_nodes[node.id] for node in nodes if node.is_root]
    if not root_nodes:
        raise HTTPException(status_code=500, detail="Story root node not found")

    # Construct and return the complete response
    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        session_id=story.session_id,
        created_at=story.created_at,
        root_nodes=root_nodes,  
        all_nodes=all_nodes     
    )