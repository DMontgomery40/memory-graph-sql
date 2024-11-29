from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./semantic.db"
    SEMANTIC_MIN_CONFIDENCE: float = 0.7
    PATTERN_LEARNING_ENABLED: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()