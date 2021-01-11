#!/usr/bin/env python

"""
OpenCV Window class
"""

import sys
from pathlib import Path, PosixPath

import cv2 as cv

from iview import keys
from iview.paths import script_name
from iview.type_ext import FilePath, Image, Optional


class Window:
    """ Class wrapper for open_cv window functions """

    def __init__(
        self,
        name="",
        flag=cv.WINDOW_GUI_NORMAL,
        image=None,
        include_script_name=True
        # self, name="", flag = cv.WINDOW_NORMAL, image=None, include_script_name=True
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
        """ Remove the window """
        cv.destroyWindow(self.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.destroy()

    @staticmethod
    def make_name(name: FilePath) -> Optional[PosixPath]:
        """
        If name is a PosixPath, return its name, else assume its a string and return it
        """
        return Path(name).name if isinstance(name, PosixPath) else name

    def set_title(self, title: FilePath, include_script_name: bool = True) -> None:
        """ Set the title of the window """
        title = self.make_name(title)
        if include_script_name:
            title = f"{script_name()} {title}"
        cv.setWindowTitle(self.name, title)

    def move(self, x: int, y: int) -> None:
        """ Move the window to x, y """
        cv.moveWindow(self.name, x, y)

    def rect(self):
        """ return x, y, w, h """
        return cv.getWindowImageRect(self.name)

    def toggle_fullscreen(self):
        value = cv.getWindowProperty(self.name, cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty(self.name, cv.WND_PROP_FULLSCREEN, float(not value))

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
        """ Wait for a keystroke or until wait_ms milliseconds pass """

        key_code = cv.waitKey(int(wait_ms))
        # = cv.waitKeyEx(int(wait_ms))

        if key_code & 0xFF == keys.ESCAPE:
            sys.exit(0)

        return key_code
