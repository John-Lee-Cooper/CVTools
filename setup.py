#!/usr/bin/env python

import io
from collections import defaultdict
from pathlib import Path
from setuptools import setup, find_packages

# The directory containing this file
DIRECTORY = Path(__file__).parent

# The text of the README file
README = (DIRECTORY / "README.md").read_text()

# Automatically capture required modules in requirements.txt for install_requires
with io.open(DIRECTORY / "requirements.txt", encoding="utf-8") as f:
    requirements = f.read().split("\n")

install_requires = [
    r.strip()
    for r in requirements
    if not ("git+" in r or r.startswith("#") or r.startswith("-"))
]

# Configure dependency links
dependency_links = [
    r.strip().replace("git+", "") for r in requirements if not ("git+" in r)
]

packages = find_packages(exclude=["tests"])

data_files = defaultdict(list)
for path in Path("data").rglob("*"):
    if path.is_file():
        data_files[str(path.parent)].append(str(path))
data_files = list(data_files.items())

setup(
    name="image-viewer",
    version="0.0.2",
    description="iview is a command line app for viewing images using open_cv.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="open cv,click",
    install_requires=install_requires,
    dependency_links=dependency_links,
    packages=packages,
    data_files=data_files,
    python_requires=">=3.6",
    entry_points=dict(console_scripts=["iview=iview.__main__:main"]),
    url="https://github.com/John-Lee-Cooper/image-viewer/",
    download_url="https://github.com/John-Lee-Cooper/image-viewer/archive/1.0.0.tar.gz",
    classifiers=[
        "License :: OSI Approved :: GPL License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    license="GPL",
    author="John Lee Cooper",
    author_email="john.lee.cooper@gatech.edu",
)
