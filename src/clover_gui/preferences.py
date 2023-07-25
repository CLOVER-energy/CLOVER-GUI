#!/usr/bin/python3.10
########################################################################################
# preferences.py - The preferences module for CLOVER-GUI application.                  #
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


from .__utils__ import BaseScreen, LOAD_LOCATION_GEOMETRY, LOCATIONS_DIRECTORY

__all__ = ("PreferencesWindow",)


class PreferencesScreen(BaseScreen, show_navigation=False):
    """
    Represents the preferences window.

    The preferences screen enables a user to set various preferences.

    TODO: Update attributes.

    """

    def __init__(self, parent) -> None:
        """
        Instantiate a :class:`PreferencesScreen` instance.

        :param: parent
            The parent window or frame.

        """

        super().__init__(parent)

        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=2)  # First row has the header
        self.columnconfigure(1, weight=1)  # These rows have entries

        self.rowconfigure(0, weight=6)
        self.rowconfigure(1, weight=3)
        self.rowconfigure(2, weight=3)
        self.rowconfigure(3, weight=1)

        self.label = ttk.Label(
            self, text="Load an existing location", style=f"{PRIMARY}", font=80
        )
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        self.location_name_label = ttk.Label(self, text="Location name")
        self.location_name_label.grid(row=1, column=0, sticky="e")

        self.load_location_name: ttk.StringVar = ttk.StringVar(self)

        self.load_location_combobox = ttk.Combobox(
            self, bootstyle="primary", textvariable=self.load_location_name
        )
        self.load_location_combobox.grid(
            row=1, column=1, padx=10, pady=5, sticky="w", ipadx=80
        )
        self.load_location_combobox.bind("<<ComboboxSelected>>", self.select_location)
        self.populate_available_locations()

        self.load_button = ttk.Button(
            self,
            text="Load",
            bootstyle=f"{PRIMARY}-outline",
            command=load_location_callback,
        )
        self.load_button.grid(row=2, column=1, padx=10, pady=10, ipadx=80, ipady=20)

        self.progress_bar = ttk.Progressbar(
            self, bootstyle=f"{PRIMARY}-striped", mode="determinate"
        )
        self.progress_bar.grid(
            row=3, column=0, columnspan=2, pady=20, padx=20, sticky="ew"
        )

    def populate_available_locations(self) -> None:
        """Populates available locations for selection."""

        if not os.path.isdir(LOCATIONS_DIRECTORY):
            return

        self.load_location_combobox["values"] = os.listdir(LOCATIONS_DIRECTORY)
        self.load_location_name.set(self.load_location_combobox["values"][0])

    def select_location(self, _) -> None:
        """Selects the location specified."""

        self.load_location_name.set(self.load_location_combobox.get())


class PreferencesWindow(tk.Toplevel):
    """
    Represents the load-location popup window.

    The load-location popup window displays and enables a user to load an existing
    location.

    TODO: Update attributes.

    """

    def __init__(self) -> None:
        """
        Instantiate a :class:`PreferencesWindow` instance.

        :param: load_location_callback:
            The callback function for when an existing location is to be loaded.

        """

        # Instntiate the parent class
        super().__init__()

        self.title("CLOVER-GUI Load Location")

        self.geometry(LOAD_LOCATION_GEOMETRY)

        self.load_location_frame = PreferencesScreen(self)

        self.protocol("WM_DELETE_WINDOW", self.withdraw)
