from typing import Any, Dict
from src.agents.base_agent import BaseAgent
from src.utils.openai import OpenAIClient

class RagAgent(BaseAgent):
    """RAG Agent that uses OpenAI to process queries about hackathon projects."""
    
    def __init__(self, openai_client: OpenAIClient):
        """Initialize the RAG agent with an OpenAI client.
        
        Args:
            openai_client: An instance of OpenAIClient for making OpenAI API calls
        """
        self.openai_client = openai_client
        self._system_prompt = """You are a helpful assistant specialized in hackathon projects. 
        Your task is to help users find and understand hackathon projects that match their interests.
        
        When responding:
        1. Analyze the user's query to understand their interests and requirements
        2. Search through the hackathon project database to find relevant projects
        3. Provide detailed information about matching projects, including:
           - Project name and description
           - Technologies used
           - Team members and their roles
           - Project goals and achievements
        4. If no exact matches are found, suggest similar projects or provide guidance
           on how to refine their search
        
        Always be helpful, informative, and encouraging about hackathon participation!"""
    
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