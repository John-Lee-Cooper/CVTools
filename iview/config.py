"""
App Configuration
"""

from pathlib import Path

from iview import color

# Paths
ROOT_PATH = Path(__file__).parent.parent
DATA_PATH = ROOT_PATH / "data/"
TRASH_PATH = DATA_PATH / "trash/"
FAVORITES_PATH = ROOT_PATH / "favorites.txt"

# Window settings
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
MATTE_COLOR = color.grey25
MATTE_SIZE = 32

FONT_PATH = DATA_PATH / "fonts" / "DroidSansMono.ttf"
FONT_SIZE = 18

# UI click styles
ERROR_STYLE = dict(fg="red", bold=True)
WARNING_STYLE = dict(fg="yellow", bold=True)
INFO_STYLE = dict(fg="green", bold=False)
