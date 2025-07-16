from datetime import datetime

from pydantic import BaseModel


class FileData(BaseModel):
    url: str


class Version(BaseModel):
    id: str
    date_published: datetime
    files: list[FileData]
