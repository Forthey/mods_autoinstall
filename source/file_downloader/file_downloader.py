from pathlib import Path
import aiohttp

from async_print import async_print
from file_downloader.i_file_downloader import IFileDownloader

class FileDownloader(IFileDownloader):
    def __init__(self):
        pass

    async def download_file(self, path: str, name: str, url: str):
        path = Path(f"{path}/{name}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                with open(path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        f.write(chunk)

        await async_print(f"✅ Downloaded: {path}")
