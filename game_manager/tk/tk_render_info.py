from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import Canvas
from typing import TYPE_CHECKING, Generic, TypeVar

from vertyces.vertex.vertex2f import Vertex2f
from vertyces.vertex.vertex3f import Vertex3f

from game_manager.tk.tk_helpers import v3f_to_hex

if TYPE_CHECKING:
    from game_manager.tk.tk_image import ImageTk

T = TypeVar("T")


@dataclass
class RenderInfoTk(ABC, Generic[T]):
    p1: Vertex2f
    p2: Vertex2f
    content: T
    z_index: int

    @abstractmethod
    def render(self, canvas: Canvas) -> None: ...


class RenderInfoTkLine(RenderInfoTk[Vertex3f]):
    def render(self, canvas: Canvas) -> None:
        canvas.create_line(
            self.p1.x,
            self.p1.y,
            self.p2.x,
            self.p2.y,
            fill=v3f_to_hex(self.content),
            width=2,
        )


class RenderInfoTkRect(RenderInfoTk["ImageTk | Vertex3f"]):
    def render(self, canvas: Canvas) -> None:
        if isinstance(self.content, Vertex3f):
            points = [
                self.p1.x,
                self.p1.y,
                self.p1.x,
                self.p2.y,
                self.p2.x,
                self.p2.y,
                self.p2.x,
                self.p1.y,
            ]
            canvas.create_polygon(points, fill=v3f_to_hex(self.content))
        else:
            self.content.render(canvas, self.p1)


class RenderInfoTkText(RenderInfoTk[Vertex3f]):
    text: str

    def __init__(
        self, p1: Vertex2f, p2: Vertex2f, text: str, color: Vertex3f, z_index: int
    ):
        super().__init__(p1, p2, color, z_index)
        self.text = text

    def render(self, canvas: Canvas) -> None:
        canvas.create_text(
            self.p1.x,
            self.p1.y,
            text=self.text,
            fill=v3f_to_hex(self.content),
            anchor="nw",
        )
