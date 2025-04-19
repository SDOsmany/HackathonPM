from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import Dict, Any, List

from src.utils.openai import OpenAIClient

load_dotenv()

# Get origins from environment variable, default to empty list if not set
origins = os.getenv("HOST_URL", "").split(",") if os.getenv("HOST_URL") else []

# add the cors origin to the server
app = FastAPI(
    title="RAG API",
    description="API for RAG",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class IdeaRequest(BaseModel):
    idea: dict

class Idea(BaseModel):
    id: int
    title: str
    summary: str
    description: str
    sources: List[str]




@router.post("/rag")
async def rag_query(
    request: QueryRequest,
) -> Dict[str, Any]:
    """Endpoint for querying the RAG agent about hackathon projects."""
    # response = await rag_agent.process({"query": request.query})
    return {
        "ideas": [
            Idea(
                id=1,
                title="Idea 1",
                summary="Sample summary",
                description="Description 1",
                sources=["https://www.google.com"]
            ),
            Idea(
                id=2,
                title="Idea 2",
                summary="Sample summary",
                description="Description 2",
                sources=["https://www.google.com"]
            ),
            Idea(
                id=3,
                title="Idea 3",
                summary="Sample summary",
                description="Description 3",
                sources=["https://www.google.com"]
            )
        ]
    }

@router.post("/plans")
async def generate_plan(
    request: IdeaRequest,
) -> Dict[str, Any]:
    """Endpoint for querying the RAG agent about hackathon projects."""
    try:
        # Access the idea details from the request
        idea = request.idea
        
        # Create a dummy response that includes the idea title
        dummy_plan = f"""Project Plan for: {idea.get('title', 'Untitled Idea')}

TIMELINE:
Week 1:
- Set up development environment
- Create basic project structure
- Begin frontend implementation

Week 2:
- Implement core features
- Set up database
- Create API endpoints

Week 3:
- Testing and debugging
- UI/UX improvements
- Documentation

TECHNICAL STACK:
- Frontend: React/Next.js
- Backend: Python/FastAPI
- Database: PostgreSQL
- Deployment: Docker, Cloud Platform

TEAM RESPONSIBILITIES:
1. Frontend Developer:
   - Implement user interface
   - Handle state management
   - Create responsive design

2. Backend Developer:
   - Design API architecture
   - Implement database models
   - Handle authentication

3. Project Manager:
   - Track progress
   - Coordinate team efforts
   - Ensure deadline compliance

DELIVERABLES:
1. Working prototype
2. Source code repository
3. Documentation
4. Presentation deck
"""
        
        return {
            "rawText": dummy_plan
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(
    router,
    prefix="/api",
)

