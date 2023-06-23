#!/usr/bin/python3.10
########################################################################################
# __init__.py - The init module for CLOVER-GUI application.                            #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import tkinter as tk

import ttkbootstrap as ttk

from typing import Callable

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen

__all__ = ("ConfigurationScreen",)


class ConfigurationFrame(ttk.Frame):
    """
    Represents the configuration frame.

    The configure frame contains toggles for configuration top-level settings for each
    run.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Configuration frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class SimulationFrame(BaseScreen, show_navigation=False):
    """
    Represents the simulation frame.

    The simulation frame contains the necessary parameters needed to launch a simulation
    in CLOVER as well as a launch button for initiating the run.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)

        self.start_year = tk.DoubleVar()
        self.end_year = tk.DoubleVar()

        self.end_year_slider = ttk.Scale(self, bootstyle="danger")
        self.end_year_slider.grid(row=3, column=1, padx=20)

        # TODO: Add configuration frame widgets and layout


class OptimisationFrame(ttk.Frame):
    """
    Represents the optimisation frame.

    The optimisation frame contains the launch parameters needed for launching an
    optimisation in CLOVER as well as a launch button for initiating the run.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        # TODO: Add configuration frame widgets and layout


class ConfigurationScreen(BaseScreen, show_navigation=True):
    """
    Represents the configuration screen.

    The configure screen contains tabbed information for configuring the screen.

    TODO: Update attributes.

    """

    def __init__(self, open_details_window: Callable) -> None:
        """
        Instantiate a :class:`ConfigureFrame` instance.

        :param: open_details_window
            A callable function to open the details screen.

        """

        super().__init__()

        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.location_label = ttk.Label(
            self, bootstyle=INFO, text="LOCATION NAME", font="80"
        )
        self.location_label.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=60, pady=20
        )

        self.configuration_notebook = ttk.Notebook(self, bootstyle=f"{INFO}")
        self.configuration_notebook.grid(
            row=1, column=0, columnspan=2, sticky="nsew", padx=60, pady=20
        )  # Use grid

        style = ttk.Style()
        style.configure("TNotebook.Tab", width=int(self.winfo_screenwidth() / 4))

        self.configuration_frame = ConfigurationFrame(self.configuration_notebook)
        self.configuration_notebook.add(
            self.configuration_frame, text="Configure", sticky="news"
        )

        self.simulation_frame = SimulationFrame(self.configuration_notebook)
        self.configuration_notebook.add(self.simulation_frame, text="Simulate")

        self.optimisation_frame = OptimisationFrame(self.configuration_notebook)
        self.configuration_notebook.add(self.optimisation_frame, text="Optimise")

        self.advanced_settings_button = ttk.Button(
            self, bootstyle=INFO, text="Advanced settings", command=open_details_window
        )
        self.advanced_settings_button.grid(
            row=2, column=1, sticky="w", pady=20, ipadx=80, ipady=20
        )
