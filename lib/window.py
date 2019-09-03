#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
https://www.pythonforthelab.com/blog/step-by-step-guide-to-building-a-gui/
https://docs.opencv.org/trunk/dc/d46/group__highgui__qt.html
https://subscription.packtpub.com/book/application_development/9781788472395/1


"""

from sys import argv
from pathlib import Path, PosixPath
import cv2 as cv
from open_cv import DATA_PATH, imread


ESC_KEY = 27
SPACE = 32
BACKSPACE = 8


def script_stem():
    return Path(argv[0]).stem


def path_name(path):
    if type(path) is PosixPath:
        return path.name
    return path


class Window:
    def __init__(
        self, name="", flag=cv.WINDOW_GUI_NORMAL, image=None, include_script_name=True
    ):

        name = path_name(name)
        if not name or include_script_name:
            name = f"{script_stem()} {name}"
        self.name = name  # or Path(argv[0]).name
        cv.namedWindow(self.name, flag)
        cv.setWindowProperty(self.name, cv.WND_PROP_AUTOSIZE, 1.0)

        self.mouse_down = False
        self.r_mouse_down = False
        self.mouse_at = self.mouse_down_at = None
        self.r_mouse_at = self.r_mouse_down_at = None

        if image is not None:
            self.display(image)

    def destroy(self):
        cv.destroyWindow(self.name)

    '''
    def __del__(self):
        #cv.destroyWindow(self.name)
        pass
    '''

    def set_title(self, title, include_script_name=True):
        title = path_name(title)
        if include_script_name:
            title = f"{script_stem()} {title}"
        cv.setWindowTitle(self.name, title)

    def setMouseCallback(self, on_mouse, image=None):
        cv.setMouseCallback(self.name, on_mouse, image)

    def mouse_reset(self):
        self.mouse_at = self.mouse_down_at = None
        self.r_mouse_at = self.r_mouse_down_at = None

    def mouse_event(self, event, x, y, flags, params):
        """
        Mouse Callback
    
        event: The event that took place
        x: The x-coordinate of the event.
        y: The y-coordinate of the event.
        flags: Any relevant flags passed by OpenCV.
        params: Any extra parameters supplied by OpenCV.
        """
        #print(event, x, y, flags, params)

        # On mouse button click, record mouse down point
        if event == cv.EVENT_LBUTTONDOWN:
            self.mouse_down = True
            self.mouse_down_at = self.mouse_at = (x, y)
            self.r_mouse_at = self.r_mouse_down_at = None
        elif event == cv.EVENT_RBUTTONDOWN:
            self.r_mouse_down = True
            self.r_mouse_down_at = self.r_mouse_at = (x, y)
            self.mouse_at = self.mouse_down_at = None

        # If mouse button is released, update mouse_down status to False
        elif event == cv.EVENT_LBUTTONUP:
            self.mouse_down = False
            self.mouse_at = (x, y)
        elif event == cv.EVENT_RBUTTONUP:
            self.r_mouse_down = False
            self.r_mouse_at = (x, y)

        # On mouse movement record mouse location
        elif event == cv.EVENT_MOUSEMOVE:
            if self.mouse_down:
                self.mouse_at = (x, y)
            if self.r_mouse_down:
                self.r_mouse_at = (x, y)

    def display(self, image, wait_ms=None):
        """
        Display image in window

        By default it will wait for ever for a key stroke
        If wait is None, it will not wait at all.
        """
        cv.imshow(self.name, image)

        if wait_ms is None:
            return -1  # None

        return self.wait(wait_ms)

    def wait(self, wait_ms=0):
        # TODO: Pass in keyhandler

        key_code = cv.waitKey(int(wait_ms))
        # key_code = cv.waitKeyEx(int(wait_ms))
        # if key_code != -1: print(key_code)

        if key_code & 0xFF == ESC_KEY:
            exit(0)

        return key_code

    # def ctrl_key(res):
    #     # control key" 19. Shift 17, the CapsLock 18, Alt bit 20, and NumLock 21.
    #     return res & (1 << 18)

    """
    cv.WND_PROP_FULLSCREEN
    cv.WND_PROP_AUTOSIZE
    cv.WND_PROP_ASPECT_RATIO
    cv.WND_PROP_OPENGL
    cv.WND_PROP_VISIBLE
    """

    def toggle_fullscreen(self):
        value = cv.getWindowProperty(self.name, cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty(self.name, cv.WND_PROP_FULLSCREEN, not value)

    def toggle_autosize(self):
        value = cv.getWindowProperty(self.name, cv.WND_PROP_AUTOSIZE)
        cv.setWindowProperty(self.name, cv.WND_PROP_AUTOSIZE, not value)

    def rect(self):
        """ return x, y, w, h """
        return cv.getWindowImageRect(self.name)

    def move(self, x, y):
        cv.moveWindow(self.name, x, y)

    def resize(self, w, h):
        cv.resizeWindow(self.name, w, h)


flag_list = (
    (cv.EVENT_FLAG_CTRLKEY, "CTRL"),
    (cv.EVENT_FLAG_ALTKEY, "ALT"),
    (cv.EVENT_FLAG_SHIFTKEY, "SHIFT"),
    (cv.EVENT_FLAG_LBUTTON, "L"),
    (cv.EVENT_FLAG_RBUTTON, "R"),
    (cv.EVENT_FLAG_MBUTTON, "M"),
)

event_dict = {
    cv.EVENT_MOUSEMOVE: "Move",
    cv.EVENT_LBUTTONDOWN: "LDown",
    cv.EVENT_RBUTTONDOWN: "RDown",
    cv.EVENT_MBUTTONDOWN: "MDown",
    cv.EVENT_LBUTTONUP: "LUp",
    cv.EVENT_RBUTTONUP: "RUp",
    cv.EVENT_MBUTTONUP: "MUp",
    cv.EVENT_LBUTTONDBLCLK: "LDblClick",
    cv.EVENT_RBUTTONDBLCLK: "RDblClick",
    cv.EVENT_MBUTTONDBLCLK: "MDblClick",
    cv.EVENT_MOUSEWHEEL: "Wheel",
    cv.EVENT_MOUSEHWHEEL: "HWheel",
}

wheel_events = (cv.EVENT_MOUSEWHEEL, cv.EVENT_MOUSEHWHEEL)


def on_mouse(event, x, y, flag, user_data):
    image = user_data
    h, w = image.shape[:2]
    if 0 <= x < w and 0 <= y < h:
        b, g, r = image[y][x]  # pixel
    else:
        b, g, r = 0, 0, 0

    event_str = event_dict[event]
    flags = " ".join([string for flag_bit, string in flag_list if flag & flag_bit])
    delta = (1 if flag > 0 else -1) if event in wheel_events else 0
    print(
        f"event={event_str:12}({event:2}) "
        f"flag={flags:12}({flag:2}) "
        f"pos=({x:4}, {y:4}) "
        f"{delta} "
        f"pixel={r:02X} {g:02X} {b:02X} "
    )


def demo(filename):
    """
    """
    image = imread(filename)

    window = Window(filename.name, image=image)
    window.setMouseCallback(on_mouse, image)
    while 1:
        window.wait(0)

    cv.destroyAllWindows()

    """
        # TODO Remove
        if key_code == ord("?"):
            print(cv.getBuildInformation())
        elif key_code == ord("f"):
            self.toggle_fullscreen()
        elif key_code == ord("a"):
            self.toggle_autosize()
        elif key_code == ord("g"):
            cv.destroyWindow(self.name)
            cv.namedWindow(self.name, cv.WINDOW_GUI_EXPANDED)
    """


if __name__ == "__main__":
    demo(DATA_PATH / "sunflower.jpg")
