#!/usr/bin/env python

""" Display all images in paths """

from open_cv import imread, resize, DATA_PATH
from open_cv.lib.window import Window, SPACE, BACKSPACE
from open_cv.lib.paths import path_to_image_paths
from open_cv import error


def main(path, max_size: int = 640) -> None:
    """
    Main routine
      Create window
      Create image Path list
      Display images
      Allow user to step forward and backward through list
    """

    image_paths = path_to_image_paths(path)
    if not image_paths:
        error(f"No images in {path}")

    window = Window()

    while True:
        image_path = image_paths.value()
        image = imread(image_path)
        image = resize(image, max_size=max_size)

        window.set_title(image_path.name)
        key = window.display(image, 0)
        if key == SPACE:
            image_paths.next()
        elif key == BACKSPACE:
            image_paths.prev()


if __name__ == "__main__":
    main(DATA_PATH / "lena.jpg")
