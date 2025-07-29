import os
from pathlib import Path

from async_print import async_print
from console_colors import CColor
from file_downloader.file_downloader import FileDownloader
from file_downloader.i_file_downloader import IFileDownloader
from hash_validator import IHashValidator, HashValidator
from mods_services import curseforge_service, modrinth_service, DownloadFileInfo


class ModFileDownloader:
    def __init__(self, download_root_path: str, minecraft_mod_loader: str, minecraft_version: str):
        self.download_root_path = download_root_path
        self.minecraft_mod_loader = minecraft_mod_loader
        self.minecraft_version = minecraft_version

        self.file_downloader: IFileDownloader = FileDownloader()
        self.hash_validator: IHashValidator = HashValidator()

    @staticmethod
    def _check_dir(path: str):
        if os.path.isdir(path):
            return

        os.mkdir(path)

    async def download_file(self, folder: str, mod_name: str, mod_url: str) -> bool:
        ModFileDownloader._check_dir(f"{self.download_root_path}/{folder}")

        try:
            download_file_info: DownloadFileInfo
            mod_url_name: str = mod_url.split("/")[-1]

            if curseforge_service.is_valid_url(mod_url):
                download_file_info = await curseforge_service.get_download_file_info(mod_url_name,
                                                                                     self.minecraft_mod_loader,
                                                                                     self.minecraft_version)
            elif modrinth_service.is_valid_url(mod_url):
                download_file_info = await modrinth_service.get_download_file_info(mod_url_name,
                                                                                   self.minecraft_mod_loader,
                                                                                   self.minecraft_version)
            else:
                raise ValueError(f"Invalid URL: {mod_url}")

            file_path = f"{self.download_root_path}/{folder}"
            file_name = f"{mod_name}.jar"
            file_full_path = f"{file_path}/{file_name}"

            if not self.hash_validator.add_validation_record(
                name=file_full_path,
                hash=download_file_info.hash,
                algo=download_file_info.hash_algorithm,
            ):
                await async_print(f"Cannot add validation record for {mod_name}")

            if os.path.exists(Path(file_full_path)):
                if self.hash_validator.validate_hash_by_record(file_full_path):
                    await async_print(f"🟠 Mod {mod_name} already downloaded, skipping")
                    return False
                else:
                    await async_print(f"🟠 {CColor.YELLOW}Mod {mod_name} already downloaded, but has invalid hash{CColor.RESET}")

            await self.file_downloader.download_file(
                path=file_path,
                name=file_name,
                url=download_file_info.url
            )

        except Exception as error:
            await async_print(f"❌ DID NOT downloaded: {mod_name}: {error}")
            return False
        return True

    def validate_hashes(self):
        all_valid: bool = True

        print(f"\n{CColor.YELLOW}Verifying file hashes...{CColor.RESET}\n")
        for filename, is_valid in self.hash_validator.validate_hashes():
            if not is_valid:
                all_valid = False
            print(f"{filename}: {f"{CColor.GREEN}OK{CColor.RESET}" if is_valid else f"{CColor.RED}FAIL{CColor.RESET}"}")

        if not all_valid:
            print(f"❌ {CColor.RED}Some of the files did non downloaded successfully, please rerun installation programm{CColor.RESET}")
        else:
            print(f"✅ {CColor.GREEN}All downloads completed!{CColor.RESET}")
