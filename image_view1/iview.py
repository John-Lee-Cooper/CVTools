#!/usr/bin/env python

"""
Display all images in paths


TODO:
  Display filename and size
  Multiple groups
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
from group import Group
import config
import keys as k


class App:
    """ TODO """

    def __init__(self, paths: List[FilePath]):

        self.image_source = ImageRing(paths)
        self.full_screen = FullScreen()
        self.group = Group()

        self.keys = k.KeyAssignments()
        self.keys.append("next", k.SPACE, "to go to the next image."),
        self.keys.append("previous", k.BACKSPACE, "to go to the previous image."),
        self.keys.append("delete", k.DELETE, "to delete the current image."),
        self.keys.append("fullscreen", k.ENTER, "to toggle full screen."),
        self.keys.append("group1", "1", "to toggle membership in Group 1."),
        self.keys.append("exit", k.ESCAPE, "to exit."),

        self.overlay_help_text = OverlayText(
            self.keys.help_string(), config.FONT_PATH, 18,
            enabled=False, v_pos="b", h_pos="c")

        with Window() as self.window:
            while True:
                self.process(self.image_source)

    def handle_keystroke(self, key):
        command = self.keys.command(key)

        if command == "next":
            self.image_source.next()

        elif command == "previous":
            self.image_source.prev()

        elif command == "delete":
            trash(self.image_source.image_path)
            self.image_source.pop()

        elif command == "fullscreen":
            self.window.toggle_fullscreen()
            self.full_screen.toggle_enabled()

        elif command == "group1":
            self.group.toggle()

        else:
            self.overlay_help_text.toggle_enabled()

    def process(self, image_source) -> None:
        """
        Main routine
          Create window
          Create image Path list
          Display images
          Allow user to step forward and backward through list
        """
        image_path, image = image_source()
        image = self.full_screen(image)
        image = self.overlay_help_text(image)
        image = self.group.mark(image, str(image_path))  # str(image_path.absolute()))
        # print(f"{image.shape[1]} x {image.shape[0]} {image_path.name}")
        key = self.window.display(image, title=image_path, wait_ms=0)
        self.handle_keystroke(key)


if __name__ == "__main__":
    App([config.DATA_PATH / "lena.jpg"])
