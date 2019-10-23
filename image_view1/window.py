#!/usr/bin/env python

from sys import platform
from pathlib import Path, PosixPath

import cv2 as cv
from paths import script_name
from type_ext import FilePath, Image, Optional
import ui

ESC_KEY = 27
SPACE = 32
BACKSPACE = 8
DELETE_KEY = -1

if platform in ("linux", "linux2"):
    DELETE_KEY = 255

elif platform == "darwin":  # OS X
    DELETE_KEY = 117

# elif platform == "win32":  # Windows...

else:
    ui.warning(f"Window does not fully support {platform}")


class Window:
    def __init__(
        self, name="", flag=cv.WINDOW_GUI_NORMAL, image=None, include_script_name=True
    ):

        name = self.make_name(name)
        if not name or include_script_name:
            name = f"{script_name()} {name}"
        self.name = name
        cv.namedWindow(self.name, flag)
        cv.setWindowProperty(self.name, cv.WND_PROP_AUTOSIZE, 1.0)

        self.mouse_down = False
        self.r_mouse_down = False
        self.mouse_at = self.mouse_down_at = None
        self.r_mouse_at = self.r_mouse_down_at = None
        self.mouse_down_with = None
        self.r_mouse_down_with = None

        if image is not None:
            self.display(image)

    def destroy(self):
        cv.destroyWindow(self.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    @staticmethod
    def make_name(name: FilePath) -> Optional[PosixPath]:
        """ If name is a PosixPath, return its name, else assume its a string and return it """
        return Path(name).name if type(name) is PosixPath else name

    def set_title(self, title: FilePath, include_script_name: bool = True) -> None:
        title = self.make_name(title)
        if include_script_name:
            title = f"{script_name()} {title}"
        cv.setWindowTitle(self.name, title)

    def display(
        self, image: Image, wait_ms: int = None, title: Optional[FilePath] = None
    ) -> int:
        """
        Display image in window

        By default it will wait for ever for a key stroke
        If wait is None, it will not wait at all.
        """
        if title:
            self.set_title(title)

        cv.imshow(self.name, image)

        if wait_ms is None:
            return -1  # None

        return self.wait(wait_ms)

    @staticmethod
    def wait(wait_ms: int = 0) -> int:
        # TODO: Pass in keyhandler

        key_code = cv.waitKey(int(wait_ms))
        # key_code = cv.waitKeyEx(int(wait_ms))
        # if key_code != -1: info(key_code)

        if key_code & 0xFF == ESC_KEY:
            exit(0)

        return key_code

    def move(self, x: int, y: int) -> None:
        cv.moveWindow(self.name, x, y)
