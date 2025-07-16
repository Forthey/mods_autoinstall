from config import get_settings
from models import file_downloader

DOWNLOAD_FILE_FORMAT = "csv"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{get_settings().sheet_id}/export?format={DOWNLOAD_FILE_FORMAT}"

async def download_sheet(name: str):
    full_name = f"{name}.{DOWNLOAD_FILE_FORMAT}";
    print(f"Downloading {full_name}")
    await file_downloader.download(
        name=full_name,
        folder=".",
        url=SHEET_URL
    )
    print(f"✅ Google Sheet downloaded as {DOWNLOAD_FILE_FORMAT}!")
