import uuid
from abc import ABC
from typing import TypeAlias

Uid: TypeAlias = uuid.UUID
"""Unique ID of an entity_object"""


class UIDObject(ABC):
    _uid: Uid

    @property
    def uid(self) -> Uid:
        if not hasattr(self, "_uid"):
            self._uid = uuid.uuid4()
        return self._uid
