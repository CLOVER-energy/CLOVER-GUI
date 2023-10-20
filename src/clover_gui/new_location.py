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

import os
import tkinter as tk

from typing import Callable

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


from .__utils__ import BaseScreen, IMAGES_DIRECTORY
from .splash_screen import SplashScreenWindow


class NewLocationScreen(BaseScreen, show_navigation=True):
    """
    Represents the new-location frame.

    The new-location frame enables a user to create a new location within CLOVER.

    TODO: Update attributes.

    """

    def __init__(
        self,
        splash_screen: SplashScreenWindow,
        create_location_callback: Callable,
        data_directory: str,
    ) -> None:
        """
        Instantiate a :class:`NewLocationScreen` instance.

        :param: splash_screen
            The :class:`SplashScreen` being displayed.

        :param: create_location_callback:
            The callback function for when a new location is created.

        :param: data_directory
            The path to the data directory.

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
        self.rowconfigure(7, weight=1)

        self.columnconfigure(0, weight=1)  # First three have forward, home, back
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)  # These three have the entries
        self.columnconfigure(4, weight=4)
        self.columnconfigure(5, weight=2)
        self.columnconfigure(6, weight=1)

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
        self.latitude_label.grid(row=2, column=3, padx=10, pady=5, sticky="e")

        self.latitude = ttk.DoubleVar(self, 0.0, "latitude")

        self.latitude_unit = ttk.Label(self, text=f"degrees North")
        self.latitude_unit.grid(row=2, column=6, padx=10, pady=5, sticky="ew")

        def update_latitude_unit():
            """Update the unit with North or South"""
            if self.latitude.get() < 0:
                self.latitude_unit.configure(text="degrees South")
                return
            self.latitude_unit.configure(text="degrees North")

        def scalar_latitude(_):
            self.latitude.set(round(self.latitude_slider.get(), 2))
            self.latitude_entry.update()
            update_latitude_unit()

        self.latitude_slider = ttk.Scale(
            self,
            from_=-90,
            to=90,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_latitude,
            bootstyle=SUCCESS,
            variable=self.latitude,
        )
        self.latitude_slider.grid(row=2, column=4, padx=10, pady=5, sticky="e")

        def enter_latitude(_):
            self.latitude.set(self.latitude_entry.get())
            self.latitude_slider.set(self.latitude.get())
            update_latitude_unit()

        self.latitude_entry = ttk.Entry(
            self, bootstyle=SUCCESS, textvariable=self.latitude
        )
        self.latitude_entry.grid(row=2, column=5, padx=10, pady=5, sticky="ew")
        self.latitude_entry.bind("<Return>", enter_latitude)

        # Longitude
        self.longitude_label = ttk.Label(self, text="Longitude")
        self.longitude_label.grid(row=3, column=3, padx=10, pady=5, sticky="e")

        self.longitude = ttk.DoubleVar(self, 0.0, "longitude")

        self.longitude_unit = ttk.Label(self, text=f"degrees East")
        self.longitude_unit.grid(row=3, column=6, padx=10, pady=5, sticky="ew")

        def update_longitude_unit():
            """Update the unit with North or South"""
            if self.longitude.get() < 0:
                self.longitude_unit.configure(text="degrees West")
                return
            self.longitude_unit.configure(text="degrees East")

        def scalar_longitude(_):
            self.longitude.set(round(self.longitude_slider.get(), 2))
            self.longitude_entry.update()
            update_longitude_unit()

        self.longitude_slider = ttk.Scale(
            self,
            from_=-180,
            to=180,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_longitude,
            bootstyle=SUCCESS,
            variable=self.longitude,
        )
        self.longitude_slider.grid(row=3, column=4, padx=10, pady=5, sticky="e")

        def enter_longitude(_):
            self.longitude.set(self.longitude_entry.get())
            self.longitude_slider.set(self.longitude.get())
            update_longitude_unit()

        self.longitude_entry = ttk.Entry(
            self, bootstyle=SUCCESS, textvariable=self.longitude
        )
        self.longitude_entry.grid(row=3, column=5, padx=10, pady=5, sticky="ew")
        self.longitude_entry.bind("<Return>", enter_longitude)

        self.time_zone_label = ttk.Label(self, text="Time zone")
        self.time_zone_label.grid(row=4, column=3, sticky="e")

        self.time_zone = ttk.DoubleVar(self, 0, "time_zone")

        def set_time_zone():
            self.time_zone.set(self.time_zone_entry.get())

        self.time_zone_entry = ttk.Spinbox(
            self,
            bootstyle=SUCCESS,
            from_=-13,
            to=13,
            increment=0.25,
            format="%.2f",
            command=set_time_zone,
        )
        self.time_zone_entry.set(0)
        self.time_zone_entry.grid(
            row=4, column=4, padx=10, pady=5, sticky="e", ipadx=68
        )

        self.time_zone_unit = ttk.Label(self, text="hours from UTC")
        self.time_zone_unit.grid(row=4, column=5, padx=10, pady=5, sticky="w")

        self.warning_text_label = ttk.Label(
            self, text="", bootstyle=DANGER, state=DISABLED
        )
        self.warning_text_label.grid(
            row=5, column=1, columnspan=4, sticky="w", padx=(20, 20), pady=20
        )

        self.create_location_button = ttk.Button(
            self,
            text="Create",
            bootstyle=f"{SUCCESS}-outline",
            command=create_location_callback,
        )
        self.create_location_button.grid(
            row=5,
            column=5,
            columnspan=2,
            padx=5,
            pady=5,
            ipadx=80,
            ipady=20,
            sticky="w",
        )

        self.bottom_bar_frame = ttk.Frame(self)
        self.bottom_bar_frame.grid(row=7, column=0, columnspan=7, sticky="news", pady=0)

        self.bottom_bar_frame.columnconfigure(0, weight=1)
        self.bottom_bar_frame.columnconfigure(1, weight=1)
        self.bottom_bar_frame.columnconfigure(2, weight=1)
        self.bottom_bar_frame.columnconfigure(3, weight=10, minsize=400)
        self.bottom_bar_frame.columnconfigure(4, weight=1)

        self.back_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "back_arrow.png",
            )
        )
        self.back_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_back(self),
            image=self.back_button_image,
        )
        self.back_button.grid(
            row=0, column=0, padx=(60, 20), pady=(10, 0), sticky="news"
        )

        self.home_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "home_icon.png",
            )
        )
        self.home_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_home(self),
            image=self.home_button_image,
        )
        self.home_button.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="news")

        self.forward_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "forward_arrow.png",
            )
        )
        self.forward_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_forward(self),
            image=self.forward_button_image,
        )
        self.forward_button.grid(row=0, column=2, padx=20, pady=(10, 0), sticky="news")
