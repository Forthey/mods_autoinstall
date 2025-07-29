from models.singleton import singleton
from schemas.modrinth import Version
from .mods_service import ModsService, DownloadFileInfo


@singleton
class ModrinthService(ModsService):
    def __init__(self):
        super().__init__(
            base_url="https://modrinth.com",
            api_base_url="https://api.modrinth.com/v2"
        )

    async def get_download_file_info(self, name: str, mod_loader: str, version: str) -> DownloadFileInfo:
        response = await self._fetch_data(
            f"/project/{name}/version",
            {
                "loaders": f"[\"{mod_loader}\"]",
                "game_versions": f"[\"{version}\"]"
            }
        )

        versions: list[Version] = [Version.model_validate(ver) for ver in response]
        versions = sorted(versions, key=lambda ver: ver.date_published, reverse=True)

        if not versions:
            raise IndexError(f"No versions found for {name} ({mod_loader}, {version})")

        if not versions[0].files:
            raise ValueError(f"No files in latest version of {name}")

        file = versions[0].files[0]

        return DownloadFileInfo(
            url=file.url,
            hash=file.hashes.sha1,
            hash_algorithm="sha1"
        )


modrinth_service = ModrinthService()
