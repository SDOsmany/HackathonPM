from langchain_openai import ChatOpenAI
from typing import Optional
from src.config.config import ConfigManager

class OpenAIClient:
    _instance: Optional['OpenAIClient'] = None
    _llm: Optional[ChatOpenAI] = None

    def __init__(self):
        # Prevent direct instantiation
        if OpenAIClient._instance is not None:
            raise RuntimeError("Use get_instance() instead")
        
        # Get OpenAI config
        config = ConfigManager().get_openai_config()
        
        # Initialize the LLM
        self._llm = ChatOpenAI(
            model=config.model,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=None,
            max_retries=2,
            api_key=config.api_key,
        )
    
    @classmethod
    def get_instance(cls) -> 'OpenAIClient':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @property
    def llm(self) -> ChatOpenAI:
        return self._llm
    
    def create_agent(self, tools, prompt):
        """
        Creates a tool calling agent with the configured LLM
        """
        from langchain.agents import create_tool_calling_agent
        return create_tool_calling_agent(self.llm, tools, prompt)