from enum import IntEnum

from pydantic import BaseModel, Field


class Mod(BaseModel):
    id: int


class HashAlgo(IntEnum):
    Sha1 = 1
    Md5 = 2


class FileHash(BaseModel):
    value: str
    algo: HashAlgo


class FileData(BaseModel):
    file_date: str = Field(alias="fileDate")
    download_url: str = Field(alias="downloadUrl")
    file_hashes: list[FileHash] = Field(alias="hashes")
