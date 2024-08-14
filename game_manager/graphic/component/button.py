from abc import ABC, abstractmethod
from typing import Callable

from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.component.graphical_component import GraphicalComponent
from game_manager.graphic.renderer import Renderer
from game_manager.io.mouse import MouseButton

ButtonActionCallback = Callable[[], None]


class Button(GraphicalComponent, ABC):
    _action_callback: ButtonActionCallback

    def __init__(
        self,
        position: Vertex2f,
        dimension: Vertex2f,
        action_callback: ButtonActionCallback,
    ) -> None:
        super().__init__(position, dimension)
        self._action_callback = action_callback

    def on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> bool:
        if (
            button == MouseButton.LEFT
            and self.bounds.contains(position)
            and self.bounds.contains(start_position)
        ):
            self._action_callback()
            return True
        return False

    @abstractmethod
    def render(self, renderer: Renderer) -> None: ...
