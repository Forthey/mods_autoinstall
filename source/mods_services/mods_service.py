from abc import abstractmethod

import aiohttp

class ModsService:
    def __init__(self, base_url: str, api_base_url: str):
        self._base_url = base_url
        self._api_base_url: str = api_base_url

    async def _fetch_data(self, url: str, params: dict[str, any], headers: dict[str, any] | None = None) -> dict[str, any]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._api_base_url}{url}", params=params,
                                   headers=headers) as response:
                return await response.json()

    @abstractmethod
    async def get_download_link(self, name: str, mod_loader: str, version: str) -> str:
        pass

    def is_valid_url(self, url: str) -> bool:
        return self._base_url in url
