#!/usr/bin/env python

"""
https://stackoverflow.com/questions/47726854/error-module-object-has-no-attribute-freetype
"""

import cv2 as cv
import numpy as np
import PILasOPENCV as ImageFont
import PILasOPENCV as Image
import PILasOPENCV as ImageDraw

from image_processor import ImageProcessor
from type_ext import FilePath, Color, Optional
from window import Window
import color


def make_font(font_path: FilePath, font_height: int) -> ImageFont:
    return ImageFont.truetype(str(font_path), font_height)


def put_text(
    image: Image,
    text: str,
    font: ImageFont,
    color_bgr: Color = (0, 0, 0),
    x: int = 0,
    y: int = 0,
):
    w, h, _ = ImageFont.getsize(text, font)
    sub = np.s_[y: y + h, x: x + w, :]

    pil_image = Image.fromarray(image[sub])
    draw = ImageDraw.Draw(pil_image)
    draw.text((0, 0), text, fill=color_bgr, font=font)
    image[sub] = cv.cvtColor(np.array(pil_image.getim()), cv.COLOR_RGB2BGR)


class OverlayText(ImageProcessor):
    def __init__(
        self,
        text: str,
        font_path: FilePath,
        font_size: int,
        color_bgr: Color = None,
        bg_color: Color = None,
        x: int = 0,
        y: int = 0,
        v_pos: str = "",
        h_pos: str = "",
        pad: int = 8,
        enabled: bool = True,
    ):
        super().__init__(enabled)
        self.font = make_font(font_path, font_size)
        self.enabled = enabled
        self.text = text
        self.color_bgr = color_bgr
        self.bg_color = bg_color
        self.x = x
        self.y = y
        self.v_pos = v_pos
        self.h_pos = h_pos
        self.pad = pad

    def set_text(self, text: str) -> None:
        self.text = text

    def draw_text(
        self,
        image: Image,
        color_bgr: Color = (0, 0, 0),
        alpha: float = 0.7,
        bg_color: Optional[Color] = None,
    ) -> None:

        lines = self.text.split("\n")
        sizes = [ImageFont.getsize(line, self.font) for line in lines]
        width = max([size[0] for size in sizes]) + 2 * self.pad
        height = sum([size[1] + size[2] for size in sizes]) + 2 * self.pad
        depth = 3

        h, w = image.shape[:2]
        height = min(h, height)
        width = min(w, width)

        if self.h_pos == "l":
            x = self.pad
        elif self.h_pos == "c":
            x = max(0, (w - width) // 2)
        elif self.h_pos == "r":
            x = max(0, (w - width - 3 * self.pad))
        else:
            x = self.x

        if self.v_pos == "t":
            y = self.pad
        elif self.v_pos == "c":
            y = max(0, (h - height) // 2)
        elif self.v_pos == "b":
            y = max(0, (h - height - 3 * self.pad))
        else:
            y = self.y

        if bg_color:
            sub = np.s_[y:y + height, x:x + width, :]
            overlay = np.full((height, width, depth), bg_color, dtype=np.uint8)
            image[sub] = cv.addWeighted(overlay, alpha, image[sub], 1 - alpha, 0)

        x += self.pad
        y += self.pad

        color_bgr = tuple(color_bgr)
        for text, size in zip(lines, sizes):
            # TODO: Align text
            y += size[2]
            put_text(image, text, self.font, color_bgr, x, y)
            y += size[1]

    def __call__(self, image: Image):
        if not self.enabled:
            return image

        color_bgr = self.color_bgr
        bg_color = self.bg_color

        if bg_color is None:  # FIXME
            average = tuple(image.mean(axis=(0, 1))[:3].astype(np.uint8))
            bg_color = average

        if color_bgr is None:  # FIXME
            color_bgr = [0 if v > 128 else 255 for v in bg_color]

        self.draw_text(image, color_bgr=color_bgr, bg_color=bg_color)

        return image


def main() -> None:
    text = "This is a line.\nIt is only a line.\nThis is a line.\nIt is only a line."
    font_path = "../DroidSansMono.ttf"

    text1 = OverlayText(
        text, font_path, 14, color.white, bg_color=color.grey25, x=10, y=20
    )
    text2 = OverlayText(text, font_path, 18, color.green, v_pos="c", h_pos="c")
    text3 = OverlayText(
        text, font_path, 12, color.red, bg_color=color.blue, v_pos="b", h_pos="r"
    )

    image = np.zeros((640, 480, 3), np.uint8)
    # image = text1(image)
    text1(image)
    image = text2(image)
    image = text3(image)

    with Window() as window:
        window.display(image, wait_ms=0)


if __name__ == "__main__":
    main()
