#!/usr/bin/python3.10
########################################################################################
# main_menu.py - The main-menu module for CLOVER-GUI application.                      #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import os
import tkinter as tk

from typing import Callable

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen, CLOVER_SPLASH_SCREEN_IMAGE, IMAGES_DIRECTORY
from .splash_screen import SplashScreenWindow


class MainMenuScreen(BaseScreen, show_navigation=False):
    """
    Represents the main-menu frame.

    The main-menu frame contains two buttons:
        - A "new-location" button, which takes the user to a screen where they can set
          up a new location,
        - A "load-location" button, which creates a popup prompting the user to load an
          existing location.

    .. attribute:: label
        The label instance holding the main-menu image.

    .. attribute:: load_location_button
        A button which provides the user the option of loading an existing location.

    .. attribute:: main_menu_image
        The image to display at the top of the main-menu screen.

    .. attribute:: new_location_button
        A button which which provides the user the option of creating a new location.

    """

    def __init__(
        self,
        data_directory: str,
        load_location_callback: Callable,
        new_location_callback: Callable,
    ) -> None:
        """
        Instantiate a :class:`MainMenuFrame` instance.

        :param: data_directory
            The name of the data directory to use.

        :param: load_location_callback
            The callback function to use when the load-location button is pressed.

        :param: new_location_callback
            The callback function to use when the new-location button is pressed.

        """

        super().__init__()

        self.pack(fill="both", expand=True)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.main_menu_image = tk.PhotoImage(
            file=os.path.join(
                data_directory, IMAGES_DIRECTORY, CLOVER_SPLASH_SCREEN_IMAGE
            )
        )
        self.main_menu_image = self.main_menu_image.subsample(2)
        self.label = ttk.Label(self, image=self.main_menu_image)
        self.label.grid(row=0, column=0, columnspan=2, sticky="news")

        self.new_location_button = ttk.Button(
            self,
            text="New location",
            bootstyle=f"{SUCCESS}-outline",
            command=new_location_callback,
        )
        self.new_location_button.grid(
            row=1, column=0, padx=5, pady=5, ipadx=80, ipady=20
        )

        self.load_location_button = ttk.Button(
            self,
            text="Load location",
            bootstyle=f"{PRIMARY}-outline",
            command=load_location_callback,
        )
        self.load_location_button.grid(
            row=1, column=1, padx=5, pady=5, ipadx=80, ipady=20
        )
