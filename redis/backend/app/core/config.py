from pydantic import BaseSettings


class Settings(BaseSettings):
    CONN_HEARTBEAT = 30
    REDIS_URL = 'redis://redis:6379'


settings = Settings()
