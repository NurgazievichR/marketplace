from typing import Annotated

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str 
    POSTGRES_HOST: str
    POSTGRES_DB: str

    @computed_field
    @property
    def postgres_url(self) -> Annotated[PostgresDsn, 'DSN']:
        return (f'postgresql+asyncpg://'
                f'{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@'
                f'{self.POSTGRES_HOST}/{self.POSTGRES_DB}')

