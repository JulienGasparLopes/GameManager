import tkinter as tk

from vertyces.vertex.vertex3f import Vertex3f

from game_manager.graphic.window import Window
from game_manager.tk.tk_helpers import v3f_to_hex


class WindowTk(Window):
    _window: tk.Tk

    def __init__(self, width: int, height: int, title: str) -> None:
        self._window = tk.Tk()
        self.set_title(title)

        self.canvas = tk.Canvas(
            self._window, width=width, height=height, highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        self._window.protocol("WM_DELETE_WINDOW", self._on_close)

    def set_background_color(self, color: Vertex3f) -> None:
        self._window.configure(bg=v3f_to_hex(color))

    def show(self, set_visible: bool) -> None:
        if set_visible:
            self._window.deiconify()
        else:
            self._window.withdraw()

    def close(self) -> None:
        self._window.destroy()
        self._window.update()
        print("Window closed")

    def set_title(self, title: str) -> None:
        self._window.title(title)
