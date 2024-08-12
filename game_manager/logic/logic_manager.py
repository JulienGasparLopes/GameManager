from abc import ABC, abstractmethod
import threading
from time import time_ns


class LogicManager(ABC):
    _update_per_second: int = 50
    _running: bool = True
    _last_update_ns: float

    _thread: threading.Thread

    def __init__(self):
        pass

    def set_update_per_second(self, ups: int) -> None:
        self._update_per_second = ups

    def start(self) -> None:
        _thread = threading.Thread(target=self._internal_loop)
        _thread.start()

    def stop(self) -> None:
        self._running = False

    def _internal_loop(self) -> None:
        _last_update_ns = time_ns()
        while self._running:
            current_time = time_ns()
            delta_ns = current_time - _last_update_ns
            if delta_ns > (1_000_000_000 / self._update_per_second):
                self.update(delta_ns)
                _last_update_ns = current_time

        self.dispose()

    @abstractmethod
    def update(self, delta_ns: float) -> None:
        pass

    @abstractmethod
    def dispose(self) -> None:
        pass
