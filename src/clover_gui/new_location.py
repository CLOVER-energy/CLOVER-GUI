#!/usr/bin/python3.10
########################################################################################
# new_location.py - The new-location module for CLOVER-GUI application.                #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import tkinter as tk

from typing import Callable

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


from .__utils__ import BaseScreen
from .splash_screen import SplashScreen


class NewLocationScreen(BaseScreen, show_navigation=True):
    """
    Represents the new-location frame.

    The new-location frame enables a user to create a new location within CLOVER.

    TODO: Update attributes.

    """

    def __init__(
        self, splash_screen: SplashScreen, create_location_callback: Callable
    ) -> None:
        """
        Instantiate a :class:`MainMenuFrame` instance.

        :param: splash_screen
            The :class:`SplashScreen` being displayed.

        :param: create_location_callback:
            The callback function for when a new location is created.

        """

        # Instntiate the parent class
        super().__init__()

        self.pack(fill="both", expand=True)

        # Set the physical distance weights of the rows and columns
        self.rowconfigure(0, weight=2)  # First row has the header
        self.rowconfigure(1, weight=1)  # These rows have entries
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        self.columnconfigure(0, weight=1)  # First three have forward, home, back
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)  # These three have the entries
        self.columnconfigure(4, weight=4)
        self.columnconfigure(5, weight=4)

        self.label = ttk.Label(
            self, text="Create a new location", style=f"{PRIMARY}", font=80
        )
        self.label.grid(row=0, column=0, columnspan=6, pady=10)

        self.new_location_label = ttk.Label(self, text="Location name")
        self.new_location_label.grid(row=1, column=3, sticky="e")

        self.new_location_entry = ttk.Entry(self, bootstyle="primary")
        self.new_location_entry.grid(
            row=1, column=4, padx=10, pady=5, sticky="e", ipadx=80
        )

        self.latitude_label = ttk.Label(self, text="Latitude")
        self.latitude_label.grid(row=2, column=3, sticky="e")

        self.latitude_entry = ttk.Entry(self, bootstyle="primary")
        self.latitude_entry.grid(row=2, column=4, padx=10, pady=5, sticky="e", ipadx=80)

        self.latitude_unit = ttk.Label(self, text="degrees North")
        self.latitude_unit.grid(row=2, column=5, padx=10, pady=5, sticky="w")

        self.longitude_label = ttk.Label(self, text="Longitude")
        self.longitude_label.grid(row=3, column=3, sticky="e")

        self.longitude_entry = ttk.Entry(self, bootstyle="primary")
        self.longitude_entry.grid(
            row=3, column=4, padx=10, pady=5, sticky="e", ipadx=80
        )

        self.longitude_unit = ttk.Label(self, text="degrees East")
        self.longitude_unit.grid(row=3, column=5, padx=10, pady=5, sticky="w")

        self.time_zone_label = ttk.Label(self, text="Time zone")
        self.time_zone_label.grid(row=4, column=3, sticky="e")

        self.time_zone_entry = ttk.Spinbox(
            self, bootstyle="primary", from_=-13, to=13, increment=0.25, format="%.2f"
        )
        self.time_zone_entry.grid(
            row=4, column=4, padx=10, pady=5, sticky="e", ipadx=68
        )

        self.time_zone_unit = ttk.Label(self, text="hours from UTC")
        self.time_zone_unit.grid(row=4, column=5, padx=10, pady=5, sticky="w")

        self.create_location_button = ttk.Button(
            self,
            text="Create",
            bootstyle=f"{PRIMARY}-outline",
            command=create_location_callback,
        )
        self.create_location_button.grid(
            row=5, column=5, padx=5, pady=5, ipadx=80, ipady=20, sticky="w"
        )
