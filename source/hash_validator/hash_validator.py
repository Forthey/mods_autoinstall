import hashlib
from enum import Enum
from typing import Iterator

from hash_validator.i_hash_validator import IHashValidator


class HashAlgorithm(Enum):
    Sha1 = "sha1"
    Md5 = "md5"


class HashValidator(IHashValidator):
    MAX_ENTRIES: int = 1000

    def __init__(self):
        self.files_to_hashes: dict[str, tuple[str, HashAlgorithm]] = {}

    def validate_hash_by_record(self, file_name) -> bool:
        (file_hash, hash_algo) = self.files_to_hashes[file_name]

        if hash_algo == HashAlgorithm.Sha1:
            current_hasher = hashlib.sha1()
        else:
            current_hasher = hashlib.md5()

        with open(file_name, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b''):
                current_hasher.update(chunk)

        calculated_hash = current_hasher.hexdigest()
        return calculated_hash.lower() == file_hash.lower()

    def validate_hashes(self) -> Iterator[tuple[str, bool]]:
        for file_name in self.files_to_hashes.keys():
            yield file_name, self.validate_hash_by_record(file_name)

    def add_validation_record(self, name: str, hash: str, algo: str) -> bool:
        if algo == "sha1":
            algorithm = HashAlgorithm.Sha1
        elif algo == "md5":
            algorithm = HashAlgorithm.Md5
        else:
            raise ValueError(f"Unknown hash algorithm: {algo}")

        if len(self.files_to_hashes) > self.MAX_ENTRIES:
            return False

        self.files_to_hashes[name] = (hash, algorithm)

        return True
