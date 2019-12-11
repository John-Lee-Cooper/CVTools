"""
Configure the tool
"""

from pathlib import Path

# Paths
DATA_PATH = Path("~/python/open_cv/data/").expanduser()
TRASH_PATH = Path("~/python/open_cv/data/trash/").expanduser()

FONT_PATH = Path("../DroidSansMono.ttf")

# UI click styles
ERROR_STYLE = dict(fg="red", bold=True)
WARNING_STYLE = dict(fg="yellow", bold=True)
INFO_STYLE = dict(fg="green", bold=False)
