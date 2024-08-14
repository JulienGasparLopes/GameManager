from game_manager.logic.uid_object import Uid, UIDObject
from local.test_logic_manager import Entity


class Map(UIDObject):
    _entities: dict[Uid, Entity]

    def __init__(self) -> None:
        self._entities = {}

    def add_entity(self, entity: Entity) -> None:
        self._entities[entity.uid] = entity

    def remove_entity(self, entity: Entity) -> None:
        if entity.uid in self._entities:
            self._entities.pop(entity.uid)
