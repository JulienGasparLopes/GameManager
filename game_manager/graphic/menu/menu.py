from abc import ABC, abstractmethod

from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton


class Menu(ABC):

    _components: list[GraphicalComponent]

    def __init__(self) -> None:
        self._components = []

    def add_component(self, component: GraphicalComponent) -> None:
        self._components.append(component)

    def remove_component(self, component: GraphicalComponent) -> None:
        self._components.remove(component)

    def _on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> None:
        # TODO: sort component by z-index
        for component in self._components:
            if component.on_click(button, position, start_position):
                break
        self.on_click(button, position, start_position)

    def _render(self, delta_ns: float, renderer: Renderer) -> None:
        for component in self._components:
            if component.visible:
                component.render(renderer)
        self.render(delta_ns, renderer)

    @abstractmethod
    def render(self, delta_ns: float, renderer: Renderer) -> None: ...

    @abstractmethod
    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> None: ...
