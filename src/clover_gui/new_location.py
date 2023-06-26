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
from .splash_screen import SplashScreenWindow


class NewLocationScreen(BaseScreen, show_navigation=True):
    """
    Represents the new-location frame.

    The new-location frame enables a user to create a new location within CLOVER.

    TODO: Update attributes.

    """

    def __init__(
        self, splash_screen: SplashScreenWindow, create_location_callback: Callable
    ) -> None:
        """
        Instantiate a :class:`NewLocationScreen` instance.

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
            self, text="Create a new location", style=SUCCESS, font=80
        )
        self.label.grid(row=0, column=0, columnspan=6, pady=10)

        self.new_location_label = ttk.Label(self, text="Location name")
        self.new_location_label.grid(row=1, column=3, sticky="e")

        self.new_location_entry = ttk.Entry(self, bootstyle=SUCCESS)
        self.new_location_entry.grid(
            row=1, column=4, padx=10, pady=5, sticky="e", ipadx=80
        )

        # Latitude
        self.latitude_label = ttk.Label(self, text="Latitude")
        self.latitude_label.grid(row=2, column=3, sticky="e", padx=10, pady=5)

        self.latitude = ttk.DoubleVar(self, 0, "latitude")

        self.scalar_latitude_value = ttk.Label(
            self, text=f"  0 degrees North"
        )
        self.scalar_latitude_value.grid(row=2, column=5, padx=10, pady=5, sticky="w")

        def scalar_latitude(_):
            self.scalar_latitude_value.config(
                text=f"{' ' * (int(abs(self.latitude.get())) < 100)}"
                f"{' ' * (int(abs(self.latitude.get())) < 10)}"
                f"{abs(round(self.latitude.get(), 2))} degrees"
                f" {'North' if self.latitude.get() >= 0 else 'South'}"
            )

        self.latitude_entry = ttk.Scale(
            self,
            from_=-90,
            to=90,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_latitude,
            bootstyle=SUCCESS,
            variable=self.latitude,
        )
        self.latitude_entry.grid(row=2, column=4, padx=10, pady=5, sticky="e")

        # Longitude
        self.longitude_label = ttk.Label(self, text="Longitude")
        self.longitude_label.grid(row=3, column=3, sticky="e", padx=10, pady=5)

        self.longitude = ttk.DoubleVar(self, 0, "longitude")

        self.scalar_longitude_value = ttk.Label(
            self, text=f"  0 degrees East"
        )
        self.scalar_longitude_value.grid(row=3, column=5, padx=10, pady=5, sticky="w")

        def scalar_longitude(_):
            self.scalar_longitude_value.config(
                text=f"{' ' * (int(abs(self.longitude.get())) < 100)}"
                f"{' ' * (int(abs(self.longitude.get())) < 10)}"
                f"{abs(round(self.longitude.get(), 2))} degrees"
                f" {'East' if self.longitude.get() >= 0 else 'West'}"
            )

        self.longitude_entry = ttk.Scale(
            self,
            from_=-180,
            to=180,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_longitude,
            bootstyle=SUCCESS,
            variable=self.longitude,
        )
        self.longitude_entry.grid(row=3, column=4, padx=10, pady=5, sticky="e")

        self.time_zone_label = ttk.Label(self, text="Time zone")
        self.time_zone_label.grid(row=4, column=3, sticky="e")

        self.time_zone = ttk.DoubleVar(self, 0, "time_zone")

        def set_time_zone():
            self.time_zone.set(self.time_zone_entry.get())

        self.time_zone_entry = ttk.Spinbox(
            self, bootstyle=SUCCESS, from_=-13, to=13, increment=0.25, format="%.2f", command=set_time_zone
        )
        self.time_zone_entry.set(0)
        self.time_zone_entry.grid(
            row=4, column=4, padx=10, pady=5, sticky="e", ipadx=68
        )

        self.time_zone_unit = ttk.Label(self, text="hours from UTC")
        self.time_zone_unit.grid(row=4, column=5, padx=10, pady=5, sticky="w")

        self.create_location_button = ttk.Button(
            self,
            text="Create",
            bootstyle=f"{SUCCESS}-outline",
            command=create_location_callback,
        )
        self.create_location_button.grid(
            row=5, column=5, padx=5, pady=5, ipadx=80, ipady=20, sticky="w"
        )
