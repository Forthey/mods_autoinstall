from abc import ABC, abstractmethod


class IFileDownloader(ABC):
    @abstractmethod
    async def download_file(self, path: str, name: str, url: str):
        pass
