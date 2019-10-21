#!/usr/bin/env python

"""
Provide Additional Click Types

Including:
  PATH - same as click.types.Path but returns a Path instead of a string
  FILEPATH - same as PATH but must be an existing file
  DIRPATH - same as PATH but must be an existing directory
"""


from pathlib import Path
import click


class PathParamType(click.types.Path):
    """ Click type extension that takes a path string and returns a Path """
    name = "Path"

    def __init__(self, exists=True, **kw):
        super().__init__(exists=exists, **kw)

    def convert(self, value, param, ctx):
        try:
            return Path(super().convert(value, param, ctx))
        except ValueError:
            self.fail("%s is not a valid path" % value, param, ctx)


class FilePathParamType(PathParamType):
    """ Click type extension that takes a path to an existing file and returns a Path """
    def __init__(self, exists=True, dir_okay=False, **kw):
        super().__init__(exists=exists, dir_okay=dir_okay, **kw)


class DirectoryPathParamType(PathParamType):
    """ Click type extension that takes a path to an existing directory and returns a Path """
    def __init__(self, exists=True, file_okay=False, **kw):
        super().__init__(exists=exists, file_okay=file_okay, **kw)


PATH = PathParamType()
FILEPATH = FilePathParamType()
DIRPATH = DirectoryPathParamType()


@click.command()
@click.option("--filepath", type=FILEPATH)
@click.option("--dirpath", type=DIRPATH, default=".")
@click.argument("path", type=PATH, nargs=-1)
def main(filepath, dirpath, path):
    click.echo(f"filepath: {filepath}")
    click.echo(f"dirpath: {dirpath}")
    click.echo(f"path: {path}")


if __name__ == "__main__":
    main()
