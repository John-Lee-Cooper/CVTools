#!/usr/bin/env python

"""
Display all images in paths

TODO:
  Multiple groups
"""

from type_ext import List, FilePath
import config
from iview import App
from group import Group  # NEW


class IViewSelect(App):
    """ TODO """

    def __init__(self, paths: List[FilePath]):

        super().__init__(paths)
        self.group = Group()
        self.keys.append(
            "1", self.group.toggle, "to toggle membership in Group 1."
        ),  # FIXME: insert before exit

    def process(self, image_source) -> None:
        """
        Main routine
          Create window
          Create image Path list
          Display images
          Allow user to step forward and backward through list
        """
        image = image_source()
        image = self.full_screen(image)
        image = self.overlay_help_text(image)

        image = self.group.mark(image, str(image_source.path))  # NEW

        key = self.window.display(image, title=image_source.path, wait_ms=0)
        self.keys.handle_keystroke(key)


if __name__ == "__main__":
    IViewSelect([config.DATA_PATH / "lena.jpg"]).run()
