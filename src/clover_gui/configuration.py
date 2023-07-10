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

from dataclasses import dataclass

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
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        self.start_year = tk.DoubleVar()
        self.end_year = tk.DoubleVar()

        # self.end_year_slider = ttk.Scale(self, bootstyle="danger")
        # self.end_year_slider.grid(row=3, column=1, padx=20)
        self.checkbox_var = tk.BooleanVar()

        # PV size
        self.pv_size_label = ttk.Label(self, text="PV System Size")
        self.pv_size_label.grid(row=1, column=1, sticky="e")

        self.pv_size_entry = ttk.Entry(self, bootstyle=INFO)
        self.pv_size_entry.grid(row=1, column=2, padx=10, pady=5, sticky="e", ipadx=80)

        self.pv_size_info = ttk.Label(self, text="kWp")
        self.pv_size_info.grid(row=1, column=3, sticky="w")

        # Storage size
        self.storage_size_label = ttk.Label(self, text="Storage Size")
        self.storage_size_label.grid(row=2, column=1, sticky="e")

        self.storage_size_entry = ttk.Entry(self, bootstyle=INFO)
        self.storage_size_entry.grid(
            row=2, column=2, padx=10, pady=5, sticky="e", ipadx=80
        )
        self.storage_size_info = ttk.Label(self, text="kWh")
        self.storage_size_info.grid(row=2, column=3, sticky="w")

        # Simulation period
        self.simulation_period_label = ttk.Label(self, text="Simulation period")
        self.simulation_period_label.grid(row=3, column=1, sticky="e")
        self.simulation_period = ttk.IntVar(self, 20, "simulation_period")

        # self.simulation_period_info = ttk.Label(self, text="Years")
        # self.simulation_period_info.grid(row=3, column=3)

        self.scaler_number = ttk.Label(
            self, text=f"{int(self.simulation_period.get())} years"
        )
        self.scaler_number.grid(row=3, column=3, sticky="w")

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
        self.years_slider.grid(row=3, column=2, padx=10, pady=5, sticky="e")

        # Generate plots
        self.do_plots_label = ttk.Label(self, text="Generate plots")
        self.do_plots_label.grid(row=4, column=1, sticky="e")

        self.checkbox = ttk.Checkbutton(
            self, variable=self.checkbox_var, bootstyle=f"round-toggle-{INFO}"
        )
        self.checkbox.grid(row=4, column=2, padx=50, sticky="e")

        self.load_location_button = ttk.Button(
            self, text="Run Simulation", bootstyle=f"{INFO}-outline"
        )
        self.load_location_button.grid(
            row=5, column=3, columnspan=2, padx=5, pady=5, ipadx=80, ipady=20
        )

        # TODO: Add configuration frame widgets and layout


