from typing import Generic, TypeVar

from game_manager.messaging.message_manager import MessageManagerProtocol

MessageManagerType = TypeVar("MessageManagerType", bound=MessageManagerProtocol)


class MessageClient(Generic[MessageManagerType]):
    _message_manager: MessageManagerType | None = None

    @property
    def message_manager(self) -> MessageManagerType:
        if self._message_manager is None:
            raise ValueError("MessageManager is not set")
        return self._message_manager

    def set_message_manager(self, message_manager: MessageManagerType) -> None:
        self._message_manager = message_manager
