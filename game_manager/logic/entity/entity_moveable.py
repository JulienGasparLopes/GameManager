from abc import ABC, abstractmethod

from vertyces.vertex.vertex2f import Vertex2f

from game_manager.logic.entity.entity import Entity


class EntityMoveable(Entity, ABC):
    speed: float
    direction: Vertex2f

    def __init__(self, position: Vertex2f, dimension: Vertex2f) -> None:
        super().__init__(position, dimension)
        self.speed = 1
        self.direction = Vertex2f(0, 0)

    @abstractmethod
    def update(self, delta_time: float) -> None: ...
