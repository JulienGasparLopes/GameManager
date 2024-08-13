from abc import ABC, abstractmethod

from vertyces.form.rectangle import Rectangle
from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton


class GraphicalComponent(ABC):
    _bounds: Rectangle

    def __init__(self, position: Vertex2f, dimension: Vertex2f) -> None:
        self._bounds = Rectangle(position, dimension)

    @classmethod
    def from_rectangle(cls, rectangle: Rectangle) -> "GraphicalComponent":
        return cls(rectangle._p1, rectangle._bounds)

    @abstractmethod
    def render(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool: ...
