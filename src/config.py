from typing import Annotated

from pydantic import ConfigDict, PostgresDsn, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_HOST: str  
    POSTGRES_DB: str
    POSTGRES_DB_TEST: str

    REDIS_HOST: str  
    REDIS_PORT: str  

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE: int
    JWT_REFRESH_TOKEN_EXPIRE: int

    @computed_field
    @property
    def postgres_url(self) -> Annotated[PostgresDsn, 'DSN']:
        return (f'postgresql+asyncpg://'
                f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}/{self.POSTGRES_DB}')
    
    @property
    def postgres_url_test(self) -> Annotated[PostgresDsn, 'DSN']:
        return self.postgres_url + '_test'
    
    
    @computed_field
    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
    
    @property
    def get_auth_data(self):
        return {"key": self.JWT_SECRET, "algorithm": self.JWT_ALGORITHM}

    model_config = ConfigDict(env_file=".env")

settings = Settings()