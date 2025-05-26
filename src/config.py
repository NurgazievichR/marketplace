from typing import Annotated

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_HOST: str
    POSTGRES_DB: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int

    @computed_field
    @property
    def postgres_url(self) -> Annotated[PostgresDsn, 'DSN']:
        return (f'postgresql+asyncpg://'
                f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}/{self.POSTGRES_DB}')
    
    @property
    def get_auth_data(self):
        return {"key": self.JWT_SECRET, "algorithm": self.JWT_ALGORITHM}

    class Config:
        env_file = ".env"

settings = Settings()