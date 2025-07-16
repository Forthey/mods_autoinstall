import asyncio
from pathlib import Path
import aiohttp
from models import singleton


@singleton
class FileDownloader:
    def __init__(self):
        pass

    async def download(self, name: str, folder: str, url: str):
        path = Path(f"{folder}/{name}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                with open(path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)

        print(f"✅ Downloaded: {path}")

file_downloader = FileDownloader()
