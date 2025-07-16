from pydantic import BaseModel, Field


class Mod(BaseModel):
    id: int


class FileData(BaseModel):
    file_date: str = Field(alias="fileDate")
    download_url: str = Field(alias="downloadUrl")
