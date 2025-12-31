from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Config(BaseSettings):
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    DATABASE_URL: Optional[str] = Field(default=None)
    EMBEDDING_MODEL_PATH: Optional[str] = Field(default="local-models/granite-embedding.gguf")
    model_config = SettingsConfigDict(env_file=".env")