#!/usr/bin/env python

"""
Display all images in paths
"""

import cv2 as cv
from window import Window
from paths import trash
from type_ext import List, FilePath
from image_paths import imread, paths_to_image_ring
from image_utils import FullScreen
from draw_text import OverlayText
from group import Group
import config
import keys as k


def main(paths: List[FilePath]) -> None:
    """
    Main routine
      Create window
      Create image Path list
      Display images
      Allow user to step forward and backward through list
    """

    image_ring = paths_to_image_ring(paths)

    full_screen = FullScreen()

    group1 = Group()

    keys = k.KeyAssignments()
    keys.append("next", k.SPACE, "to go to the next image."),
    keys.append("previous", k.BACKSPACE, "to go to the previous image."),
    keys.append("delete", k.DELETE, "to delete the current image."),
    keys.append("fullscreen", k.ENTER, "to toggle full screen."),
    keys.append("group1", "1", "to toggle membership in Group 1."),
    keys.append("exit", k.ESCAPE, "to exit."),
    help_string = keys.help_string()

    overlay_help_text = OverlayText(help_string, config.FONT_PATH, 18,
                                    enabled=False, v_pos="b", h_pos="c")

    with Window() as window:

        for image_path in image_ring:
            image = imread(image_path)
            image = full_screen(image)
            image = overlay_help_text(image)

            image_path_abs = str(image_path.absolute())
            if image_path_abs in group1:
                cv.rectangle(image, (10, 10), (20, 20), (0, 255, 0), -1)

            key = window.display(image, title=image_path, wait_ms=0)

            command = keys.command(key)

            if command == "next":
                image_ring.next()

            elif command == "previous":
                image_ring.prev()

            elif command == "delete":
                trash(image_ring.pop())

            elif command == "fullscreen":
                window.toggle_fullscreen()
                full_screen.toggle_enabled()

            elif command == "group1":
                group1.toggle_item(image_path_abs)

            else:
                overlay_help_text.toggle_enabled()


if __name__ == "__main__":
    main([config.DATA_PATH / "lena.jpg"])

