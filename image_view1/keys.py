"""
Provide key constants for each platform
"""

from sys import platform
import ui


ESC = 27
SPACE = 32
BACKSPACE = 8
ENTER = 13

if platform in ("linux", "linux2"):
    DELETE = 255

elif platform == "darwin":  # OS X
    DELETE = 117

# elif platform == "win32":  # Windows...

else:
    ui.warning(f"Window does not fully support {platform}")
    DELETE = -1
