from abc import ABC, abstractmethod
from typing import Any

class BaseAgent(ABC):
    """Base class for all agents in the system."""
    
    @abstractmethod
    async def process(self, input_data: Any) -> Any:
        """Process the input data and return the result."""
        pass 