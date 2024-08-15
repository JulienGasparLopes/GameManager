import json
import os
from abc import ABC, abstractmethod

from game_manager.logic.uid_object import Uid
from game_manager.storage.storage_manager import StorageManager


class FileSystemStorageManager(StorageManager, ABC):
    _storage_path: str

    def __init__(self, storage_path: str) -> None:
        super().__init__()
        self._storage_path = storage_path

    def _store_data(self, data_type: str, uid: Uid, data: dict[object, object]) -> None:
        filename = f"{self._storage_path}/{data_type}_{uid}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as file:
            file.write(json.dumps(data))

    def _retrieve_data(self, data_type: str, uid: Uid) -> dict[object, object] | None:
        filename = f"{self._storage_path}/{data_type}_{uid}.json"
        if not os.path.exists(filename):
            return None
        with open(filename, "r") as file:
            data: dict[object, object] = json.loads(file.read())
        return data

    @abstractmethod
    def _unparse_object(self, object_to_unparse: object) -> dict[object, object]: ...

    @abstractmethod
    def _parse_object(self, object_data: dict[object, object]) -> object: ...
