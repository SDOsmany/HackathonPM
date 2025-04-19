from typing import Any, Dict
from src.agents.base_agent import BaseAgent
from src.utils.openai import OpenAIClient
import json

class ProjectPlannerAgent(BaseAgent):
    """Agent that generates detailed project plans and implementation strategies."""
    
    def __init__(self, openai_client: OpenAIClient):
        """Initialize the project planner agent.
        
        Args:
            openai_client: An instance of OpenAIClient for making OpenAI API calls
        """
        self.openai_client = openai_client
        
        self._system_prompt = """You are an expert project planner and technical architect. Your task is to create detailed implementation plans for hackathon projects.

        When creating a project plan:
        1. Break down the project into clear phases:
           - Setup and Planning (1-2 hours)
           - Core Development (12-16 hours)
           - UI/UX Implementation (4-6 hours)
           - Testing and Refinement (2-4 hours)
           - Final Presentation Prep (1-2 hours)

        2. For each phase, provide:
           - Specific tasks and subtasks
           - Required technologies and tools
           - Estimated time for each task
           - Dependencies between tasks
           - Potential challenges and solutions

        3. Include a technical architecture section with:
           - Frontend framework and libraries
           - Backend technologies
           - Database design
           - API endpoints
           - Third-party services

        4. Provide UI/UX recommendations:
           - Color scheme and design system
           - Key screens and components
           - User flow diagrams
           - Accessibility considerations

        5. Add a deployment strategy:
           - Hosting platform
           - CI/CD pipeline
           - Environment setup
           - Monitoring and logging

        Format your response as a JSON object with the following structure:
        {
            "status": "success",
            "message": "string describing the response",
            "project_plan": {
                "title": "project title",
                "phases": [
                    {
                        "name": "phase name",
                        "duration": "estimated duration",
                        "tasks": [
                            {
                                "name": "task name",
                                "description": "detailed description",
                                "duration": "estimated time",
                                "dependencies": ["task1", "task2"],
                                "technologies": ["tech1", "tech2"],
                                "challenges": ["challenge1", "challenge2"]
                            }
                        ]
                    }
                ],
                "technical_architecture": {
                    "frontend": {
                        "framework": "framework name",
                        "libraries": ["lib1", "lib2"],
                        "components": ["comp1", "comp2"]
                    },
                    "backend": {
                        "framework": "framework name",
                        "libraries": ["lib1", "lib2"],
                        "apis": ["api1", "api2"]
                    },
                    "database": {
                        "type": "database type",
                        "schema": "schema description"
                    }
                },
                "ui_ux": {
                    "color_scheme": ["color1", "color2"],
                    "screens": ["screen1", "screen2"],
                    "components": ["comp1", "comp2"],
                    "user_flow": "flow description"
                },
                "deployment": {
                    "platform": "platform name",
                    "pipeline": ["step1", "step2"],
                    "environments": ["env1", "env2"]
                }
            }
        }

        Make sure to:
        - Keep all time estimates realistic for a 24-48 hour hackathon
        - Include specific technologies and tools
        - Provide detailed but actionable tasks
        - Consider scalability and maintainability
        - Return ONLY the JSON object, no other text"""
    
    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parse the response text to extract JSON.
        
        Args:
            text: Response text from the model
            
        Returns:
            Parsed JSON response
        """
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        return {
            "status": "error",
            "message": "Failed to parse response as JSON",
            "project_plan": None
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed project plan.
        
        Args:
            input_data: Dictionary containing the project idea and any additional context
            
        Returns:
            Dictionary containing the project plan
        """
        project_idea = input_data.get("idea", {})
        
        # Create the messages for the chat completion
        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": f"Create a detailed project plan for this idea:\n\nTitle: {project_idea.get('title', '')}\nSummary: {project_idea.get('summary', '')}"}
        ]
        
        # Get the response from OpenAI
        response = await self.openai_client.llm.ainvoke(messages)
        
        # Parse the response to extract JSON
        return self._parse_json_response(response.content) 