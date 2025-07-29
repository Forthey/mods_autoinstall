from datetime import datetime

from pydantic import BaseModel


class Hashes(BaseModel):
    sha512: str
    sha1: str


class FileData(BaseModel):
    url: str
    hashes: Hashes


class Version(BaseModel):
    id: str
    date_published: datetime
    files: list[FileData]
