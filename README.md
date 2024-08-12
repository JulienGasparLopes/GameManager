# Game Manager

A Python package to help developing game.

It's purpose is to provide a bunch of helpers and abstractions to focus on game development.

# Graphic vs Logic

Graphic and Logic are separated for a better code responsibility separation.

It also allows to better divide UI from pure logic

These are the main concepts :

- Game Logic
- Graphics (window, rendering ...)
- Input/Output (mouse, keyboard, sound)
- WIP - Messaging bus (for communication between UI and logic)

# Implementations

This package proposes some specific and utsable implementation using graphic libraries.

Currently, only TKinter is supported.

We aim to implement OpenGL/Vulkan.

# TKinter example

Here is a minimum example using TKinter implementation (draws a red rectangle) :

```python
from vertyces.vertex.vertex2f import Vertex2f
from vertyces.vertex.vertex3f import Vertex3f

from game_manager.graphic.graphic_manager import GraphicManager
from game_manager.graphic.renderer import Renderer
from game_manager.logic.logic_manager import LogicManager
from game_manager.tk.utils import initialize_tk_context


class TestLogicManager(LogicManager):
    def __init__(self):
        super().__init__()

    def update(self, delta_ns: float) -> None: ...

    def dispose(self) -> None:
        print("Disposing Logic Manager")


class TestGraphicManager(GraphicManager):
    def render(self, delta_ns: float, renderer: Renderer) -> None:
        renderer.draw_rect(Vertex2f(0, 0), Vertex2f(100, 100), Vertex3f(255, 0, 0))

    def dispose(self) -> None:
        print("Disposing Graphic Manager")


def main():
    logic_manager = TestLogicManager()
    window, renderer, mouse, keyboard = initialize_tk_context()
    graphic_manager = TestGraphicManager(renderer)

    print("Starting logic manager thread")
    logic_manager.start()

    print("Starting graphic manager thread")
    graphic_manager.start()


if __name__ == "__main__":
    main()
```
