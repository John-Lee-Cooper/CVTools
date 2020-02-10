import config
from type_ext import Optional, PosixPath
import cv2 as cv


class Group:
    """
    TODO
    """

    def __init__(
        self,
        path: Optional[PosixPath] = None,
        color=(0, 255, 0),
        size=10,
    ):
        self.path = path or config.FAVORITES_PATH
        self.color = color
        self.size = size

        self.item = None
        self._items = set()
        self.read()

    # def __contains__(self, item):
    #     return item in self._items

    def mark(self, image, item):
        self.item = item
        if item in self._items:
            self.draw(image, 10, 10)
        return image

    # TODO pass symbol as argument to Group
    def draw(self, image, x, y):
        cv.rectangle(image, (x, y), (x + self.size, y + self.size), self.color, -1)

    def toggle(self):
        if self.item in self._items:
            self._items.remove(self.item)
        else:
            self._items.add(self.item)
        self.write()

    def read(self) -> None:
        try:
            with open(self.path) as fp:
                self._items = set(item.strip() for item in fp.readlines())
        except FileNotFoundError:
            pass

    def write(self) -> None:
        with open(self.path, "w") as fp:
            fp.writelines(f"{item}\n" for item in sorted(self._items))
