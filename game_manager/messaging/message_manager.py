from abc import ABC
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from game_manager.messaging.message_client import MessageClient


class MessageManagerProtocol(Protocol): ...


class MessageManager(ABC):
    def __init__(
        self,
        message_client_left: "MessageClient",  # type: ignore [type-arg]
        message_client_right: "MessageClient",  # type: ignore [type-arg]
    ) -> None:
        message_client_left.set_message_manager(self)
        message_client_right.set_message_manager(self)
