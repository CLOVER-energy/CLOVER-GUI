#
#
#

import sys

from typing import Any

from setuptools import find_packages

from cx_Freeze import setup, Executable

BASE: str = "Win32GUI" if sys.platform == "win32" else None

# Dependencies are automatically detected, but it might need
# fine tuning.
includes_files: list[str] = ["src/images/"]
build_options: dict[str, list[Any]] = {
    "packages": [],
    "excludes": [],
    "include_files": includes_files,
}

executables = [Executable("src/main.py", base=BASE, target_name="clover-gui")]

try:
    with open("README.md", "r", encoding="UTF-8") as f:
        long_description: str = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="CLOVER-GUI",
    version="1.0.0a1",
    description="A graphical user interface for CLOVER",
    long_description=long_description,
    author="Ben Winchester and Hamish Beath",
    author_email="benedict.winchester@gmail.com,hamishbeath@outlook.com",
    url="https://github.com/CLOVER-energy/CLOVER-GUI",
    project_urls={
        "Bug Tracker": "https://github.com/CLOVER-energy/CLOVER-GUI/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "customtkinter >= 5.1.3",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    options={"build_exe": build_options},
    executables=executables,
)
