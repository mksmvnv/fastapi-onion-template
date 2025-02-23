import yaml

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    title: str
    version: str
    root_path: str
    port: int


class AuthSettings(BaseModel):
    private_key_path: Path
    public_key_path: Path
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int


class DatabaseSettings(BaseModel):
    url: str


class QuerySettings(BaseModel):
    default_page: int
    default_limit: int
    max_limit: int


class Settings(BaseSettings):
    app: AppSettings
    auth: AuthSettings
    database: DatabaseSettings
    query: QuerySettings

    model_config = SettingsConfigDict(validate_default=True)

    @classmethod
    def from_yaml(cls, path: Path):
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return cls(**data)


config_path = Path(__file__).parent / "config.yaml"

settings = Settings.from_yaml(config_path)
