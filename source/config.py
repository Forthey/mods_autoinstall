from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sheet_id: str = Field(alias="SHEET_ID")

    curseforge_api_key: str = Field(alias="CURSEFORGE_API_KEY")

    minecraft_version: str = Field(alias="MINECRAFT_VERSION")

    minecraft_mod_loader: str = Field(alias="MINECRAFT_MOD_LOADER")

    download_path: str = Field(alias="DOWNLOAD_PATH")

    download_client: bool = Field(alias="DOWNLOAD_CLIENT")

    download_server: bool = Field(alias="DOWNLOAD_SERVER")

    model_config = SettingsConfigDict(env_file="config.txt")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
