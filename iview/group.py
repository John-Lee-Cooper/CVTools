"""
Image processor for adding images to groups
"""

import cv2 as cv

from iview import config
from iview.image_processor import ImageProcessor
from iview.type_ext import Color, Image, Optional, PosixPath


class Group(ImageProcessor):
    """
    TODO
    """

    def __init__(
        self,
        path: Optional[PosixPath] = None,
        color: Color = (0, 255, 0),
        size: int = 10,
    ):
        super().__init__(True)

        self.path = path or config.FAVORITES_PATH
        print(self.path)
        self.color = color
        self.size = size

        self.item = None
        self._items = set()
        self.read()

    def __call__(self, image, item, *args):
        self.item = item
        if item in self._items:
            self._draw(image, 10, 10)
        return image

    # TODO pass symbol as argument to Group
    def _draw(self, image: Image, x: int, y: int) -> None:
        cv.rectangle(image, (x, y), (x + self.size, y + self.size), self.color, -1)

    def toggle(self) -> None:
        if self.item in self._items:
            self._items.remove(self.item)
        else:
            self._items.add(self.item)
        self.write()

    def read(self) -> None:
        try:
            with open(self.path) as fp:
                self._items = {item.strip() for item in fp.readlines()}
        except FileNotFoundError:
            pass

    def write(self) -> None:
        with open(self.path, "w") as fp:
            fp.writelines(f"{item}\n" for item in sorted(self._items))
