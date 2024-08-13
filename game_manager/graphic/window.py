from abc import ABC, abstractmethod
from typing import Callable


class Window(ABC):
    _on_close_callback: Callable[[], None] | None = None

    def __init__(self, width: int, height: int, title: str): ...

    @abstractmethod
    def show(self, set_visible: bool) -> None: ...

    @abstractmethod
    def close(self) -> None: ...

    def set_on_close_callback(self, callback: Callable[[], None]) -> None:
        self._on_close_callback = callback

    def _on_close(self) -> None:
        if self._on_close_callback:
            self._on_close_callback()
