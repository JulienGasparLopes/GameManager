from abc import ABC, abstractmethod
from typing import Callable

from vertyces.vertex.vertex2f import Vertex2f


class Window(ABC):
    _width: int
    _height: int

    _on_close_callback: Callable[[], None] | None = None

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    def _on_close(self) -> None:
        if self._on_close_callback:
            self._on_close_callback()

    def set_on_close_callback(self, callback: Callable[[], None]) -> None:
        self._on_close_callback = callback

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def get_dimensions(self) -> Vertex2f:
        return Vertex2f(self._width, self._height)

    @property
    def get_center(self) -> Vertex2f:
        return Vertex2f(self._width / 2, self._height / 2)

    @abstractmethod
    def show(self, set_visible: bool) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    @abstractmethod
    def set_title(self, title: str) -> None: ...
