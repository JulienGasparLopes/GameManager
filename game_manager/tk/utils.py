from typing import Any

from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.renderer import Renderer
from game_manager.graphic.window import Window
from game_manager.io.keyboard import Keyboard
from game_manager.io.mouse import Mouse, MouseButton
from game_manager.tk.tk_renderer import RendererTk
from game_manager.tk.tk_window import WindowTk


def initialize_tk_context() -> tuple[Window, Renderer, Mouse, Keyboard]:
    window = WindowTk(800, 600, "Game")
    renderer = RendererTk(window)
    keyboard = Keyboard()
    mouse = Mouse()

    def _handle_left_mouse_release(event: Any) -> object:
        mouse.__mouse_release__(Vertex2f(event.x, event.y), MouseButton.LEFT)
        return {}

    def _handle_right_mouse_release(event: Any) -> object:
        mouse.__mouse_release__(Vertex2f(event.x, event.y), MouseButton.RIGHT)
        return {}

    def _handle_mouse_move(event: Any) -> object:
        mouse.__mouse_move__(Vertex2f(event.x, event.y))
        return {}

    def _handle_left_mouse_drag_move(event: Any) -> object:
        mouse.__mouse_drag_move__(Vertex2f(event.x, event.y), MouseButton.LEFT)
        return {}

    def _handle_right_mouse_drag_move(event: Any) -> object:
        mouse.__mouse_drag_move__(Vertex2f(event.x, event.y), MouseButton.RIGHT)
        return {}

    window._window.bind("<KeyPress>", keyboard._key_press)
    window._window.bind("<KeyRelease>", keyboard._key_release)

    window._window.bind("<Motion>", _handle_mouse_move)
    window._window.bind("<B1-Motion>", _handle_left_mouse_drag_move)
    window._window.bind("<B2-Motion>", _handle_right_mouse_drag_move)

    window.canvas.bind("<ButtonRelease-1>", _handle_left_mouse_release)
    window.canvas.bind("<ButtonRelease-2>", _handle_right_mouse_release)

    return window, renderer, mouse, keyboard
