#!/usr/bin/env python3

"""
alias vclean=' ./vem.py clean'
alias vvenv='  ./vem.py venv'
alias vinit='  ./vem.py init'
alias vrun='   ./vem.py run'
"""

import platform
import subprocess
from typing import List, Callable
from pathlib import Path
from shutil import rmtree

try:
    import typer
except:
    print('pip install typer')
    exit(0)

app = typer.Typer(help="Virtual Environment Management utility.")

APP_PATH = Path("/Users/johncooper/Applications")  # FIXME
VENV_PATH = Path("./venv")
REQUIREMENTS_PATH = Path("requirements")
REQUIREMENTS_TXT_PATH = Path("requirements.txt")

windows = platform.system() == "Windows"
SEPARATOR = " & " if windows else "; "
ACTIVATE_PATH = VENV_PATH / ("Scripts/activate.bat" if windows else "bin/activate")
ACTIVATE_COMMAND = (
    f"{ACTIVATE_PATH} {SEPARATOR}" if windows else f"source {ACTIVATE_PATH} {SEPARATOR}"
)

# SOURCE_PATHS = sorted(Path(".").glob("*.py"))

venv_commands = f"""
    python3 -m venv {VENV_PATH}
    {ACTIVATE_COMMAND} pip install --upgrade pip
    {ACTIVATE_COMMAND} pip install -r {REQUIREMENTS_PATH}
    {ACTIVATE_COMMAND} pip freeze > {REQUIREMENTS_TXT_PATH}
    """

init_commands = ""
run_commands = ""
exe_commands = ""


def echo(string):
    typer.secho(string, fg=typer.colors.GREEN, bold=True)


def remove(path: Path):
    if path.exists():
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()


def before(path1: Path, path2: Path):
    return path1.stat().st_mtime < path2.stat().st_mtime


def make(target: Path, dependencies: List[Path], command: Callable):
    if not target.exists() or any(before(target, dep) for dep in dependencies):
        command()


def run(commands):
    for command in [command.strip() for command in commands.strip().split("\n")]:
        echo("\n" + command)
        result = subprocess.run(command, shell=True)
        # echo(f"{result.args} {result.returncode}\n")
    return result


@app.command()
def clean():
    """
    Remove temporary files
    """
    echo(clean.__doc__)
    remove(VENV_PATH)
    remove(Path("__pycache__"))


@app.command()
def venv():
    """
    Make virtual environment
    """
    echo(venv.__doc__)
    clean()
    run(venv_commands)


@app.command()
def init():
    """
    Initialize database
    """
    make(VENV_PATH, [REQUIREMENTS_PATH], venv)

    echo(init.__doc__)
    run(init_commands)


@app.command()
def exe():
    """
    Build exectutable
    """
    make(VENV_PATH, [REQUIREMENTS_PATH], venv)
    remove(APP_PATH / "i_view.app")

    echo(exe.__doc__)
    run(exe_commands)

    remove(Path("build"))
    remove(Path("dist"))
    remove(Path("setup.py"))


@app.command("run")
def run_():
    """
    Run flask app
    """
    make(VENV_PATH, [REQUIREMENTS_PATH], venv)

    echo(run_.__doc__)
    run(run_commands)


'''
SCRIPTS_PATH = Path("scripts")
init_commands = f"""
    {ACTIVATE_COMMAND} {SCRIPTS_PATH / 'load.py'} {SCRIPTS_PATH / 'python.md'}
    """
'''

exe_commands = f"""
    {ACTIVATE_COMMAND} py2applet --make-setup i_view.py
    {ACTIVATE_COMMAND} python setup.py py2app -A --argv-emulation --emulate-shell-environment
    mv dist/i_view.app {APP_PATH}
"""


RUN_PATH = Path("iview.py")
run_commands = f"""
    {ACTIVATE_COMMAND} python {RUN_PATH}
    """



if __name__ == "__main__":
    # typer.run(web)
    app()
