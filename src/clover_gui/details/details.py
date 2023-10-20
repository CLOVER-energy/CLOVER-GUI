#!/usr/bin/python3.10
########################################################################################
# details.py - The details module for CLOVER-GUI application.                          #
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

from ..__utils__ import DETAILS_GEOMETRY

__all__ = ("DetailsWindow",)

from .conversion import ConversionFrame
from .diesel import DieselFrame
from .finance import FinanceFrame
from .ghgs import GHGFrame
from .grid import GridFrame
from .load import LoadFrame
from .storage import StorageFrame
from .solar import SolarFrame
from .system import SystemFrame
from .transmission import TransmissionFrame
from .wind import WindFrame


class DetailsWindow(tk.Toplevel):
    """
    Represents the details window.

    The details window contains tabs for inputting more precise information into the
    application.

    TODO: Update attributes.

    """

    def __init__(
        self,
        add_battery_to_scenario_frame,
        add_diesel_generator_to_scenario_frame,
        add_grid_profile_to_scenario_frame,
        add_pv_panel_to_scenario_frame,
        data_directory: str,
        renewables_ninja_token: ttk.StringVar,
        save_configuration: Callable,
        set_batteries_on_scenario_frame,
        set_diesel_generators_on_scenario_frame,
        set_grid_profiles_on_scenario_frame,
        set_pv_panels_on_scenario_frame,
        system_lifetime: ttk.IntVar,
    ) -> None:
        """
        Instantiate a :class:`DetailsWindow` instance.

        :param: add_battery_to_scenario_frame
            Add a new battery to the combobox on the scenarios frame.

        :param: add_diesel_generator_to_scenario_frame
            Add a new diesel generator to the combobox on the scenarios frame.

        :param: add_grid_profile_to_scenario_frame
            Add a new grid profile to the combobox on the scenarios frame.

        :param: add_pv_panel_to_scenario_frame
            Add a new PV panel to the combobox on the scenarios frame.

        :param: data_directory
            The name of the data directory.

        :param: renewables_ninja_token
            The renewables.ninja API token for the user.

        :param: save_configuration
            Function for saving the configuration.

        :param: set_batteries_on_scenario_frame,
            Set the batteries on the scenarios frame.

        :param: set_diesel_generators_on_scenario_frame,
            Set the diesel generators on the scenarios frame.

        :param: set_grid_profiles_on_scenario_frame,
            Set the grid profiles panels on the scenarios frame.

        :param: set_pv_panels_on_scenario_frame,
            Set the PV panels on the scenarios frame.

        :param: system_lifetime
            The lifetime of the system.

        """

        super().__init__()

        self.title("CLOVER-GUI Details")

        self.system_lifetime = system_lifetime
        self.save_configuration = save_configuration

        self.geometry(DETAILS_GEOMETRY)

        self.protocol("WM_DELETE_WINDOW", self.save_and_close)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1, minsize=100)
        self.rowconfigure(1, weight=6)

        self.details_label = ttk.Label(
            self,
            bootstyle=INFO,
            text="Detailed settings",
            font=("TkDefaultFont", "16", "bold"),
        )
        self.details_label.grid(row=0, column=0, sticky="w", padx=20, pady=5, ipady=20)

        self.save_and_close_button = ttk.Button(
            self,
            bootstyle="info.Outline.TButton",
            text="Save and Close",
            command=self.save_and_close,
        )
        self.save_and_close_button.grid(
            row=0, column=1, sticky="e", padx=20, pady=5, ipadx=20, ipady=10
        )

        self.notebook_style = ttk.Style()
        # self.notebook_style.configure(
        #     (details_notebook_style_name := "Details.TNotebook.Tab"),
        #     font=("TkDefaultFont", "14"),
        # )

        # Define the base style
        self.notebook_style.configure(
            "Details.TNotebook.Tab",
            font=("TkDefaultFont", "12"),
            width=int(self.winfo_screenwidth() / 8),
            **{"tabbar.font": ("TkDefaultFont", 14), "tabbar.foreground": "blue"},
        )

        self.details_notebook = ttk.Notebook(
            self, bootstyle=f"{SECONDARY}"  # , style="Details.TNotebook.Tab"
        )
        self.details_notebook.grid(
            row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=5
        )

        self.solar_frame = SolarFrame(
            self.details_notebook, data_directory, renewables_ninja_token
        )
        self.details_notebook.add(
            self.solar_frame,
            text="Solar",
            sticky="news",
        )

        # self.wind_frame = WindFrame(self.details_notebook)
        # self.details_notebook.add(
        #     self.wind_frame, text="Wind", sticky="news", state=DISABLED
        # )

        self.storage_frame = StorageFrame(self.details_notebook)
        self.details_notebook.add(self.storage_frame, text="Storage", sticky="news")

        self.load_frame = LoadFrame(self.details_notebook)
        self.details_notebook.add(self.load_frame, text="Load", sticky="news")

        # self.conversion_frame = ConversionFrame(self.details_notebook)
        # self.details_notebook.add(
        #     self.conversion_frame, text="Convert", sticky="news", state=DISABLED
        # )

        # self.transmission_frame = TransmissionFrame(self.details_notebook)
        # self.details_notebook.add(
        #     self.transmission_frame, text="Transmit.", sticky="news", state=DISABLED
        # )

        self.diesel_frame = DieselFrame(self.details_notebook)
        self.details_notebook.add(self.diesel_frame, text="Diesel", sticky="news")

        self.grid_frame = GridFrame(self.details_notebook)
        self.details_notebook.add(self.grid_frame, text="Grid", sticky="news")

        self.finance_frame = FinanceFrame(self.details_notebook)
        self.details_notebook.add(self.finance_frame, text="Finance", sticky="news")

        self.ghgs_frame = GHGFrame(self.details_notebook)
        self.details_notebook.add(self.ghgs_frame, text="GHGs", sticky="news")

        self.system_frame = SystemFrame(self.details_notebook)
        self.details_notebook.add(self.system_frame, text="System", sticky="news")

        # Update the various frames with the add-panel functions.
        self.solar_frame.pv_frame.add_panel_to_scenario_frame = (
            add_pv_panel_to_scenario_frame
        )
        self.storage_frame.battery_frame.add_battery_to_scenario_frame = (
            add_battery_to_scenario_frame
        )
        self.diesel_frame.generator_frame.add_generator_to_scenario_frame = (
            add_diesel_generator_to_scenario_frame
        )
        self.grid_frame.add_grid_profile_to_scenario_frame = (
            add_grid_profile_to_scenario_frame
        )

        # Update the various frames with the set-panel functions.
        self.solar_frame.pv_frame.set_panels_on_system_frame = (
            set_pv_panels_on_scenario_frame
        )
        self.storage_frame.battery_frame.set_batteries_on_system_frame = (
            set_batteries_on_scenario_frame
        )
        self.diesel_frame.generator_frame.set_generators_on_system_frame = (
            set_diesel_generators_on_scenario_frame
        )
        self.grid_frame.set_profiles_on_system_frame = (
            set_grid_profiles_on_scenario_frame
        )

    def save_and_close(self) -> None:
        """Actioned when closed."""

        # Save all of the variables from the details screen.
        self.save_configuration()

        self.withdraw()
