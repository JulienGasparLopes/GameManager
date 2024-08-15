from abc import ABC, abstractmethod
from typing import Protocol, Type, TypeVar

from game_manager.logic.uid_object import Uid


class StorableObject(Protocol):
    _uid: Uid


T = TypeVar("T", bound=StorableObject)


class StorageManager(ABC):
    def store_object(self, object_to_store: T) -> None:
        data = self._unparse_object(object_to_store)
        self._store_data(object_to_store.__class__.__name__, object_to_store._uid, data)

    def retrieve_object(self, object_type: Type[T], uid: Uid) -> T | None:
        data = self._retrieve_data(object_type.__name__, uid)
        if data is None:
            return None
        stored_object: T = self._parse_object(data)  # type: ignore[assignment]
        stored_object._uid = uid
        return stored_object

    @abstractmethod
    def _unparse_object(self, object_to_unparse: object) -> dict[object, object]: ...

    @abstractmethod
    def _parse_object(self, object_data: dict[object, object]) -> object: ...

    @abstractmethod
    def _store_data(
        self, data_type: str, uid: Uid, data: dict[object, object]
    ) -> None: ...

    @abstractmethod
    def _retrieve_data(
        self, data_type: str, uid: Uid
    ) -> dict[object, object] | None: ...
