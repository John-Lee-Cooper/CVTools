"""
Configure the tool
"""

from pathlib import Path

# Paths
ROOT_PATH = Path("~/Development/cv_tools").expanduser()
ROOT_PATH = Path("~/python/cv_tools").expanduser()
DATA_PATH = ROOT_PATH / "data/"
TRASH_PATH = DATA_PATH / "trash/"
FONT_PATH = DATA_PATH / "fonts" / "DroidSansMono.ttf"
FAVORITES_PATH = ROOT_PATH / "favorites.txt"

# UI click styles
ERROR_STYLE = dict(fg="red", bold=True)
WARNING_STYLE = dict(fg="yellow", bold=True)
INFO_STYLE = dict(fg="green", bold=False)
