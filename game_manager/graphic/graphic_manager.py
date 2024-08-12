import threading
from abc import abstractmethod
from time import time_ns

from game_manager.graphic.renderer import Renderer


class GraphicManager:
    _frame_per_second: int = 30
    _running: bool = True

    _renderer: Renderer

    def __init__(self, renderer: Renderer) -> None:
        self._renderer = renderer

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

    @abstractmethod
    def render(self, delta_ns: float, renderer: Renderer) -> None: ...

    @abstractmethod
    def dispose(self) -> None: ...
