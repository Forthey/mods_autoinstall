from async_print import async_print
from config import get_settings
from console_colors import CColor
from file_downloader import IFileDownloader, FileDownloader

DOWNLOAD_FILE_FORMAT = "csv"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{get_settings().sheet_id}/export?format={DOWNLOAD_FILE_FORMAT}"


async def download_sheet(name: str):
    file_downloader: IFileDownloader = FileDownloader()

    full_name = f"{name}.{DOWNLOAD_FILE_FORMAT}"
    await async_print(f"{CColor.YELLOW}Downloading {full_name}{CColor.RESET}...")
    await file_downloader.download_file(
        path=".",
        name=full_name,
        url=SHEET_URL
    )
