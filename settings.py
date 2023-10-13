from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    server_host: str = 'localhost' 
    server_port: int = 8050
    
    database_url: str = 'postgresql+asyncpg://postgres:postgres@db:8787/postgres'

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_file_encoding='utf-8',
        extra='allow'
        )



settings = Settings()