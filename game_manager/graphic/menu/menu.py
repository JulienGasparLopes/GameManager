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
        # TODO: sort component by z-index ?
        for component in self._components:
            position_translated = position.translated(
                component.bounds.position.inverted()
            )
            start_position_translated = start_position.translated(
                component.bounds.position.inverted()
            )
            if component._on_click(
                button, position_translated, start_position_translated
            ):
                return
        self.on_click(button, position, start_position)

    def _render(self, delta_ns: float, renderer: Renderer) -> None:
        renderer.set_offset(Vertex2f(0, 0))
        renderer.set_z_index(0)
        self.render(delta_ns, renderer)

        for component in self._components:
            renderer.set_offset(Vertex2f(0, 0))
            renderer.set_z_index(0)
            component._render(renderer)

    @abstractmethod
    def render(self, delta_ns: float, renderer: Renderer) -> None: ...

    @abstractmethod
    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> None: ...
