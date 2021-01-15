#!/usr/bin/env python

"""
Display all images in paths

TODO:

"""

import sys

from iview import config
from iview import keys as k
from iview.draw_text import OverlayText
from iview.image_ring import ImageRing
from iview.image_utils import FitCanvas, screen_size
from iview.paths import trash
from iview.type_ext import FilePath, List
from iview.window import Window


class App:
    """ TODO """

    def __init__(self, paths: List[FilePath], subdirectories: bool = False):

        screen_w, screen_h = screen_size()
        self.image_source = ImageRing(paths, subdirectories)
        self.part_screen = FitCanvas(
            config.WINDOW_WIDTH, config.WINDOW_HEIGHT, enabled=True
        )
        self.full_screen = FitCanvas(screen_w, screen_h)
        self.overlay_help_text = OverlayText(
            "", config.FONT_PATH, config.FONT_SIZE, enabled=False, v_pos="b", h_pos="c"
        )

        self.keys = k.KeyAssignments()
        self.keys.append(k.SPACE, self.image_source.next, "to go to the next image.")
        self.keys.append(
            k.BACKSPACE, self.image_source.prev, "to go to the previous image."
        )
        self.keys.append(k.DELETE, self.delete, "to delete the current image.")
        self.keys.append(k.ENTER, self.fullscreen, "to toggle full screen.")
        self.keys.append(k.ESCAPE, sys.exit, "to exit.")

        self.keys.default_handler = self.overlay_help_text.toggle_enabled

        self.window = None

    def fullscreen(self) -> None:
        self.window.toggle_fullscreen()
        self.full_screen.toggle_enabled()
        self.part_screen.toggle_enabled()

    def delete(self) -> None:
        """ TODO """
        trash(self.image_source.path)
        self.image_source.pop()

    def run(self) -> None:
        """ TODO """
        self.overlay_help_text.set_text(self.keys.help_string())
        with Window() as self.window:
            while True:
                self.process(self.image_source)

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
        image = self.part_screen(image)
        image = self.overlay_help_text(image)
        key = self.window.display(image, title=image_source.path, wait_ms=0)
        self.keys.handle_keystroke(key)


"""
if __name__ == "__main__":
    App(paths, subdirectories=recursive).run()
"""
