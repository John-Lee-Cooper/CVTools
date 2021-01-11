#!/usr/bin/env python

"""
Extension to iview to allow selecting of images.

TODO:
  Multiple groups
  Save groups in json.  Config?
"""

from iview import config
from iview.group import Group
from iview.iview import App
from iview.type_ext import FilePath, List


class IViewSelect(App):
    """ TODO """

    def __init__(self, paths: List[FilePath]):

        super().__init__(paths)
        self.group = Group()
        # FIXME: insert before exit
        self.keys.append("1", self.group.toggle, "to toggle membership in Group 1.")

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

        image = self.group(image, str(image_source.path))  # NEW

        key = self.window.display(image, title=image_source.path, wait_ms=0)
        self.keys.handle_keystroke(key)


if __name__ == "__main__":
    IViewSelect([config.DATA_PATH / "lena.jpg"]).run()
