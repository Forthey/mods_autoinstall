from abc import ABC, abstractmethod
from typing import Iterator


class IHashValidator(ABC):
    @abstractmethod
    def validate_hashes(self) -> Iterator[tuple[str, bool]]: ...

    @abstractmethod
    def add_validation_record(self, name: str, hash: str, algo: str) -> bool: ...

    @abstractmethod
    def validate_hash_by_record(self, file_name) -> bool: ...
