from abc import ABC, abstractmethod

from vertyces.form.rectangle import Rectangle
from vertyces.vertex.vertex2f import Vertex2f

from game_manager.logic.uid_object import UIDObject


class Entity(UIDObject, ABC):
    bounds: Rectangle

    def __init__(self, position: Vertex2f, dimension: Vertex2f) -> None:
        self.bounds = Rectangle(position, dimension)

    @classmethod
    def from_rectangle(cls, rectangle: Rectangle) -> "Entity":
        return cls(rectangle._p1, rectangle._bounds)

    @abstractmethod
    def update(self, delta_time: float) -> None: ...

    @property
    def position(self) -> Vertex2f:
        return self.bounds._p1.clone()
