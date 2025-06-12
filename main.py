import asyncio
import os

import aiohttp
import pandas as pd
from tqdm import tqdm

from google_table import download_sheet
from modr_requests import get_download_link
from settings import get_setting


MINECRAFT_VERSION = get_setting().MINECRAFT_VERSION
DOWNLOAD_PATH = os.path.realpath(get_setting().DOWNLOAD_PATH)


async def download_file(name: str, folder: str, url: str):
    path = f"{DOWNLOAD_PATH}\\{folder}\\{name}.jar"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            with open(path, 'wb') as f, tqdm(
                    desc=path,
                    total=total_size,
                    unit='B',
                    unit_scale=True,
            ) as pbar:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    pbar.update(len(chunk))
    

    print(f"✅ Downloaded: {path}")


async def main():
    def check_dir(path: str):
        if os.path.isdir(path):
            return
        
        os.mkdir(path)


    async def download_file_mode(mode: str) -> bool:
        mod_url: str = str(row.get(f"{mode}-url"))
        mod_name: str = str(row.get(f"{mode}-name"))

        check_dir(f"{DOWNLOAD_PATH}/{mode}")
        
        try:
            download_link = await get_download_link(mod_url.split("/")[-1], "neoforge", MINECRAFT_VERSION)
        except Exception as error:
            print(f"❌ DID NOT downloaded: {mod_name}: {error}")
            return False

        await download_file(mod_name, mode, download_link)
        
        return True

    download_sheet("mods")

    df = pd.read_excel("google_table/tables/mods.xlsx", sheet_name="Лист1")

    if not os.path.isdir(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)

    for index, row in df.iterrows():
        if not str(row.get("client-url")).startswith("https://"):
            continue

        result: bool = True

        if get_setting().DOWNLOAD_CLIENT:
            result = await download_file_mode("client")

        if result and get_setting().DOWNLOAD_SERVER:
            await download_file_mode("server")

    os.remove("google_table/tables/mods.xlsx")


if __name__ == "__main__":
    asyncio.run(main())
