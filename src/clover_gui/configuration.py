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

        self.start_year = tk.DoubleVar()
        self.end_year = tk.DoubleVar()

        self.end_year_slider = ttk.Scale(self, bootstyle="danger")
        self.end_year_slider.grid(row=3, column=1, padx=20)
        self.checkbox_var = tk.BooleanVar()

        self.pv_size_label = ttk.Label(self, text="PV System Size")
        self.pv_size_label.grid(row=1, column=1, sticky="e")
        
        self.pv_size_info = ttk.Label(self, text="kWp")
        self.pv_size_info.grid(row=1, column=3, sticky="w")
        
        self.pv_size_entry = ttk.Entry(self, bootstyle="primary")
        self.pv_size_entry.grid(
            row=1, column=2, padx=10, pady=5, sticky="e", ipadx=80
        )
        
        self.storage_size_label = ttk.Label(self, text="Storage Size")
        self.storage_size_label.grid(row=2, column=1, sticky="e")

        self.storage_size_info = ttk.Label(self, text="kWh")
        self.storage_size_info.grid(row=2, column=3, sticky="w")

        self.storage_size_entry = ttk.Entry(self, bootstyle="primary")
        self.storage_size_entry.grid(
            row=2, column=2, padx=10, pady=5, sticky="e", ipadx=80
        )

        self.simulation_period_label = ttk.Label(self, text="Simulation period")
        self.simulation_period_label.grid(row=3, column=1, sticky="e")

        # self.simulation_period_info = ttk.Label(self, text="Years")
        # self.simulation_period_info.grid(row=3, column=3)

        self.scaler_number = ttk.Label(self, text="")
        self.scaler_number.grid(row=3, column=3, sticky="w")

        def scaler(e):
            self.scaler_number.config(text=f'{int(self.years_slider.get())}')    
        
        self.years_slider = ttk.Scale(self, from_=0, to=30, orient=tk.HORIZONTAL, length=200, command=scaler)
        self.years_slider.grid(row=3, column=2, padx=10, pady=5, ipadx=80, sticky="e")

        self.do_plots_label = ttk.Label(self, text="Generate plots")
        self.do_plots_label.grid(row=4, column=1, sticky="e")
        
        self.checkbox = ttk.Checkbutton(self, variable=self.checkbox_var, bootstyle="round-toggle")
        self.checkbox.grid(row=4, column=2, padx=50)

        self.load_location_button = ttk.Button(
        self, text="Run Simulation", bootstyle=f"{PRIMARY}-outline"
        )
        self.load_location_button.grid(
            row=5, column=3, padx=5, pady=5, ipadx=80, ipady=20
        )        

        
        


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
