#!/usr/bin/env python

"""
Display all images in paths
"""
from pathlib import PosixPath
import cv2 as cv
from window import Window
from paths import trash
from image_paths import imread, paths_to_image_ring
from image_utils import resize
from type_ext import List, FilePath
from draw_text import make_font, draw_text
import config
import keys


KEY_HELP = """\
Press
  <SPACE>     to go to the next image.
  <BACKSPACE> to go to the previous image.
  <DELETE>    to delete the current image.
  <ESCAPE>    to exit."""

show_help = False
font = make_font('../DroidSansMono.ttf')


def process(window: Window, image_path: PosixPath, size: int) -> int:
    """
    Read image from image_path,
    resize it so that it is a width or height is size,
    and display it in window.
    Return any key strokes
    """
    image = imread(image_path)

    image = resize(image, width=size, max_size=size)

    if show_help:
        average = cv.mean(image)
        color = [0 if v > 128 else 255 for v in average]
        draw_text(image, KEY_HELP, font, 18, color=color, bg_color=average)

    key = window.display(image, 0)
    return key


def main(paths: List[FilePath], size: int = 2048) -> None:
    """
    Main routine
      Create window
      Create image Path list
      Display images
      Allow user to step forward and backward through list
    """

    with Window() as window:

        image_ring = paths_to_image_ring(paths)
        for image_path in image_ring:

            window.set_title(image_path.name)

            key = process(window, image_path, size)

            if key == keys.SPACE:
                image_ring.next()

            elif key == keys.BACKSPACE:
                image_ring.prev()

            elif key == keys.DELETE:
                trash(image_ring.pop())

            else:
                global show_help
                show_help = not show_help


if __name__ == "__main__":
    main([config.DATA_PATH / "lena.jpg"])
