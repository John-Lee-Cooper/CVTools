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
import config
import keys


KEY_HELP = """\
Press
  <SPACE>     to go to the next image.
  <BACKSPACE> to go to the previous image.
  <DELETE>    to delete the current image.
  <ESCAPE>    to exit."""

show_help = False


def draw_text(image, string, color=(255, 255, 255), bg_color=None, alpha=0.7):
    h_align = "r"
    v_align = "b"

    ft = cv.freetype.createFreeType2()
    ft.loadFontData(fontFileName='../DroidSansMono.ttf', id=0)
    font_height = 18

    lines = string.split('\n')
    width = int(max([len(line) for line in lines]) * font_height * 0.625)
    height = (len(lines) + 1) * font_height

    h_pad = font_height // 2
    v_pad = font_height // 2
    h, w = image.shape[:2]
    if h_align == "l":
        x = h_pad
    elif h_align == "c":
        x = max(0, (w - width) // 2)
    elif h_align == "r":
        x = max(0, (w - width - h_pad))

    if v_align == "t":
        y = v_pad
    elif v_align == "c":
        y = max(0, (h - height) // 2)
    elif v_align == "b":
        y = max(0, (h - height - v_pad))

    if bg_color:
        overlay = image.copy()
        cv.rectangle(overlay, (x, y), (x + width, y + height), bg_color, -1)
        image[:] = cv.addWeighted(overlay, alpha, image, 1 - alpha, 0)
        x += h_pad
        y += v_pad

    for text in lines:
        y += font_height
        ft.putText(
            img=image,
            text=text,
            org=(x, y),
            fontHeight=font_height,
            color=color,
            thickness=-1,
            line_type=cv.LINE_AA,
            bottomLeftOrigin=True)



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
        draw_text(image, KEY_HELP, color=color, bg_color=average)

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
