from game_manager.graphic.renderer import Image, Renderer
from game_manager.tk.tk_render_info import (
    RenderInfoTk,
    RenderInfoTkLine,
    RenderInfoTkRect,
    RenderInfoTkText,
)
from vertyces.vertex.vertex2f import Vertex2f
from vertyces.vertex.vertex3f import Vertex3f

from game_manager.tk.tk_window import WindowTk


class RendererTk(Renderer):
    _render_info_list: list[RenderInfoTk] = []

    _window_tk: WindowTk

    def __init__(self, window_tk: WindowTk) -> None:
        self._window_tk = window_tk

    def render_start(self) -> None:
        self._render_info_list = []
        self._window_tk._window.update_idletasks()
        self._window_tk._window.update()

    def render_end(self) -> None:
        self._render_info_list.sort(key=lambda ri: ri.z_index)
        for ri in self._render_info_list:
            ri.render(self._window_tk.canvas)

    def draw_line(
        self, p1: Vertex2f, p2: Vertex2f, content: Vertex3f, z_index: int = 0
    ) -> None:
        p1_t = p1.translated(self.offset)
        p2_t = p2.translated(self.offset)
        self._render_info_list.append(
            RenderInfoTkLine(p1_t, p2_t, content, self.z_index + z_index)
        )

    def draw_rect(
        self, p1: Vertex2f, p2: Vertex2f, content: Vertex3f | Image, z_index: int = 0
    ) -> None:
        p1_t = p1.translated(self.offset)
        p2_t = p2.translated(self.offset)
        self._render_info_list.append(
            RenderInfoTkRect(p1_t, p2_t, content, self.z_index + z_index)
        )

    def draw_text(
        self, p: Vertex2f, text: str, color: Vertex3f, z_index: int = 0
    ) -> None:
        p_t = p.translated(self.offset)
        self._render_info_list.append(
            RenderInfoTkText(p_t, p_t, text, color, self.z_index + z_index)
        )
