import asyncio
import os
from pathlib import Path
from typing import Coroutine

import pandas as pd

from google_table import download_sheet
from google_table.download_sheet import DOWNLOAD_FILE_FORMAT
from models import make_safe_path, file_downloader
from mods_services import modrinth_service, curseforge_service
from config import settings

MINECRAFT_VERSION = settings.minecraft_version
DOWNLOAD_PATH = os.path.realpath(settings.download_path)


def check_dir(path: str):
    if os.path.isdir(path):
        return

    os.mkdir(path)


async def download_mod_file(folder: str, mod_name: str, mod_url: str) -> bool:
    check_dir(f"{DOWNLOAD_PATH}/{folder}")

    if os.path.exists(Path(f"{DOWNLOAD_PATH}/{folder}/{mod_name}.jar")):
        print(f"🟠 Mod {mod_name} already downloaded, skipping")
        return False

    try:
        download_link: str
        mod_url_name: str = mod_url.split("/")[-1]

        if curseforge_service.is_valid_url(mod_url):
            download_link = await curseforge_service.get_download_link(mod_url_name, settings.minecraft_mod_loader,
                                                                       MINECRAFT_VERSION)
        elif modrinth_service.is_valid_url(mod_url):
            download_link = await modrinth_service.get_download_link(mod_url_name, settings.minecraft_mod_loader,
                                                                     MINECRAFT_VERSION)
        else:
            raise ValueError(f"Invalid URL: {mod_url}")

        await file_downloader.download(
            name=f"{mod_name}.jar",
            folder=f"{DOWNLOAD_PATH}/{folder}".replace("//", "/"),
            url=download_link
        )
    except Exception as error:
        print(f"❌ DID NOT downloaded: {mod_name}: {error}")
        return False
    return True


async def main():
    await download_sheet("mods")

    df = pd.read_csv(f"mods.{DOWNLOAD_FILE_FORMAT}")

    if not os.path.isdir(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)

    tasks: list[Coroutine] = []

    for index, row in df.iterrows():
        result: bool = True

        if settings.download_client and str(row.get("client-url")).startswith("https://"):
            mod_url: str = str(row.get(f"client-url"))
            mod_name: str = make_safe_path(str(row.get(f"client-name")))
            tasks.append(download_mod_file(
                folder="client",
                mod_name=mod_name,
                mod_url=mod_url
            ))

        if result and settings.download_server and str(row.get("server-url")).startswith("https://"):
            mod_url: str = str(row.get(f"server-url"))
            mod_name: str = make_safe_path(str(row.get(f"server-name")))
            tasks.append(download_mod_file(
                folder="server",
                mod_name=mod_name,
                mod_url=mod_url
            ))

    await asyncio.gather(*tasks)

    print("✅ All downloads completed!")

    os.remove(f"mods.{DOWNLOAD_FILE_FORMAT}")


if __name__ == "__main__":
    asyncio.run(main())
