from abc import ABC, abstractmethod

from vertyces.form.rectangle import Rectangle
from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton


class GraphicalComponent(ABC):
    _visible: bool
    _z_index: int
    _components: list["GraphicalComponent"]

    bounds: Rectangle

    def __init__(
        self,
        position: Vertex2f,
        dimension: Vertex2f,
        z_index: int = 0,
        visible: bool = True,
    ) -> None:
        self.bounds = Rectangle(position, dimension)
        self._visible = visible
        self._z_index = z_index

        self._components = []

    def add_component(self, component: "GraphicalComponent") -> None:
        self._components.append(component)

    def remove_component(self, component: "GraphicalComponent") -> None:
        self._components.remove(component)

    def clear_components(self) -> None:
        self._components.clear()

    @classmethod
    def from_rectangle(cls, rectangle: Rectangle) -> "GraphicalComponent":
        return cls(rectangle._p1, rectangle.dimensions)

    def show(self, visible: bool = True) -> None:
        self._visible = visible

    @property
    def visible(self) -> bool:
        return self._visible

    @property
    def z_index(self) -> int:
        return self._z_index

    def _render(self, renderer: Renderer) -> None:
        if self.visible:
            current_offset = renderer.offset.translated(self.bounds.position)
            current_z_index = renderer.z_index + self.z_index
            renderer.set_offset(current_offset)
            renderer.set_z_index(current_z_index)
            self.render(renderer)
            for component in self._components:
                renderer.set_offset(current_offset)
                renderer.set_z_index(current_z_index)
                component._render(renderer)

    @abstractmethod
    def render(self, renderer: Renderer) -> None: ...

    def _on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        if not self.visible:
            return False

        if not self.bounds.contains(position):
            return False

        position_translated = position.translated(self.bounds.position.inverted())
        start_position_translated = start_position.translated(
            self.bounds.position.inverted()
        )
        for component in self._components:
            if component._on_click(
                button, position_translated, start_position_translated
            ):
                return True

        return self.on_click(button, position_translated, start_position_translated)

    @abstractmethod
    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool: ...
