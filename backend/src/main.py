from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List

from src.agents.rag_agent import RagAgent
from src.agents.project_planner_agent import ProjectPlannerAgent
from src.utils.openai import OpenAIClient
from src.utils.vector_db import VectorDB
from src.config.config import ConfigManager

# Initialize config
config_manager = ConfigManager()
config = config_manager.config

# Create FastAPI app
app = FastAPI(
    title="RAG API",
    description="API for RAG",
    version="0.1.0",
    debug=config.server.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.server.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

class QueryInput(BaseModel):
    query: str

class IdeaInput(BaseModel):
    idea: Dict[str, Any]

# Initialize services
vector_db = VectorDB(config_manager)
vector_db.load_documents()  # Load documents from configured source

async def get_rag_agent() -> RagAgent:
    """Dependency injection for the RAG agent."""
    openai_client = OpenAIClient.get_instance()
    return RagAgent(openai_client, vector_db)

@router.post("/rag")
async def rag_query(
    request: QueryRequest,
    rag_agent: RagAgent = Depends(get_rag_agent)
) -> Dict[str, Any]:
    """Endpoint for querying the RAG agent about hackathon projects."""
    response = await rag_agent.process({"query": request.query})
    return response

@app.post("/plans")
async def generate_plan(input_data: IdeaInput) -> Dict[str, Any]:
    """Generate a detailed project plan for a selected idea."""
    try:
        project_planner_agent = ProjectPlannerAgent(OpenAIClient.get_instance())
        response = await project_planner_agent.process(input_data.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(
    router,
    prefix="/api",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


