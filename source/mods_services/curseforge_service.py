from config import settings
from schemas.curseforge import Mod, FileData
from mods_services.mods_service import ModsService
from models.singleton import singleton


@singleton
class CurseForgeService(ModsService):
    def __init__(self):
        super().__init__(
            base_url="https://www.curseforge.com",
            api_base_url="https://api.curseforge.com/v1"
        )
        self.__api_key = settings.curseforge_api_key
        self.__minecraft_game_id = 432
        self.__mc_mods_class_id = 6
        self.__mod_loader_name_to_id: dict[str, int] = {
            "any": 0,
            "forge": 1,
            "cauldron": 2,
            "liteloader": 3,
            "fabric": 4,
            "quilt": 5,
            "neoforge": 6
        }

    async def _fetch_data_with_key(self, url: str, params: dict[str, any]) -> dict[str, any]:
        return await self._fetch_data(url, params, headers={"x-api-key": self.__api_key})

    async def get_download_link(self, name: str, mod_loader: str, version: str):
        mod_loader_id = self.__mod_loader_name_to_id.get(mod_loader)
        if mod_loader_id is None:
            raise KeyError

        response = await self._fetch_data_with_key(
            url=f"/mods/search",
            params={
                "gameId": 432,
                "classId": 6,
                "slug": name,
                "gameVersion": version,
            }
        )

        data: list[dict] | None = response.get("data")
        if data is None:
            raise ValueError

        mods: list[Mod] = [Mod.model_validate(mod) for mod in data]
        if len(mods) != 1:
            raise ValueError

        response = await self._fetch_data_with_key(
            url=f"/mods/{mods[0].id}/files",
            params={
                "gameVersion": version,
                "modLoaderType": mod_loader_id
            }
        )

        data: list[dict] | None = response.get("data")
        if data is None:
            raise ValueError

        files: list[FileData] = [FileData.model_validate(file) for file in data]
        if len(files) == 0:
            raise ValueError(f"No files in latest version of {name}")

        files = sorted(files, key=lambda file: file.file_date, reverse=True)

        return files[0].download_url


curseforge_service = CurseForgeService()
