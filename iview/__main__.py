#!/usr/bin/env python

"""
Command line interface to iview
"""

from pathlib import Path

import sys
import typer

from iview.paths import script_name
from iview.type_ext import List
from iview.iview import App
from lib.cli import run as typer_run
from lib.util import update_docstring

__version__ = "1.0.0"


def version_option(version: str) -> bool:
    """
    :returns: the typer Option that handles --version
    """

    def version_callback(_ctxt: typer.Context, value: bool):
        if value:
            typer.echo(f"{script_name()} version: {version}")
            sys.exit(0)

    return typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    )


def run(
    paths: List[Path],  # List[FilePath],
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Traverse subdirectories of directories included in PATHS",
    ),
    version: bool = version_option(__version__),
) -> None:
    """
    {app} - a digital photo viewer

    \b
    {app} allows you to step forward or backward though all the images
    and/or image directories specified in the arguments.

    {app} displays the image specified by PATHS.
    PATHS is a list of image paths or a directory containing images.

    \b
    Press
      <SPACE>     to go to the next image.
      <BACKSPACE> to go to the previous image.
      <DELETE>    to delete the current image.
      <ESCAPE>    to exit.
    """

    App(paths, subdirectories=recursive).run()


def main() -> None:
    """Call the app command run """

    update_docstring(run, app=script_name())
    typer_run(run)


if __name__ == "__main__":
    main()
