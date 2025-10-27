from pydantic import BaseModel
import os

class Settings(BaseModel):
    app_name: str = "API Test Playground"
    env: str = os.getenv("ENV", "local")
    db_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    seed: bool = os.getenv("SEED", "true").lower() == "true"

settings = Settings()