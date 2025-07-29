import asyncio
import os
from typing import Coroutine

import pandas as pd

from file_downloader import ModFileDownloader
from google_table import download_sheet
from google_table.download_sheet import DOWNLOAD_FILE_FORMAT
from models import make_safe_path
from config import settings

MINECRAFT_VERSION = settings.minecraft_version
DOWNLOAD_PATH = os.path.realpath(settings.download_path)


async def main():
    await download_sheet("mods")

    df = pd.read_csv(f"mods.{DOWNLOAD_FILE_FORMAT}")

    if not os.path.isdir(DOWNLOAD_PATH):
        os.mkdir(DOWNLOAD_PATH)

    tasks: list[Coroutine] = []

    mod_file_downloader = ModFileDownloader(DOWNLOAD_PATH, settings.minecraft_mod_loader, settings.minecraft_version)
    for index, row in df.iterrows():
        result: bool = True

        if settings.download_client and str(row.get("client-url")).startswith("https://"):
            mod_url: str = str(row.get(f"client-url"))
            mod_name: str = make_safe_path(str(row.get(f"client-name")))
            tasks.append(mod_file_downloader.download_file(
                folder="client",
                mod_name=mod_name,
                mod_url=mod_url
            ))

        if result and settings.download_server and str(row.get("server-url")).startswith("https://"):
            mod_url: str = str(row.get(f"server-url"))
            mod_name: str = make_safe_path(str(row.get(f"server-name")))
            tasks.append(mod_file_downloader.download_file(
                folder="server",
                mod_name=mod_name,
                mod_url=mod_url
            ))

    await asyncio.gather(*tasks)

    os.remove(f"mods.{DOWNLOAD_FILE_FORMAT}")

    mod_file_downloader.validate_hashes()

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    asyncio.run(main())
