import threading
import time
from abc import ABC, abstractmethod
from time import time_ns
from typing import Generic

from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.menu.menu import Menu
from game_manager.graphic.renderer import Renderer
from game_manager.graphic.window import Window
from game_manager.io.keyboard import Keyboard
from game_manager.io.mouse import Mouse, MouseButton
from game_manager.messaging.message_client import MessageClient, MessageManagerType


class GraphicManager(
    MessageClient[MessageManagerType], Generic[MessageManagerType], ABC
):
    _current_fps_counter: int = 0
    _last_fps_count_time: float = 0
    _current_fps: int = 0

    _frame_per_second: int = 50
    _running: bool = True
    _is_disposed: bool = False

    _window: Window
    _renderer: Renderer
    _keyboard: Keyboard
    _mouse: Mouse

    _current_menu: Menu | None = None

    def __init__(
        self, window: Window, renderer: Renderer, keyboard: Keyboard, mouse: Mouse
    ) -> None:
        self._window = window
        self._renderer = renderer
        self._keyboard = keyboard
        self._mouse = mouse
        mouse.set_button_release_callback(self._on_click)

    def start(self, main_thread: bool = True) -> None:
        if main_thread:
            self._last_fps_count_time = time_ns()
            self._internal_loop()
        else:
            _thread = threading.Thread(target=self._internal_loop)
            _thread.start()

    def stop(self) -> None:
        self._running = False

    def set_current_menu(self, menu: Menu | None) -> None:
        self._current_menu = menu

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

    @abstractmethod
    def dispose(self) -> None: ...

    def _internal_loop(self) -> None:
        _last_update_ns = time_ns()
        while self._running:
            current_time = time_ns()
            delta_ns = current_time - _last_update_ns
            if delta_ns > (1_000_000_000 / self._frame_per_second):
                self._renderer.render_start()
                self._render(delta_ns, self._renderer)
                self._renderer.render_end()
                _last_update_ns = current_time

                self._current_fps_counter += 1
                current_time = time_ns()
                if current_time - self._last_fps_count_time > 1_000_000_000:
                    self._current_fps = self._current_fps_counter
                    self._current_fps_counter = 0
                    self._last_fps_count_time = current_time
            else:
                time.sleep(
                    (((1_000_000_000 / self._frame_per_second) - delta_ns) * 0.95)
                    / 1_000_000_000
                )

        self.dispose()
        self._is_disposed = True

    def _on_click(
        self, button: MouseButton, position: Vertex2f, start_position: Vertex2f
    ) -> None:
        if self._current_menu:
            self._current_menu._on_click(button, position, start_position)

    def _render(self, delta_ns: float, renderer: Renderer) -> None:
        if self._current_menu:
            self._current_menu._render(delta_ns, renderer)

    @property
    def fps(self) -> int:
        return self._current_fps
