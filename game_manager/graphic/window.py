from abc import ABC, abstractmethod
from game_manager.graphic.renderer import Renderer


class Window(ABC):
    def __init__(self, width: int, height: int, title: str): ...

    @abstractmethod
    def show(self, set_visible: bool) -> None: ...
