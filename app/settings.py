from pydantic import BaseSettings, PostgresDsn, RedisDsn


class Settings(BaseSettings):
    database_dsn: PostgresDsn
    redis_dsn: RedisDsn


settings = Settings()
