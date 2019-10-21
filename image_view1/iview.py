#!/usr/bin/env python

""" Display all images in paths """

from window import Window, SPACE, BACKSPACE, DELETE_KEY
from paths import trash
from image_paths import imread, paths_to_image_ring
from image_utils import resize
import config


def process(window, image_path, size):
    image = imread(image_path)

    image = resize(image, width=size, max_size=size)

    key = window.display(image, 0)
    return key


def main(paths, size: int = 640) -> None:
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

            if key == SPACE:
                image_ring.next()

            elif key == BACKSPACE:
                image_ring.prev()

            elif key == DELETE_KEY:
                trash(image_path)
                image_ring.pop()

            else:
                print(key)


if __name__ == "__main__":
    main([config.data_path / "lena.jpg"])
