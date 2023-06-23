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

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen

__all__ = "ConfigurationScreen"


class ConfigurationFrame(ttk.Frame):
    """
    Represents the configuration frame.

    The configure frame contains toggles for configuration top-level settings for each
    run.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        # TODO: Add configuration frame widgets and layout


class SimulationFrame(ttk.Frame):
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

        self.start_year = tk.DoubleVar()
        self.end_year = tk.DoubleVar()

        # self.years_slider.grid(parent, row=3, column=1, padx=20)

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

    def __init__(
        self,
    ) -> None:
        """
        Instantiate a :class:`ConfigureFrame` instance.

        """

        super().__init__()

        self.pack(fill="both", expand=True)

        self.configuration_notebook = ttk.Notebook(self, bootstyle=f"{INFO}")

        style = ttk.Style()
        style.configure("TNotebook.Tab", width=int(self.winfo_screenwidth() / 4))

        self.configuration_frame = ConfigurationFrame(self.configuration_notebook)
        self.configuration_notebook.add(self.configuration_frame, text="Configure")

        self.simulation_frame = SimulationFrame(self.configuration_notebook)
        self.configuration_notebook.add(self.simulation_frame, text="Simulate")

        self.optimisation_frame = OptimisationFrame(self.configuration_notebook)
        self.configuration_notebook.add(self.optimisation_frame, text="Optimise")

        self.configuration_notebook.pack(fill="both", expand=True, padx=60, pady=40)
