#!/usr/bin/env python

"""
Display all images in paths

TODO:
  Display filename and size
  Output class
  Play mode
  Transition
"""

import cv2 as cv
from window import Window
from paths import trash
from type_ext import List, FilePath
from image_ring import ImageRing
from image_utils import FullScreen
from draw_text import OverlayText
import config
import keys as k


class App:
    """ TODO """

    def __init__(self, paths: List[FilePath]):

        self.image_source = ImageRing(paths)
        self.full_screen = FullScreen()
        self.overlay_help_text = OverlayText("", config.FONT_PATH, 18, enabled=False, v_pos="b", h_pos="c")

        self.keys = k.KeyAssignments()
        self.keys.append(k.SPACE, self.image_source.next, "to go to the next image."),
        self.keys.append(k.BACKSPACE, self.image_source.prev, "to go to the previous image."),
        self.keys.append(k.DELETE, self.delete, "to delete the current image."),
        self.keys.append(k.ENTER, self.fullscreen, "to toggle full screen."),
        #self.keys.append(k.ESCAPE, exit, "to exit."),

        self.keys.default_handler = self.overlay_help_text.toggle_enabled

        self.window = None

    def fullscreen(self):
        self.window.toggle_fullscreen()
        self.full_screen.toggle_enabled()

    def delete(self):
        trash(self.image_source.path)
        self.image_source.pop()

    def run(self):
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
        image = self.overlay_help_text(image)
        key = self.window.display(image, title=image_source.path, wait_ms=0)
        self.keys.handle_keystroke(key)


if __name__ == "__main__":
    App([config.DATA_PATH / "lena.jpg"]).run()
