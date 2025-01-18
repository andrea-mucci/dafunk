from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite:///dafunk_test.db"