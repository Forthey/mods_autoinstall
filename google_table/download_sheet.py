import requests

from settings import get_setting


SHEET_URL = f"https://docs.google.com/spreadsheets/d/{get_setting().SHEET_ID}/export?format=xlsx"


def download_sheet(name: str):
    response = requests.get(SHEET_URL)
    response.raise_for_status()

    with open(f"google_table/tables/{name}.xlsx", "wb") as f:
        f.write(response.content)

    print("✅ Google Sheet downloaded as Excel!")
