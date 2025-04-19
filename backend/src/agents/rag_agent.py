from typing import Any, Dict, List
from src.agents.base_agent import BaseAgent
from src.utils.openai import OpenAIClient
from src.utils.vector_db import VectorDB
from langchain.tools import Tool

class RagAgent(BaseAgent):
    """RAG Agent that uses OpenAI and VectorDB to process queries about hackathon projects."""
    
    def __init__(self, openai_client: OpenAIClient, vector_db: VectorDB):
        """Initialize the RAG agent with an OpenAI client and VectorDB.
        
        Args:
            openai_client: An instance of OpenAIClient for making OpenAI API calls
            vector_db: An instance of VectorDB for document retrieval
        """
        self.openai_client = openai_client
        self.vector_db = vector_db
        
        # Create the document search tool
        self.document_search_tool = Tool(
            name="document_search",
            func=self._search_documents,
            description="Search for relevant documents in the vector database. Input should be a search query string."
        )
        
        self._system_prompt = """You are a helpful assistant specialized in hackathon projects. 
        Your task is to help users find and understand hackathon projects that match their interests.
        
        When responding:
        1. Analyze the user's query to understand their interests and requirements
        2. Use the document_search tool to find relevant projects
        3. Provide detailed information about matching projects, including:
           - Project name and description
           - Technologies used
           - Team members and their roles
           - Project goals and achievements
        4. If no exact matches are found, suggest similar projects or provide guidance
           on how to refine their search
        
        Always be helpful, informative, and encouraging about hackathon participation!"""
    
    def _search_documents(self, query: str) -> str:
        """Search for relevant documents in the vector database.
        
        Args:
            query: Search query
            
        Returns:
            Formatted string containing search results
        """
        results = self.vector_db.similarity_search(query)
        
        if not results:
            return "No relevant documents found."
        
        formatted_results = []
        for i, result in enumerate(results, 1):
            formatted_results.append(
                f"Result {i}:\n"
                f"Content: {result['content']}\n"
                f"Metadata: {result['metadata']}\n"
            )
        
        return "\n".join(formatted_results)
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the user's query about hackathon projects.
        
        Args:
            input_data: Dictionary containing the user's query and any additional context
            
        Returns:
            Dictionary containing the agent's response
        """
        user_query = input_data.get("query", "")
        
        # Create the messages for the chat completion
        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        # Get the response from OpenAI
        response = await self.openai_client.llm.ainvoke(messages)
        
        return {
            "response": response.content,
            "query": user_query
        } 