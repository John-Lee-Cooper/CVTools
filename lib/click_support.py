#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provide Additional Click Types
Including
  PATH - same as click.types.Path but returns a Path instead of a string
  FILEPATH - same as PATH but must be an existing file
  DIRPATH - same as PATH but must be an existing directory
"""


from pathlib import Path
import click


"""
TODO:
  Color     (r,g,b, #RRGGBB or green)
  ImagePath *.[jpg|png|...]
  Image     *.[jpg|png|...]


class BasedIntParamType(click.ParamType):
    name = 'integer'

    def convert(self, value, param, ctx):
        try:
            if value[:2].lower() == '0x':
                return int(value[2:], 16)
            if value[:1] == '0':
                return int(value, 8)
            return int(value, 10)
        except ValueError:
            self.fail('%s is not a valid integer' % value, param, ctx)

INT = BasedIntParamType()
"""


class PathParamType(click.types.Path):
    name = "Path"

    def __init__(self, exists=True, **kw):
        super().__init__(exists=exists, **kw)

    def convert(self, value, param, ctx):
        try:
            value = super().convert(value, param, ctx)
            return Path(value)
        except ValueError:
            self.fail("%s is not a valid path" % value, param, ctx)


class FilePathParamType(PathParamType):
    def __init__(self, exists=True, dir_okay=False, **kw):
        super().__init__(exists=exists, dir_okay=dir_okay, **kw)


class DirectoryPathParamType(PathParamType):
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
