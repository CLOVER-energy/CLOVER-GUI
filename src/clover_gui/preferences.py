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
import yaml

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


from .__utils__ import (
    BaseScreen,
    DEFAULT_GUI_THEME,
    GLOBAL_SETTINGS_FILEPATH,
    LOAD_LOCATION_GEOMETRY,
    RENEWABLES_NINJA_TOKEN,
    SYSTEM_LIFETIME,
    THEME,
)

__all__ = ("PreferencesWindow",)

# Available themes:
#   The list of available themes.
AVAILABLE_THEMES: list[str] = [
    DEFAULT_GUI_THEME,
    "journal",
    "cosmo",
    "minty",
    "darkly",
    "vapor",
]


class PreferencesScreen(BaseScreen, show_navigation=False):
    """
    Represents the preferences window.

    The preferences screen enables a user to set various preferences.

    TODO: Update attributes.

    """

    def __init__(
        self,
        parent,
        renewables_ninja_token: ttk.StringVar,
        select_theme: Callable,
        system_lifetime: ttk.IntVar,
        theme: ttk.StringVar,
    ) -> None:
        """
        Instantiate a :class:`PreferencesScreen` instance.

        :param: parent
            The parent window or frame.

        :param: select_theme
            Function to select the theme.

        :param: renewables_ninja_token
            The renewables.ninja API token for the user.

        :param: system_lifetime
            The lifetime of the system, in years.

        :param: theme
            The current theme.

        """

        super().__init__(parent)

        self.renewables_ninja_token = renewables_ninja_token
        self.select_theme = select_theme
        self.system_lifetime = system_lifetime
        self.theme = theme

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.renewables_ninja_label = ttk.Label(self, text="Renewables ninja API token")
        self.renewables_ninja_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.renewables_ninja_entry = ttk.Entry(
            self,
            textvariable=self.renewables_ninja_token,
        )
        self.renewables_ninja_entry.grid(
            row=0, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.system_lifetime_label = ttk.Label(self, text="System lifetime")
        self.system_lifetime_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.system_lifetime_entry = ttk.Entry(
            self,
            textvariable=self.system_lifetime,
        )
        self.system_lifetime_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.system_lifetime_unit = ttk.Label(self, text="years")
        self.system_lifetime_unit.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        self.theme_label = ttk.Label(self, text="Theme")
        self.theme_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.theme_combobox = ttk.Combobox(
            self, textvariable=self.theme, state=READONLY
        )
        self.theme_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w", ipadx=60)
        self.theme_combobox.bind("<<ComboboxSelected>>", self.combobox_theme_select)
        self.populate_themes()

    def combobox_theme_select(self, _) -> None:
        """Select the theme from the combobox."""

        self.select_theme(self.theme_combobox.get())

    def populate_themes(self) -> None:
        """Populate the combobox with themes."""

        self.theme_combobox["values"] = AVAILABLE_THEMES


class PreferencesWindow(tk.Toplevel):
    """
    Represents the load-location popup window.

    The load-location popup window displays and enables a user to load an existing
    location.

    TODO: Update attributes.

    """

    def __init__(
        self,
        renewables_ninja_token: ttk.StringVar,
        select_theme: Callable,
        system_lifetime: ttk.IntVar,
        theme: str,
    ) -> None:
        """
        Instantiate a :class:`PreferencesWindow` instance.

        :param: select_theme
            Function to select the theme.

        :param: renewables_ninja_token
            The renewables.ninja API token for the user.

        :param: system_lifetime
            The lifetime of the system, in years.

        :param: theme
            The current theme.


        """

        # Instntiate the parent class
        super().__init__()

        self.title("CLOVER-GUI Load Location")

        self.geometry(LOAD_LOCATION_GEOMETRY)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.preferences_label = ttk.Label(
            self, bootstyle=SECONDARY, text="Preferences", font="80"
        )
        self.preferences_label.grid(row=0, column=0, sticky="w", padx=20, pady=5)

        self.preferences_screen = PreferencesScreen(
            self, renewables_ninja_token, select_theme, system_lifetime, theme
        )
        self.preferences_screen.grid(row=1, column=0, padx=20, pady=5, sticky="news")

        self.protocol("WM_DELETE_WINDOW", self.withdraw_and_save)

    def withdraw_and_save(self) -> None:
        """Withdraw and save the window."""

        # Save the configuration.
        with open(
            GLOBAL_SETTINGS_FILEPATH, "w", encoding="utf-8"
        ) as global_settings_file:
            yaml.dump(
                {
                    RENEWABLES_NINJA_TOKEN: self.preferences_screen.renewables_ninja_token.get(),
                    SYSTEM_LIFETIME: self.preferences_screen.system_lifetime.get(),
                    THEME: self.preferences_screen.theme.get(),
                },
                global_settings_file,
            )

        self.withdraw()
