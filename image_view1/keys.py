#!/usr/bin/env python

from sys import platform
import ui


ESC_KEY = 27
SPACE = 32
BACKSPACE = 8

if platform in ("linux", "linux2"):
    DELETE_KEY = 255

elif platform == "darwin":  # OS X
    DELETE_KEY = 117

# elif platform == "win32":  # Windows...

else:
    ui.warning(f"Window does not fully support {platform}")
    DELETE_KEY = -1
