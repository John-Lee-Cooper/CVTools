import config
from type_ext import Optional, PosixPath


class Group:
    """
    TODO
    """

    def __init__(self, path: Optional[PosixPath] = None):
        self.path = path or config.FAVORITES_PATH
        self.items = set()
        self.read()

    def read(self) -> None:
        try:
            with open(self.path) as fp:
                self.items = [item.strip() for item in fp.readlines()]
        except FileNotFoundError:
            pass
        self.items = set(self.items)

    def write(self) -> None:
        with open(self.path, "w") as fp:
            fp.writelines(f"{item}\n" for item in sorted(self.items))

    def toggle_item(self, item: str) -> None:
        if item in self.items:
            self.items.remove(item)
        else:
            self.items.add(item)
        self.write()
