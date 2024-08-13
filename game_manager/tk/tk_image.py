from tkinter import Canvas

from PIL import Image as PilImage
from PIL import ImageTk as PILImageTk
from vertyces.vertex.vertex2f import Vertex2f

from game_manager.graphic.renderer import Image


class ImageTk(Image):
    tk_image: PilImage.Image
    image: PILImageTk.PhotoImage | None = None

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
            self.image = PILImageTk.PhotoImage(self.tk_image)
        canvas.create_image(position.x, position.y, image=self.image, anchor="nw")
