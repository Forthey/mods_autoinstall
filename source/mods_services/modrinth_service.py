from models.singleton import singleton
from schemas.modrinth import Version
from .mods_service import ModsService


@singleton
class ModrinthService(ModsService):
    def __init__(self):
        super().__init__(
            base_url="https://modrinth.com",
            api_base_url="https://api.modrinth.com/v2"
        )

    async def get_download_link(self, name: str, mod_loader: str, version: str) -> str:
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

        return versions[0].files[0].url


modrinth_service = ModrinthService()
