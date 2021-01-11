#!/usr/bin/env python

import io
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
    r.strip().replace("git+", "")
    for r in requirements
    if not ("git+" in r)
]

setup(
    name="image_viewer",
    description="Description",
    version="1.0",
    # version="1.0.post7",
    packages=["iview", "lib"],
    install_requires=install_requires,
    python_requires=">=3.6",
    entry_points="""
        [console_scripts]
        iview=iview.iview:main
    """,
    author="John Lee Cooper",
    keyword="open_cv",
    long_description=README,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/John-Lee-Cooper/iview",
    download_url="https://github.com/John-Lee-Cooper/iview/archive/1.0.0.tar.gz",
    dependency_links=dependency_links,
    author_email="john.lee.cooper@gatech.edu",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
