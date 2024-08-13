import threading
from abc import ABC, abstractmethod
from time import time_ns
from typing import Generic

from game_manager.graphic.renderer import Renderer
from game_manager.graphic.window import Window
from game_manager.io.keyboard import Keyboard
from game_manager.io.mouse import Mouse
from game_manager.messaging.message_client import MessageClient, MessageManagerType


class GraphicManager(
    ABC, MessageClient[MessageManagerType], Generic[MessageManagerType]
):
    _frame_per_second: int = 30
    _running: bool = True
    _is_disposed: bool = False

    _window: Window
    _renderer: Renderer
    _keyboard: Keyboard
    _mouse: Mouse

    def __init__(
        self, window: Window, renderer: Renderer, keyboard: Keyboard, mouse: Mouse
    ) -> None:
        self._window = window
        self._renderer = renderer
        self._keyboard = keyboard
        self._mouse = mouse

    def start(self, main_thread: bool = True) -> None:
        if main_thread:
            self._internal_loop()
        else:
            _thread = threading.Thread(target=self._internal_loop)
            _thread.start()

    def stop(self) -> None:
        self._running = False

    def _internal_loop(self) -> None:
        _last_update_ns = time_ns()
        while self._running:
            current_time = time_ns()
            delta_ns = current_time - _last_update_ns
            if delta_ns > (1_000_000_000 / self._frame_per_second):
                self._renderer.render_start()
                self.render(delta_ns, self._renderer)
                self._renderer.render_end()
                _last_update_ns = current_time

        self.dispose()
        self._is_disposed = True

    @abstractmethod
    def render(self, delta_ns: float, renderer: Renderer) -> None: ...

    @abstractmethod
    def dispose(self) -> None: ...

    @property
    def is_disposed(self) -> bool:
        return self._is_disposed

    @property
    def window(self) -> Window:
        return self._window

    @property
    def keyboard(self) -> Keyboard:
        return self._keyboard

    @property
    def mouse(self) -> Mouse:
        return self._mouse
