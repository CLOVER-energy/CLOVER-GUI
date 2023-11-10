#
#
#

import sys

from typing import Any

from setuptools import find_packages, setup

# from cx_Freeze import setup, Executable

BASE: str = "Win32GUI" if sys.platform == "win32" else None

# Dependencies are automatically detected, but it might need
# fine tuning.
includes_files: list[str] = ["src/images/"]
build_options: dict[str, list[Any]] = {
    "packages": [],
    "excludes": [],
    "include_files": includes_files,
}

# executables = [Executable("src/main.py", base=BASE, target_name="clover-gui")]

try:
    with open("README.md", "r", encoding="UTF-8") as f:
        long_description: str = f.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="CLOVER-GUI",
    version="1.0.0b3",
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
        "clover-energy >=5.2.0a6",
        "customtkinter>=5.2.0",
        "cx-Freeze >=6.15.5",
        "pandas >=1.2.3",
        "PyYAML >=5.4.1",
        "RangeSlider>=2021.7.4",
        "seaborn >=0.11.1",
        "ttkbootstrap>=1.10.1",
    ],
    include_package_data=True,
    package_data={"": ["data/images/*"]},
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    options={"build_exe": build_options},
    # executables=executables,
)
