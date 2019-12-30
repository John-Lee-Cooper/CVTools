"""
Configure the tool
"""

from pathlib import Path

# Paths
OPEN_CV = Path("~/python/open_cv").expanduser()
DATA_PATH = OPEN_CV / "data/"
TRASH_PATH = OPEN_CV / "data/trash/"

CV_TOOLS = Path("~/python/cv_tools").expanduser()
FONT_PATH = CV_TOOLS / "DroidSansMono.ttf"
FAVORITES_PATH = CV_TOOLS / "favorites.txt"

# UI click styles
ERROR_STYLE = dict(fg="red", bold=True)
WARNING_STYLE = dict(fg="yellow", bold=True)
INFO_STYLE = dict(fg="green", bold=False)
