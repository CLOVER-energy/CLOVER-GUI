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

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=3)
        self.columnconfigure(4, weight=1)

        self.start_year = tk.DoubleVar()
        self.end_year = tk.DoubleVar()

        # self.end_year_slider = ttk.Scale(self, bootstyle="danger")
        # self.end_year_slider.grid(row=3, column=1, padx=20)
        self.checkbox_var = tk.BooleanVar()

        # PV size
        self.pv_size_label = ttk.Label(self, text="PV System Size")
        self.pv_size_label.grid(row=1, column=0, columnspan=3, sticky="e")

        self.pv_size_entry = ttk.Entry(self, bootstyle=INFO)
        self.pv_size_entry.grid(row=1, column=3, padx=10, pady=5, sticky="e", ipadx=80)

        self.pv_size_info = ttk.Label(self, text="kWp")
        self.pv_size_info.grid(row=1, column=4, sticky="w")

        # Storage size
        self.storage_size_label = ttk.Label(self, text="Storage Size")
        self.storage_size_label.grid(row=2, column=0, columnspan=3, sticky="e")

        self.storage_size_entry = ttk.Entry(self, bootstyle=INFO)
        self.storage_size_entry.grid(
            row=2, column=3, padx=10, pady=5, sticky="e", ipadx=80
        )

        # Simulation period
        self.simulation_period_label = ttk.Label(self, text="Simulation period")
        self.simulation_period_label.grid(row=3, column=0, columnspan=3, sticky="e")
        self.simulation_period = ttk.IntVar(self, 20, "simulation_period")

        # self.simulation_period_info = ttk.Label(self, text="Years")
        # self.simulation_period_info.grid(row=3, column=3)

        self.scaler_number = ttk.Label(
            self, text=f"{int(self.simulation_period.get())} years"
        )
        self.scaler_number.grid(row=3, column=4, sticky="w")

        def scaler(e):
            self.scaler_number.config(
                text=f"{' ' * (int(self.years_slider.get()) < 10)}{int(self.years_slider.get())} years"
            )

        self.years_slider = ttk.Scale(
            self,
            from_=0,
            to=30,
            orient=tk.HORIZONTAL,
            length=320,
            command=scaler,
            bootstyle=INFO,
            variable=self.simulation_period,
        )
        self.years_slider.grid(row=3, column=3, padx=10, pady=5, sticky="e")

        # Generate plots
        self.do_plots_label = ttk.Label(self, text="Generate plots")
        self.do_plots_label.grid(row=4, column=0, columnspan=3, sticky="e")

        self.checkbox = ttk.Checkbutton(
            self, variable=self.checkbox_var, bootstyle=f"round-toggle-{INFO}"
        )
        self.checkbox.grid(row=4, column=3, padx=50)

        self.load_location_button = ttk.Button(
            self, text="Run Simulation", bootstyle=f"{INFO}-outline"
        )
        self.load_location_button.grid(
            row=5, column=3, columnspan=2, padx=5, pady=5, ipadx=80, ipady=20
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
        self.pack(fill="both", expand=True)

        # Set the physical distance weights of the rows and columns
        self.rowconfigure(0, weight=1)  # First row has the header
        self.rowconfigure(1, weight=1)  # These rows have entries
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)
        self.rowconfigure(7, weight=1)
        self.rowconfigure(8, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=3)
        self.columnconfigure(4, weight=1)
    

        # Optimisation Min/Max set
        self.optimisation_minmax_label = ttk.Label(self, text="the")
        self.optimisation_minmax_label.grid(row=2, column=1, padx=10, pady=5, sticky="nw")

        self.optimisation_minmax = ttk.StringVar(self, "Minimise", "Minimum/Maximum")
        self.optimisation_minmax_entry = ttk.Combobox(
            self, bootstyle=INFO, textvariable=self.optimisation_minmax
        )
        self.optimisation_minmax_entry.grid(
            row=2, column=0, padx=10, pady=5, sticky="nw", ipadx=60
        )
        self.populate_minmax()

        # Optimisation criterion set
        self.optimisation_criterion_label = ttk.Label(self, text="Optimisation Criterion")
        self.optimisation_criterion_label.grid(row=1, column=0, padx=10, pady=5, sticky="nw")

        self.optimisation_criterion = ttk.StringVar(self, "LCUE", "Optimisation Criterion")
        self.optimisation_criterion_entry = ttk.Combobox(
            self, bootstyle=INFO, textvariable=self.optimisation_criterion
        )
        self.optimisation_criterion_entry.grid(
            row=2, column=2, padx=10, pady=5, sticky="nw", ipadx=60
        )
        self.populate_available_optimisation_criterion()

        # Threshold criterion set
        self.threshold_criterion_label = ttk.Label(self, text="Threshold Criteria")
        self.threshold_criterion_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.add_threshold_var = tk.BooleanVar()
        self.add_threshold = ttk.Checkbutton(self, bootstyle="info-toolbutton", 
                                                 variable=self.add_threshold_var,
                                                   text='Add')

        self.add_threshold.grid(row=4, column=4, padx=10, pady=5, 
                                           sticky="w", ipadx=80)
        
        
        self.threshold_criterion = ttk.StringVar(self, "Unmet energy fraction", "Threshold Criterion")
        self.threshold_criterion_entry = ttk.Combobox(
            self, bootstyle=INFO, textvariable=self.threshold_criterion
        )
        self.threshold_criterion_entry.grid(
        row=5, column=0, padx=10, pady=5, ipadx=60
        )

        self.populate_threshold_criteria()

        self.chevrons = ttk.StringVar(self, ">", ">/<")
        self.chevrons_entry = ttk.Combobox(
            self, bootstyle=INFO, textvariable=self.chevrons
        )        
        self.chevrons_entry.grid(row=5, column=1, padx=10, pady=5, sticky='w', ipadx=60)

        self.populate_chevrons()
        
        self.threshold_value = ttk.IntVar(self, 0.05, "threshold_value")
        self.threshold_entry = ttk.Entry(self, bootstyle=INFO, textvariable=self.threshold_value)
        self.threshold_entry.grid(
            row=5, column=2, padx=10, pady=5, sticky="w", ipadx=80
        )

        # Second threshold criteria
        self.threshold_criterion_2 = ttk.StringVar(self, "", "Threshold Criterion 2")
        self.threshold_criterion_entry_2 = ttk.Combobox(
            self, bootstyle=INFO, textvariable=self.threshold_criterion_2
        )
        self.threshold_criterion_entry_2.grid(
        row=6, column=0, padx=10, pady=5, ipadx=60
        )

        self.populate_threshold_criteria_2()

        self.chevrons_2 = ttk.StringVar(self, ">", ">/<_2")
        self.chevrons_entry_2 = ttk.Combobox(
            self, bootstyle=INFO, textvariable=self.chevrons
        )        
        self.chevrons_entry_2.grid(row=6, column=1, padx=10, pady=5, sticky='w', ipadx=60)
        self.populate_chevrons_2()

        self.threshold_value_2 = ttk.IntVar(self, "", "threshold_value_2")
        self.threshold_entry_2 = ttk.Entry(self, bootstyle=INFO, textvariable=self.threshold_value_2)
        self.threshold_entry_2.grid(
            row=6, column=2, padx=10, pady=5, sticky="w", ipadx=80
        )
        self.threshold_2_click_var = tk.BooleanVar()
        self.threshold_2_click = ttk.Checkbutton(self, bootstyle="danger-toolbutton", 
                                                 variable=self.threshold_2_click_var,
                                                   text='Remove')

        self.threshold_2_click.grid(row=6, column=4, padx=10, pady=5, 
                                           sticky="w", ipadx=80)



    def populate_available_optimisation_criterion(self) -> None:
        """Populate the combo box with the set of avialable batteries."""
        
        self.optimisation_criterion_entry["values"] = [
        "LCUE ($/kWh)",
        "Emissions intensity (gCO2/kWh)",
        "Unmet energy fraction",
        "Blackouts",
        "Clean water blackouts",
        "Cumulative cost ($)",
        "Cumulative ghgs (kgCO2eq)",
        "Cumulative system cost ($)",
        "Cumulative system ghgs (kgCO2eq)",
        "Total_cost ($)",
        "Total system cost ($)",
        "Total ghgs (kgCO2eq)",
        "Total system ghgs (kgCO2eq)",
        "Kerosene cost mitigated ($)",
        "Kerosene ghgsm mitigated (kgCO2eq)",
        "Renewables fraction"
        ]
    
    def populate_minmax(self) -> None:
        """Populate the combo box with minmax."""
    
        self.optimisation_minmax_entry["values"] = [
        "Minimise",
        "Maximise",
    ]

    def populate_threshold_criteria(self) -> None:
        """Populate the combo box with threshold criteria."""

        self.threshold_criterion_entry["values"] = [
        "LCUE ($/kWh)",
        "Emissions intensity (gCO2/kWh) (Max)",
        "Unmet energy fraction",
        "Blackouts (Max)",
        "Clean water blackouts (Max)",
        "Cumulative cost ($) (Max)",
        "Cumulative ghgs (kgCO2eq) (Max)",
        "Cumulative system cost ($) (Max)",
        "Cumulative system ghgs (kgCO2eq)",
        "Total_cost ($) (Max)",
        "Total system cost ($) (Max)",
        "Total ghgs (kgCO2eq) (Max)",
        "Total system ghgs (kgCO2eq) (Max)",
        "Kerosene cost mitigated ($) (Min)",
        "Kerosene ghgsm mitigated (kgCO2eq) (Min)",
        "Renewables fraction (Min)"
        ]
    
    def populate_threshold_criteria_2(self) -> None:
        """Populate the combo box with threshold criteria."""

        self.threshold_criterion_entry_2["values"] = [
        "LCUE ($/kWh)",
        "Emissions intensity (gCO2/kWh) (Max)",
        "Unmet energy fraction",
        "Blackouts (Max)",
        "Clean water blackouts (Max)",
        "Cumulative cost ($) (Max)",
        "Cumulative ghgs (kgCO2eq) (Max)",
        "Cumulative system cost ($) (Max)",
        "Cumulative system ghgs (kgCO2eq)",
        "Total_cost ($) (Max)",
        "Total system cost ($) (Max)",
        "Total ghgs (kgCO2eq) (Max)",
        "Total system ghgs (kgCO2eq) (Max)",
        "Kerosene cost mitigated ($) (Min)",
        "Kerosene ghgsm mitigated (kgCO2eq) (Min)",
        "Renewables fraction (Min)"
        ]
    
    def populate_chevrons(self) -> None:
        """Populate the combo box with less than more than chevrons."""
        self.chevrons_entry["values"] = [
        ">",
        "<"
        ]
    
    def populate_chevrons_2(self) -> None:
        """Populate the combo box with less than more than chevrons."""
        self.chevrons_entry_2["values"] = [
        ">",
        "<"
        ]


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
