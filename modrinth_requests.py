from datetime import datetime

import aiohttp
from pydantic import BaseModel


class FileData(BaseModel):
    url: str


class Version(BaseModel):
    id: str
    date_published: datetime
    files: list[FileData]


async def fetch_data(url: str, params: dict[str, any]):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            return await response.json()


async def get_download_link(name: str, mod_loader: str, version: str) -> str:
    response = await fetch_data(
        f"https://api.modrinth.com/v2/project/{name}/version",
        {
            "loaders": f"[\"{mod_loader}\"]",
            "game_versions": f"[\"{version}\"]"
        }
    )

    versions: list[Version] = [Version.model_validate(ver) for ver in response]
    versions = sorted(versions, key=lambda ver: ver.date_published, reverse=True)

    return versions[0].files[0].url
