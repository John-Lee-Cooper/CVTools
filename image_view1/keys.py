"""
Provide key constants for each platform
"""

from sys import platform
from typing import Optional

import ui



ESCAPE = 27
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

KEY_NAME = {
    ESCAPE: "<ESCAPE>",
    SPACE: "<SPACE>",
    BACKSPACE: "<BACKSPACE>",
    ENTER: "<ENTER>",
    DELETE: "<DELETE>",
}


class KeyAssignment:
    max_width = 0

    def __init__(self, command: str, value: str, description: str):

        if isinstance(value, type(0)):
            name = KEY_NAME.get(value)
        else:
            name, value = value, ord(value)

        self.command = command
        self.value = value
        self.name = name
        self.description = description

        KeyAssignment.max_width = max(KeyAssignment.max_width, len(name))

    def __str__(self):
        return f"{self.name:{self.max_width}} {self.description}"


class KeyAssignments:
    def __init__(self, default_command="help"):
        self.list_ = []
        self.default_command = default_command

    def append(self, command: str, value: str, description: str):
        self.list_.append(KeyAssignment(command, value, description))

    def command(self, key: int) -> Optional[str]:
        for ka in self.list_:
            if key == ka.value:
                if callable(ka.command):
                    ka.command()
                    return None
                return ka.command
        print(key)
        return self.default_command

    def help_string(self, header: str = "Press", delim: str = "\n  ") -> str:
        return delim.join([header] + [str(key) for key in self.list_])
