#!/usr/bin/python3.10
########################################################################################
# __utils__.py - The utility module for CLOVER-GUI application.                        #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import os

import tkinter as tk

import ttkbootstrap as ttk

__all__ = (
    "BaseScreen",
    "CLOVER_SPLASH_SCREEN_IMAGE",
    "IMAGES_DIRECTORY",
    "MAIN_WINDOW_GEOMETRY",
)

# CLOVER splash-screen image:
#   The name of the CLOVER splash-screen image.
CLOVER_SPLASH_SCREEN_IMAGE: str = "clover_splash_screen.png"

# Images directory:
#   The directory containing the images to display.
IMAGES_DIRECTORY: str = os.path.join("clover_gui", "images")

# Main-window geometry:
#   The geometry to use for the main window, specified in width and height.
MAIN_WINDOW_GEOMETRY: str = "1220x800"


class BaseScreen(ttk.Frame):
    """
    Abstract class that represents a screen within the CLOVER-GUI application.

    .. attribute:: show_navigation
        Whether to show the navigation buttons.

    """

    # Private attributes:
    #   .. attribute:: _backward_journey
    #       Keeps track of the backward journey within the GUI.
    #
    #   .. attribute:: _forward_journey
    #       Keeps track of the forward journey within the GUI if applicable.
    #

    _backward_journey: list = []
    _forward_journey: list = []
    show_navigation: bool

    def __init_subclass__(cls, show_navigation: bool) -> None:
        """
        Sub-class hook to ensure that forward and backward navigation are present if
        applicable.

        :param: show_navigation

        """

        cls.show_navigation = show_navigation

        return super().__init_subclass__()
