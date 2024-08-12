from tkinter import Canvas

from PIL import Image as PilImage
from PIL import ImageTk
from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.renderer import Image


class ImageTk(Image):
    tk_image: ImageTk
    image: ImageTk.PhotoImage | None = None

    def __init__(
        self,
        path: str,
        width: int,
        height: int,
        rotation_angle: int | None = None,
    ) -> None:
        self.tk_image = PilImage.open(path).resize((width, height))
        if rotation_angle:
            self.tk_image = self.tk_image.rotate(rotation_angle)

    def render(self, canvas: Canvas, position: Vertex2f) -> None:
        if not self.image:
            self.image = ImageTk.PhotoImage(self.tk_image)
        canvas.create_image(position.x, position.y, image=self.image, anchor="nw")