@dataclass
class ThresholdCriterion:
    """
    Represents a threshold criterion.

    .. attribute:: criterion_name
        The name of the criterion.

    .. attribute:: less_than
        Whether to use a less-than (True) or greater-than (False) condition for the
        criterion.

    .. attribute:: value
        The threshold value for the criterion.

    """

    criterion_name: ttk.StringVar
    less_than: ttk.BooleanVar
    value: ttk.DoubleVar


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
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
    

        # Optimisation criterion frame
        self.optimisation_criterion_frame = ttk.Labelframe(
            self, style="info.TLabelframe", text="Optimisation criterion"
        )
        self.optimisation_criterion_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=10,
            ipady=40,
            ipadx=20,
            sticky="news",
        )

        self.optimisation_criterion_frame.rowconfigure(0, weight=1)

        self.optimisation_criterion_frame.columnconfigure(0, weight=3)
        self.optimisation_criterion_frame.columnconfigure(1, weight=1)
        self.optimisation_criterion_frame.columnconfigure(2, weight=3)

        # Optimisation Min/Max set
        self.optimisation_minmax = ttk.StringVar(self, "Minimise", "Minimum/Maximum")
        self.optimisation_minmax_entry = ttk.Combobox(
            self.optimisation_criterion_frame,
            bootstyle=INFO,
            textvariable=self.optimisation_minmax,
        )
        self.optimisation_minmax_entry.grid(
            row=0, column=0, padx=10, pady=5, sticky="ew", ipadx=100
        )
        self.populate_minmax()

        # the
        self.optimisation_minmax_label = ttk.Label(
            self.optimisation_criterion_frame, text="the"
        )
        self.optimisation_minmax_label.grid(
            row=0, column=1, padx=10, pady=5, sticky="ew"
        )

        # Optimisation criterion set
        self.optimisation_criterion = ttk.StringVar(
            self, "LCUE", "Optimisation Criterion"
        )
        self.optimisation_criterion_entry = ttk.Combobox(
            self.optimisation_criterion_frame,
            bootstyle=INFO,
            textvariable=self.optimisation_criterion,
        )
        self.optimisation_criterion_entry.grid(
            row=0, column=2, padx=10, pady=5, sticky="ew", ipadx=100
        )
        self.populate_available_optimisation_criterion()

        # Threshold criteria frame
        self.threshold_criteria_frame = ttk.Labelframe(
            self, style="info.TLabelframe", text="Threshold criteria"
        )
        self.threshold_criteria_frame.grid(
            row=1,
            column=0,
            padx=5,
            pady=10,
            ipady=200,
            ipadx=20,
            sticky="news",
        )

        self.threshold_criteria_frame.columnconfigure(0, weight=1)
        self.threshold_criteria_frame.columnconfigure(1, weight=1)
        self.threshold_criteria_frame.columnconfigure(2, weight=1)
        self.threshold_criteria_frame.columnconfigure(3, weight=1)

        self.threshold_criteria_frame.rowconfigure(0, weight=1)
        self.threshold_criteria_frame.rowconfigure(1, weight=8)

        threshold_criteria: list[ThresholdCriterion] = []

        def add_threshold_criterion() -> None:
            """Add a new threshold criterion to the list."""
            pass

        self.add_threshold_criterion_button = ttk.Button(
            self.threshold_criteria_frame,
            bootstyle=INFO,
            command=add_threshold_criterion,
            text="Add threshold criterion",
        )
        self.add_threshold_criterion_button.grid(
            row=0, column=0, padx=10, pady=5, sticky="w", ipadx=40
        )

        # Create the scrollable frame for threshold criteria
        self.scrollable_frame = ScrolledFrame(self.threshold_criteria_frame)
        self.scrollable_frame.grid(
            row=1,
            column=0,
            columnspan=4,
            padx=10,
            pady=5,
            sticky="ew",
            ipadx=10,
            ipady=80,
        )

        # Iterations
        self.iterations_label = ttk.Label(self, text="")
        self.iterations_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        # Iteration length
        self.iteration_length_label = ttk.Label(self, text='Iteration Length')
        self.iteration_length_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.iteration_length = ttk.DoubleVar(self, "5.0")
        self.iteration_length_entry = ttk.Entry(
            self,bootstyle=INFO, textvariable=self.iteration_length
        )
        self.iteration_length_entry.grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.iteration_length_units = ttk.Label(self, text="Years")
        self.iteration_length_units.grid(row=8, column=2, padx=10, pady=5, sticky="w")

        # Number iterations
        self.no_iterations_label = ttk.Label(self, text="Number of iterations")
        self.no_iterations_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        self.no_iteration = ttk.IntVar(self, 1)
        self.no_iteration_entry = ttk.Entry(
            self,bootstyle=INFO, textvariable=self.no_iteration
        )
        self.no_iteration_entry.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        #Step sizes
        self.steps_label = ttk.Label(self, text="")
        self.steps_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")

        # PV step size
        self.pv_step_label = ttk.Label(self, text="PV step size")
        self.pv_step_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")

        self.pv_min_label = ttk.Label(self, text="min")
        self.pv_min_label.grid(row=11, column=0, padx=10, pady=5, sticky="e")
        
        self.pv_min = ttk.IntVar(self, 5)
        self.pv_min_entry = ttk.Entry(
            self,bootstyle=INFO, textvariable=self.pv_min
        )
        self.pv_min_entry.grid(row=11, column=1, padx=10, pady=5, sticky="w")

        self.pv_max_label = ttk.Label(self, text="max")
        self.pv_max_label.grid(row=11, column=1, padx=10, pady=5, sticky="e")
        
        self.pv_max = ttk.IntVar(self, 20)
        self.pv_max_entry = ttk.Entry(
            self,bootstyle=INFO, textvariable=self.pv_max
        )
        self.pv_max_entry.grid(row=11, column=2, padx=10, pady=5, sticky="w")
        
        self.pv_step_num_label = ttk.Label(self, text="step")
        self.pv_step_num_label.grid(row=11, column=2, padx=10, pady=5, sticky="e")
        self.pv_step_num = ttk.IntVar(self, 5)

        self.pv_step_num_entry = ttk.Entry(
            self,bootstyle=INFO, textvariable=self.pv_step_num
        )
        self.pv_step_num_entry.grid(row=11, column=3, padx=10, pady=5, sticky="w")


        # Storage step size
        self.storage_step_label = ttk.Label(self, text="Storage step size")
        self.storage_step_label.grid(row=12, column=0, padx=10, pady=5, sticky="w")

        self.storage_min_label = ttk.Label(self, text="min")
        self.storage_min_label.grid(row=12, column=0, padx=10, pady=5, sticky="e")
        
        self.storage_min = ttk.IntVar(self, 5)
        self.storage_min_entry = ttk.Entry(
            self,bootstyle=INFO, textvariable=self.storage_min
        )
        self.storage_min_entry.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        self.storage_max_label = ttk.Label(self, text="max")
        self.storage_max_label.grid(row=12, column=1, padx=10, pady=5, sticky="e")
        
        self.storage_max = ttk.IntVar(self, 30)
        self.storage_max_entry = ttk.Entry(
            self,bootstyle=INFO, textvariable=self.storage_max
        )
        self.storage_max_entry.grid(row=12, column=2, padx=10, pady=5, sticky="w")
        
        self.storage_step_num_label = ttk.Label(self, text="step")
        self.storage_step_num_label.grid(row=12, column=2, padx=10, pady=5, sticky="e")
        self.storage_step_num = ttk.IntVar(self, 5)

        self.storage_step_num_entry = ttk.Entry(
            self,bootstyle=INFO, textvariable=self.pv_step_num
        )
        self.storage_step_num_entry.grid(row=12, column=3, padx=10, pady=5, sticky="w")
        



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
            "Renewables fraction",
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
            "Renewables fraction (Min)",
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
            "Renewables fraction (Min)",
        ]

    def populate_chevrons(self) -> None:
        """Populate the combo box with less than more than chevrons."""
        self.chevrons_entry["values"] = [">", "<"]

    def populate_chevrons_2(self) -> None:
        """Populate the combo box with less than more than chevrons."""
        self.chevrons_entry_2["values"] = [">", "<"]


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
