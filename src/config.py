from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")
    
    database_url: str 
    enviroment: str = "production"
    
settings = Settings()