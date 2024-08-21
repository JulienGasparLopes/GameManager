from abc import ABC, abstractmethod

from vertyces.form.rectangle import Rectangle
from vertyces.vertex.vertex2f import Vertex2f

from game_manager.logic.entity.entity import Entity
from game_manager.logic.entity.entity_moveable import EntityMoveable
from game_manager.logic.uid_object import Uid, UIDObject


class Map(UIDObject, ABC):
    _entities: dict[Uid, Entity]

    def __init__(self) -> None:
        self._entities = {}

    def add_entity(self, entity: Entity) -> None:
        self._entities[entity.uid] = entity

    def remove_entity(self, entity_uid: Uid) -> None:
        if entity_uid in self._entities:
            self._entities.pop(entity_uid)

    def get_entity(self, uid: Uid) -> Entity | None:
        return self._entities.get(uid)

    def _update(self, delta_time: float) -> None:
        self.update(delta_time)
        for entity in self._entities.values():
            if isinstance(entity, EntityMoveable):
                new_position = self._calculate_entity_new_position(delta_time, entity)
                if new_position:
                    entity.bounds = Rectangle(new_position, entity.bounds.dimensions)
            entity.update(delta_time)

    def _calculate_entity_new_position(
        self, delta_ns: float, entity: EntityMoveable
    ) -> Vertex2f | None:
        delta_position = entity.direction.multiplied(
            entity.speed * delta_ns / 10_000_000
        )
        possible_new_positions = [
            entity.bounds._p1.translated(delta_position),
            entity.bounds._p1.translated(Vertex2f(delta_position.x, 0)),
            entity.bounds._p1.translated(Vertex2f(0, delta_position.y)),
        ]
        new_position: Vertex2f | None = None
        for possible_new_position in possible_new_positions:
            new_position = possible_new_position
            new_bounds = Rectangle(possible_new_position, entity.bounds.dimensions)
            for other_entity in self._entities.values():
                if other_entity == entity:
                    continue
                if other_entity.bounds.collides(new_bounds):
                    new_position = None
                    break
            if new_position:
                break

        return new_position

    @abstractmethod
    def update(self, delta_time: float) -> None: ...
