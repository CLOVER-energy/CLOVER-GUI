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
    END_YEAR,
    GLOBAL_SETTINGS_FILEPATH,
    LOAD_LOCATION_GEOMETRY,
    MAX_START_YEAR,
    MIN_START_YEAR,
    RENEWABLES_NINJA_TOKEN,
    RENEWABLES_NINJA_DATA_PERIOD,
    START_YEAR,
    SYSTEM_LIFETIME,
    THEME,
)

__all__ = ("PreferencesWindow",)

# Available themes:
#   The list of available themes.
AVAILABLE_THEMES: list[str] = [
    DEFAULT_GUI_THEME,
    # "journal",
    # "cosmo",
    # "minty",
    # "darkly",
    "litera",
    # "vapor",
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
        end_year: ttk.IntVar,
        renewables_ninja_token: ttk.StringVar,
        select_theme: Callable,
        start_year: ttk.IntVar,
        system_lifetime: ttk.IntVar,
        theme: ttk.StringVar,
    ) -> None:
        """
        Instantiate a :class:`PreferencesScreen` instance.

        :param: parent
            The parent window or frame.

        :param: end_year
            The end year for fetching renewables.ninja data.

        :param: renewables_ninja_token
            The renewables.ninja API token for the user.

        :param: select_theme
            Function to select the theme.

        :param: start_year
            The start year for fetching renewables.ninja data.

        :param: system_lifetime
            The lifetime of the system, in years.

        :param: theme
            The current theme.

        """

        super().__init__(parent)

        self.end_year = end_year
        self.renewables_ninja_token = renewables_ninja_token
        self.select_theme = select_theme
        self.start_year = start_year
        self.system_lifetime = system_lifetime
        self.theme = theme

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Renewables ninja settings
        self.renewables_ninja_label_frame = ttk.Labelframe(
            self, text="Renewables ninja settings"
        )
        self.renewables_ninja_label_frame.grid(
            row=0, column=0, sticky="news", padx=20, pady=5
        )

        self.renewables_ninja_label_frame.columnconfigure(0, weight=1)
        self.renewables_ninja_label_frame.columnconfigure(1, weight=1)
        self.renewables_ninja_label_frame.columnconfigure(2, weight=1)

        self.renewables_ninja_label_frame.rowconfigure(0, weight=1)
        self.renewables_ninja_label_frame.rowconfigure(1, weight=1)
        self.renewables_ninja_label_frame.rowconfigure(2, weight=1)
        self.renewables_ninja_label_frame.rowconfigure(3, weight=1)

        # API token
        self.renewables_ninja_label = ttk.Label(
            self.renewables_ninja_label_frame, text="Renewables ninja API token"
        )
        self.renewables_ninja_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        self.renewables_ninja_entry = ttk.Entry(
            self.renewables_ninja_label_frame,
            textvariable=self.renewables_ninja_token,
        )
        self.renewables_ninja_entry.grid(
            row=0, column=1, padx=10, pady=5, sticky="ew", ipadx=65
        )

        # System lifetime
        self.system_lifetime_label = ttk.Label(
            self.renewables_ninja_label_frame, text="System lifetime"
        )
        self.system_lifetime_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.system_lifetime_entry = ttk.Entry(
            self.renewables_ninja_label_frame,
            textvariable=self.system_lifetime,
        )
        self.system_lifetime_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew", ipadx=65
        )

        self.system_lifetime_unit = ttk.Label(
            self.renewables_ninja_label_frame, text="years"
        )
        self.system_lifetime_unit.grid(row=1, column=2, sticky="w", padx=10, pady=5)

        # Start year
        self.start_year_label = ttk.Label(
            self.renewables_ninja_label_frame, text="Solar data start year"
        )
        self.start_year_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        def update_end_year():
            self.end_year.set(self.start_year.get() + RENEWABLES_NINJA_DATA_PERIOD)
            self.end_year_entry.update()

        def scalar_start_year(_):
            self.start_year.set(
                max(min(self.start_year.get(), MAX_START_YEAR), MIN_START_YEAR)
            )
            self.start_year_entry.update()
            update_end_year()

        self.start_year_slider = ttk.Scale(
            self.renewables_ninja_label_frame,
            from_=MIN_START_YEAR,
            to=MAX_START_YEAR,
            orient=ttk.HORIZONTAL,
            command=scalar_start_year,
            # bootstyle=WARNING,
            variable=self.start_year,
        )
        self.start_year_slider.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        def enter_start_year(_):
            self.start_year.set(self.start_year_entry.get())
            self.start_year_slider.set(self.start_year.get())
            update_end_year()

        self.start_year_entry = ttk.Entry(
            self.renewables_ninja_label_frame,
            # bootstyle=WARNING,
            textvariable=self.start_year,
        )

        self.start_year_entry.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
        self.start_year_entry.bind("<Return>", enter_start_year)

        # End year
        self.end_year_label = ttk.Label(
            self.renewables_ninja_label_frame, text="Solar data end year"
        )
        self.end_year_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        def update_start_year():
            self.start_year.set(self.end_year.get() - RENEWABLES_NINJA_DATA_PERIOD)
            self.start_year_entry.update()

        def scalar_end_year(_):
            self.end_year.set(
                max(
                    min(
                        self.end_year.get(),
                        MAX_START_YEAR + RENEWABLES_NINJA_DATA_PERIOD,
                    ),
                    MIN_START_YEAR + RENEWABLES_NINJA_DATA_PERIOD,
                )
            )
            self.end_year_entry.update()
            update_start_year()

        self.end_year_slider = ttk.Scale(
            self.renewables_ninja_label_frame,
            from_=MIN_START_YEAR + RENEWABLES_NINJA_DATA_PERIOD,
            to=MAX_START_YEAR + RENEWABLES_NINJA_DATA_PERIOD,
            orient=ttk.HORIZONTAL,
            command=scalar_end_year,
            # bootstyle=WARNING,
            variable=self.end_year,
        )
        self.end_year_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        def enter_end_year(_):
            self.end_year.set(self.end_year_entry.get())
            self.end_year_slider.set(self.end_year.get())
            update_start_year()

        self.end_year_entry = ttk.Entry(
            self.renewables_ninja_label_frame,
            # bootstyle=WARNING,
            textvariable=self.end_year,
        )

        self.end_year_entry.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
        self.end_year_entry.bind("<Return>", enter_end_year)

        # Graphical user settings
        self.graphical_label_frame = ttk.Labelframe(self, text="GUI preferences")
        self.graphical_label_frame.grid(
            row=1, column=0, sticky="news", padx=20, pady=10
        )

        self.graphical_label_frame.rowconfigure(0, weight=1)

        self.graphical_label_frame.columnconfigure(0, weight=1)
        self.graphical_label_frame.columnconfigure(1, weight=1)
        self.graphical_label_frame.columnconfigure(2, weight=1)

        self.theme_label = ttk.Label(self.graphical_label_frame, text="Theme")
        self.theme_label.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        self.theme_combobox = ttk.Combobox(
            self.graphical_label_frame, textvariable=self.theme, state=READONLY
        )
        self.theme_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w", ipadx=60)
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
        end_year: ttk.IntVar,
        renewables_ninja_token: ttk.StringVar,
        select_theme: Callable,
        start_year: ttk.IntVar,
        system_lifetime: ttk.IntVar,
        theme: str,
    ) -> None:
        """
        Instantiate a :class:`PreferencesWindow` instance.

        :param: end_year
            The end year for fetching renewables.ninja data.

        :param: renewables_ninja_token
            The renewables.ninja API token for the user.

        :param: select_theme
            Function to select the theme.

        :param: start_year
            The start year for fetching renewables.ninja data.

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
            self,
            end_year,
            renewables_ninja_token,
            select_theme,
            start_year,
            system_lifetime,
            theme,
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
                    END_YEAR: self.preferences_screen.end_year.get(),
                    RENEWABLES_NINJA_TOKEN: self.preferences_screen.renewables_ninja_token.get(),
                    START_YEAR: self.preferences_screen.start_year.get(),
                    SYSTEM_LIFETIME: self.preferences_screen.system_lifetime.get(),
                    THEME: self.preferences_screen.theme.get(),
                },
                global_settings_file,
            )

        self.withdraw()
