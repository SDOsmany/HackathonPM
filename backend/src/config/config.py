from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

class OpenAIConfig(BaseModel):
    """OpenAI configuration settings."""
    api_key: str = Field(..., description="OpenAI API key")
    model: str = Field(default="gpt-4", description="OpenAI model to use")
    temperature: float = Field(default=0.0, description="Model temperature")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens to generate")

class ServerConfig(BaseModel):
    """Server configuration settings."""
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=True, description="Debug mode")
    cors_origins: list[str] = Field(default=[], description="Allowed CORS origins")

class Config(BaseModel):
    """Main configuration class that combines all config sections."""
    openai: OpenAIConfig
    server: ServerConfig = Field(default_factory=ServerConfig)

class ConfigManager:
    """Singleton class to manage configuration."""
    _instance: Optional['ConfigManager'] = None
    _config: Optional[Config] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._config is None:
            self._load_config()

    def _load_config(self) -> None:
        """Load configuration from environment variables."""
        load_dotenv()

        # Load OpenAI config
        openai_config = OpenAIConfig(
            api_key=os.getenv("OPENAI_API_KEY", ""),
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.0")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "0")) if os.getenv("OPENAI_MAX_TOKENS") else None
        )

        # Load server config
        server_config = ServerConfig(
            host=os.getenv("SERVER_HOST", "0.0.0.0"),
            port=int(os.getenv("SERVER_PORT", "8000")),
            debug=os.getenv("DEBUG", "True").lower() == "true",
            cors_origins=os.getenv("CORS_ORIGINS", "").split(",") if os.getenv("CORS_ORIGINS") else []
        )

        self._config = Config(
            openai=openai_config,
            server=server_config
        )

    @property
    def config(self) -> Config:
        """Get the current configuration."""
        return self._config

    def get_openai_config(self) -> OpenAIConfig:
        """Get OpenAI configuration."""
        return self._config.openai

    def get_server_config(self) -> ServerConfig:
        """Get server configuration."""
        return self._config.server 