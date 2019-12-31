import config
from type_ext import Optional, PosixPath


class Group:
    """
    TODO
    """

    def __init__(self, path: Optional[PosixPath] = None):
        self.path = path or config.FAVORITES_PATH
        self._items = set()
        self.read()

    def __contains__(self, item):
        return item in self._items

    def read(self) -> None:
        try:
            with open(self.path) as fp:
                self._items = set(item.strip() for item in fp.readlines())
        except FileNotFoundError:
            pass

    def write(self) -> None:
        with open(self.path, "w") as fp:
            fp.writelines(f"{item}\n" for item in sorted(self._items))

    def toggle_item(self, item: str) -> None:
        if item in self._items:
            self._items.remove(item)
        else:
            self._items.add(item)
        self.write()
