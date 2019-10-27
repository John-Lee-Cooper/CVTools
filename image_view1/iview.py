#!/usr/bin/env python

"""
Display all images in paths
"""
from pathlib import PosixPath
from window import Window
from paths import trash
from image_paths import imread, paths_to_image_ring
from image_utils import resize
from type_ext import List, FilePath
import config


def process(window: Window, image_path: PosixPath, size: int) -> int:
    """
    Read image from image_path,
    resize it so that it is a width or height is size,
    and display it in window.
    Return any key strokes
    """
    image = imread(image_path)

    image = resize(image, width=size, max_size=size)

    key = window.display(image, 0)
    return key


def main(paths: List[FilePath], size: int = 640) -> None:
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

            if key == config.NEXT_KEY:
                image_ring.forward()

            elif key == config.PREV_KEY:
                image_ring.backward()

            elif key in config.DELETE_KEYS:
                trash(image_ring.pop())

            else:
                print(key)


if __name__ == "__main__":
    main([config.DATA_PATH / "lena.jpg"])
