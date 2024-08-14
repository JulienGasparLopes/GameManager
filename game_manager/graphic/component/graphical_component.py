from abc import ABC, abstractmethod

from vertyces.form.rectangle import Rectangle
from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton


class GraphicalComponent(ABC):
    _visible: bool

    bounds: Rectangle

    def __init__(
        self, position: Vertex2f, dimension: Vertex2f, visible: bool = True
    ) -> None:
        self.bounds = Rectangle(position, dimension)
        self._visible = visible

    @classmethod
    def from_rectangle(cls, rectangle: Rectangle) -> "GraphicalComponent":
        return cls(rectangle._p1, rectangle._bounds)

    def show(self, visible: bool = True) -> None:
        self._visible = visible

    @property
    def visible(self) -> bool:
        return self._visible

    @abstractmethod
    def render(self, renderer: Renderer) -> None: ...

    @abstractmethod
    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool: ...
