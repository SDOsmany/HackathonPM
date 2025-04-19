from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from typing import Optional

class OpenAIClient:
    _instance: Optional['OpenAIClient'] = None
    _llm: Optional[ChatOpenAI] = None

    def __init__(self):
        # Prevent direct instantiation
        if OpenAIClient._instance is not None:
            raise RuntimeError("Use get_instance() instead")
        load_dotenv()
        
    @classmethod
    def get_instance(cls) -> 'OpenAIClient':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def llm(self) -> ChatOpenAI:
        if self._llm is None:
            self._llm = ChatOpenAI(
                model="gpt-4.1",  # Fixed typo from "gpt-4o"
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        return self._llm
    
    def create_agent(self, tools, prompt):
        """
        Creates a tool calling agent with the configured LLM
        """
        from langchain.agents import create_tool_calling_agent
        return create_tool_calling_agent(self.llm, tools, prompt)