import threading
import time
from abc import ABC, abstractmethod
from time import time_ns
from typing import Generic, TypeVar

from game_manager.logic.map.map import Map
from game_manager.logic.uid_object import Uid
from game_manager.messaging.message_client import MessageClient, MessageManagerType

TMap = TypeVar("TMap", bound=Map)


class BaseLogicManager(
    MessageClient[MessageManagerType], Generic[MessageManagerType, TMap], ABC
):
    _current_ups_counter: int = 0
    _last_ups_count_time: float = 0
    _current_ups: int = 0

    _thread: threading.Thread
    _running: bool = True
    _is_disposed: bool = False

    _update_per_second: int = 50
    _last_update_ns: float

    _maps: dict[Uid, TMap]

    def __init__(self) -> None:
        self._maps = {}

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
                for map in self._maps.values():
                    map._update(delta_ns)
                _last_update_ns = current_time

                self._current_ups_counter += 1
                current_time = time_ns()
                if current_time - self._last_ups_count_time > 1_000_000_000:
                    self._current_ups = self._current_ups_counter
                    self._current_ups_counter = 0
                    self._last_ups_count_time = current_time
            else:
                time.sleep(
                    (((1_000_000_000 / self._update_per_second) - delta_ns) * 0.95)
                    / 1_000_000_000
                )

        self.dispose()
        self._is_disposed = True

    def add_map(self, map: TMap) -> None:
        self._maps[map.uid] = map

    def remove_map(self, map_uid: Uid) -> TMap:
        return self._maps.pop(map_uid)

    def get_map(self, map_uid: Uid) -> TMap | None:
        return self._maps[map_uid]

    @property
    def is_disposed(self) -> bool:
        return self._is_disposed

    @property
    def ups(self) -> int:
        return self._current_ups

    @abstractmethod
    def update(self, delta_ns: float) -> None: ...

    @abstractmethod
    def dispose(self) -> None: ...
