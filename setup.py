#!/usr/bin/env python

from setuptools import setup
from pathlib import Path

# The text of the README file in directory containing this file
README = (Path(__file__).parent / "README.md").read_text()

setup(
    name="image-viewer",
    version="0.0.2",
    description="iview is a command line app for viewing images using open_cv.",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords="open cv,click",
    install_requires=['click==7.1.2', 'freetype-py==2.2.0', 'gif2numpy==1.3', 'kaitaistruct==0.9', 'mss==6.1.0', 'numpy2gif==1.0', 'numpy==1.19.4', 'opencv-python==4.4.0.46', 'pilasopencv==2.7', 'pyobjc-core==7.1', 'pyobjc-framework-cocoa==7.1', 'pyobjc-framework-quartz==7.1', 'pyuserinput==0.1.11', 'typer==0.3.2'],
    # dependency_links="",
    packages=['lib', 'iview'],
    data_files=[('data/fonts', ['data/fonts/DroidSansMono.ttf'])],
    python_requires=">=3.6",
    entry_points=dict(console_scripts=["iview=iview.__main__:main"]),
    url="https://github.com/John-Lee-Cooper/image-viewer/",
    download_url="https://github.com/John-Lee-Cooper/image-viewer/archive/1.0.0.tar.gz",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    license="GPL",
    author="John Lee Cooper",
    author_email="john.lee.cooper@gatech.edu",
)
