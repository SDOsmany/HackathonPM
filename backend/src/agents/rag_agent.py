from typing import Any, Dict, List
from src.agents.base_agent import BaseAgent
from src.utils.openai import OpenAIClient
from src.utils.vector_db import VectorDB
from langchain.tools import Tool
import json
import uuid

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
        
        self._system_prompt = """You are a creative hackathon project idea generator. Your task is to analyze existing hackathon projects and generate 3 new, innovative ideas based on them.

        When generating ideas:
        1. Analyze the search results to understand the types of projects and technologies used
        2. For each idea:
           - Create a unique, catchy title that reflects the project's purpose
           - Write a detailed summary (3-5 sentences) that explains:
             * The problem the project solves
             * The main features and functionality
             * The target users and their needs
             * The technologies that could be used
             * The potential impact or benefits
        3. Use the search results as inspiration but create original ideas
        4. Make sure each idea is feasible for a hackathon (can be built in 24-48 hours)
        5. Include relevant sources from the search results that inspired each idea

        Format your response as a JSON object with the following structure:
        {
            "status": "success",
            "message": "string describing the response",
            "ideas": [
                {
                    "id": "unique identifier",
                    "title": "creative project title",
                    "summary": "3-5 sentence detailed description",
                    "sources": ["source1", "source2"]
                }
            ]
        }

        Make sure to:
        - Generate unique, memorable titles
        - Write detailed, informative summaries
        - Include specific technologies and features
        - Reference relevant sources that inspired each idea
        - Return ONLY the JSON object, no other text"""
    
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
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse the response text to extract JSON.
        
        Args:
            text: Response text from the model
            
        Returns:
            Parsed JSON response
        """
        # Try to find JSON in the response
        try:
            # Look for JSON object in the text
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # If JSON parsing fails, return an error response
        return {
            "status": "error",
            "message": "Failed to parse response as JSON",
            "ideas": []
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process the user's query about hackathon projects.
        
        Args:
            input_data: Dictionary containing the user's query and any additional context
            
        Returns:
            Dictionary containing the agent's response
        """
        user_query = input_data.get("query", "")
        
        # First, search for relevant documents
        search_results = self._search_documents(user_query)
        
        # Create the messages for the chat completion
        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": f"Query: {user_query}\n\nSearch Results:\n{search_results}"}
        ]
        
        # Get the response from OpenAI
        response = await self.openai_client.llm.ainvoke(messages)
        
        # Parse the response to extract JSON
        return self._parse_json_response(response.content) 