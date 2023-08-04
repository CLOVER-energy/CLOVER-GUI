#!/usr/bin/python3.10
########################################################################################
# splash_screen.py - The splash-screen module for CLOVER-GUI application.              #
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

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import CLOVER_SPLASH_SCREEN_IMAGE, IMAGES_DIRECTORY

__all__ = ("SplashScreenWindow",)


# Screens
class SplashScreenWindow(tk.Toplevel):
    """
    Represents a splash screen.

    """

    def __init__(self, parent, data_directory: str) -> None:
        """
        Instantiate the :class:`SplashScreen` instance.

        :param: parent
            The parent screen.

        :param: data_directory
            The path to the data directory.

        """

        tk.Toplevel.__init__(self, parent)

        self.title("CLOVER-GUI Splash")
        self.background_image = tk.PhotoImage(
            file=os.path.join(
                data_directory, IMAGES_DIRECTORY, CLOVER_SPLASH_SCREEN_IMAGE
            )
        )
        self.background_image = self.background_image.subsample(2)
        self.splash_label = ttk.Label(self, image=self.background_image)
        self.splash_label.pack()

        # Create an updatable progress bar.
        self.progress_bar = ttk.Progressbar(
            self, bootstyle=f"{SUCCESS}-striped", mode="determinate"
        )
        self.progress_bar.pack(pady=20, padx=20, fill="x")
        self.progress_bar.start()

        # Disable the in-built minimise, maximise and close buttons.
        self.overrideredirect(True)

        # Required to make the splash screen visible.
        self.update()

    def set_progress_bar_progress(self, value) -> None:
        """
        Sets the value of the progress bar.

        :param: value
            The value to use for setting the progress bar position.

        """

        self.progress_bar["value"] = value
        self.progress_bar.update()
