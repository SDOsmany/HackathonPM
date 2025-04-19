from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import Dict, Any

from src.agents.rag_agent import RagAgent
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

async def get_rag_agent() -> RagAgent:
    """Dependency injection for the RAG agent."""
    openai_client = OpenAIClient.get_instance()
    return RagAgent(openai_client)

@router.post("/rag")
async def rag_query(
    request: QueryRequest,
    rag_agent: RagAgent = Depends(get_rag_agent)
) -> Dict[str, Any]:
    """Endpoint for querying the RAG agent about hackathon projects."""
    response = await rag_agent.process({"query": request.query})
    return response

app.include_router(
    router,
    prefix="/api",
)


