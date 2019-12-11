#!/usr/bin/env python

"""
Display all images in paths
"""


from window import Window
from paths import trash
from type_ext import List, FilePath
from image_paths import imread, paths_to_image_ring
from image_utils import FullScreen
from draw_text import OverlayText
import config
import keys


KEY_HELP = """\
Press
  <SPACE>     to go to the next image.
  <BACKSPACE> to go to the previous image.
  <DELETE>    to delete the current image.
  <ESCAPE>    to exit."""


def main(paths: List[FilePath]) -> None:
    """
    Main routine
      Create window
      Create image Path list
      Display images
      Allow user to step forward and backward through list
    """

    full_screen = FullScreen()
    overlay_text = OverlayText(
        KEY_HELP, "../DroidSansMono.ttf", 18, enabled=False, v_pos="b", h_pos="c"
    )

    with Window() as window:

        image_ring = paths_to_image_ring(paths)
        for image_path in image_ring:

            image = imread(image_path)
            image = full_screen(image)
            image = overlay_text(image)

            key = window.display(image, title=image_path, wait_ms=0)

            if key == keys.SPACE:
                image_ring.next()

            elif key == keys.BACKSPACE:
                image_ring.prev()

            elif key == keys.DELETE:
                trash(image_ring.pop())

            elif key == keys.ENTER:
                window.toggle_fullscreen()
                full_screen.toggle_enabled()

            else:
                overlay_text.toggle_enabled()
                print(key)


if __name__ == "__main__":
    main([config.DATA_PATH / "lena.jpg"])
