#!/usr/bin/env python

import cv2 as cv
import numpy as np
from window import Window


def make_font(font_path):
    font = cv.freetype.createFreeType2()
    font.loadFontData(fontFileName=font_path, id=0)
    return font


def draw_text(
    image, string,
    font, font_height,
    color=(0, 0, 0), bg_color=None, alpha=0.7,
    x=0, y=0, v_align="t", h_align = "l",
):
    lines = string.split('\n')
    width = int(max([len(line) for line in lines]) * font_height * 0.65)
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
        font.putText(
            img=image,
            text=text,
            org=(x, y),
            fontHeight=font_height,
            color=color,
            thickness=-1,
            line_type=cv.LINE_AA,
            bottomLeftOrigin=True)


def main() -> None:
    image = np.zeros((640, 480, 3), np.uint8)
    string = "This is a line\nIt is only a line"
    font = make_font('../DroidSansMono.ttf')

    color1 = (255, 255, 255)
    color2 = (0, 255, 0)
    color3 = (0, 0, 255)
    bg_color1 = (32, 32, 32)
    bg_color3 = (64, 0, 0)

    draw_text(image, string, font, 14, color1, bg_color1)
    draw_text(image, string, font, 18, color2, v_align='c', h_align='c')
    draw_text(image, string, font, 12, color3, bg_color3, v_align='b', h_align='r')

    with Window() as window:
        window.display(image, wait_ms=0)


if __name__ == "__main__":
    main()
