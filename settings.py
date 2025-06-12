from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SHEET_ID: str

    MINECRAFT_VERSION: str

    DOWNLOAD_PATH: str

    DOWNLOAD_CLIENT: bool

    DOWNLOAD_SERVER: bool

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
