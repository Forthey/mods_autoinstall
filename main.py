import asyncio
import os

import aiohttp
import pandas as pd
from tqdm import tqdm

import modrinth_requests
from download_sheet import download_sheet
from settings import settings

MINECRAFT_VERSION = settings.MINECRAFT_VERSION
DOWNLOAD_PATH = os.path.realpath(settings.DOWNLOAD_PATH)


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
    download_sheet("mods")

    df = pd.read_excel('mods.xlsx', sheet_name='Лист1')

    try:
        os.mkdir("client")
        os.mkdir("server")
    except FileExistsError:
        pass

    for index, row in df.iterrows():
        if int(index) < 4:
            continue

        if settings.DOWNLOAD_CLIENT:
            mod_url = row.get("client-url")
            mod_name = row.get("client-name")

            download_link = await modrinth_requests.get_download_link(mod_url.split("/")[-1], "neoforge",
                                                                      MINECRAFT_VERSION)
            await download_file(mod_name, "client", download_link)

        if settings.DOWNLOAD_SERVER:
            mod_url = row.get("server-url")
            mod_name = row.get("server-name")

            download_link = await modrinth_requests.get_download_link(mod_url.split("/")[-1], "neoforge",
                                                                      MINECRAFT_VERSION)
            await download_file(mod_name, "server", download_link)

    os.remove("mods.xlsx")


asyncio.run(main())
