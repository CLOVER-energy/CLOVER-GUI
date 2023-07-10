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

import math
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

        self.scalerber = ttk.Label(
            self, text=f"{int(self.simulation_period.get())} years"
        )
        self.scalerber.grid(row=3, column=3, sticky="w")

        def scaler(e):
            self.scalerber.config(
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

    def __init__(self, parent, system_lifetime: ttk.IntVar):
        super().__init__(parent)

        self.system_lifetime = system_lifetime

        # TODO: Add configuration frame widgets and layout
        self.pack(fill="both", expand=True)

        # Set the physical distance weights of the rows and columns
        self.rowconfigure(0, weight=20)  # Row has iteration settings
        self.rowconfigure(1, weight=1)  # Row has step settings
        self.rowconfigure(2, weight=10)  # Row has optimisation criteria
        self.rowconfigure(3, weight=40)  # Row has threshold criteria
        # self.rowconfigure(3, weight=1)
        # self.rowconfigure(4, weight=1)
        # self.rowconfigure(5, weight=1)
        # self.rowconfigure(6, weight=1)
        # self.rowconfigure(7, weight=1)
        # self.rowconfigure(8, weight=1)
        # self.rowconfigure(9, weight=1)
        # self.rowconfigure(10, weight=1)
        # self.rowconfigure(11, weight=1)
        # self.rowconfigure(12, weight=1)

        self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=1)
        # self.columnconfigure(3, weight=1)
        # self.columnconfigure(4, weight=1)

        # Iterations frame
        self.iterations_frame = ttk.Labelframe(
            self, style="info.TLabelframe", text="Iterations"
        )
        self.iterations_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=10,
            ipady=80,
            ipadx=40,
            sticky="news",
        )

        self.iterations_frame.rowconfigure(0, weight=4)
        self.iterations_frame.rowconfigure(1, weight=4)
        self.iterations_frame.rowconfigure(2, weight=1)

        self.iterations_frame.columnconfigure(0, weight=10)  # First row has the header
        self.iterations_frame.columnconfigure(1, weight=10)  # These rows have entries
        self.iterations_frame.columnconfigure(2, weight=1)  # These rows have entries
        self.iterations_frame.columnconfigure(3, weight=1)  # These rows have entries

        # Warning about number of iterations
        self.iteration_length = ttk.IntVar(self, "5")
        self.number_of_iterations = ttk.IntVar(self, "2")

        self.warning_text = ttk.Label(
            self.iterations_frame, text="", bootstyle=SECONDARY
        )
        self.warning_text_displayed = ttk.BooleanVar(
            self, False, "warning_text_displayed"
        )
        self.warning_text.grid(
            row=2, column=0, columnspan=3, padx=10, pady=5, sticky="w"
        )

        def update_optimisation_time_warning() -> None:
            """
            If the simulation time is longer than the system lifetime, warn the user.

            The simulation time, i.e., the total length of time for which optimisations
            will be run, can either equal zero, or can exceed the lifetime of the
            system. In either case, the user needs to be warned.

            """

            # Period exceeds system lifetime
            if (
                optimisation_length := self.iteration_length.get()
                * self.number_of_iterations.get()
            ) > self.system_lifetime.get():
                self.warning_text.configure(
                    text="The length and number of iterations specified amounts to "
                    f"{optimisation_length} years which is greater than the system "
                    f"lifetime of {self.system_lifetime.get()} years.",
                )
                self.warning_text.configure(
                    bootstyle=DANGER,
                )
                self.warning_text_displayed.set(True)
                return

            # Optimisation length is zero years.
            if optimisation_length == 0:
                self.warning_text.configure(
                    text="The length and number of iterations specified amounts to "
                    f"{optimisation_length} years and, hence, no optimisations will be "
                    "carried out.",
                )
                self.warning_text.configure(
                    bootstyle=DANGER,
                )
                self.warning_text_displayed.set(True)
                return

            # Text should be disabled.
            if self.warning_text_displayed.get():
                self.warning_text.configure(
                    text="The length and number of iterations specified amounts to "
                    f"{optimisation_length} years which is less than the system "
                    f"lifetime of {self.system_lifetime.get()} years.",
                    bootstyle=SECONDARY,
                )

        # Iteration length
        self.iteration_length_label = ttk.Label(
            self.iterations_frame, text="Iteration Length"
        )
        self.iteration_length_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        def scalar_iteration_length(_):
            self.iteration_length.set(self.iteration_length.get())
            self.iteration_length_entry.update()
            update_optimisation_time_warning()

        self.iteration_length_slider = ttk.Scale(
            self.iterations_frame,
            from_=0,
            to=30,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_iteration_length,
            bootstyle=INFO,
            variable=self.iteration_length,
            # state=DISABLED
        )
        self.iteration_length_slider.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        def enter_iteration_length(_):
            self.iteration_length.set(self.iteration_length_entry.get())
            self.iteration_length_slider.set(int(self.iteration_length.get()))
            update_optimisation_time_warning()

        self.iteration_length_entry = ttk.Entry(
            self.iterations_frame,
            bootstyle=INFO,
            textvariable=self.iteration_length,
        )
        self.iteration_length_entry.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        self.iteration_length_entry.bind("<Return>", enter_iteration_length)

        self.iteration_length_unit = ttk.Label(self.iterations_frame, text=f"years")
        self.iteration_length_unit.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        # Number of iterations
        self.number_of_iterations_label = ttk.Label(
            self.iterations_frame, text="Number of iterations"
        )
        self.number_of_iterations_label.grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )

        def scalarber_of_iterations(_):
            self.number_of_iterations.set(self.number_of_iterations.get())
            self.number_of_iterations_entry.update()
            update_optimisation_time_warning()

        self.number_of_iterations_slider = ttk.Scale(
            self.iterations_frame,
            from_=0,
            to=5,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalarber_of_iterations,
            bootstyle=INFO,
            variable=self.number_of_iterations,
            # state=DISABLED
        )
        self.number_of_iterations_slider.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew"
        )

        def enterber_of_iterations(_):
            self.number_of_iterations.set(self.number_of_iterations_entry.get())
            self.number_of_iterations_slider.set(int(self.number_of_iterations.get()))
            update_optimisation_time_warning()

        self.number_of_iterations_entry = ttk.Entry(
            self.iterations_frame,
            bootstyle=INFO,
            textvariable=self.number_of_iterations,
        )
        self.number_of_iterations_entry.grid(
            row=1, column=2, padx=10, pady=5, sticky="ew"
        )
        self.number_of_iterations_entry.bind("<Return>", enterber_of_iterations)

        self.number_of_iterations_unit = ttk.Label(
            self.iterations_frame, text=f"iterations"
        )
        self.number_of_iterations_unit.grid(
            row=1, column=3, padx=10, pady=5, sticky="ew"
        )

        # Steps frame
        self.steps_frame = ttk.Labelframe(
            self, style="info.TLabelframe", text="Optimisation configuration parameters"
        )
        self.steps_frame.grid(
            row=1,
            column=0,
            padx=5,
            pady=10,
            ipady=0,
            ipadx=0,
            sticky="news",
        )

        self.steps_frame.rowconfigure(0, weight=1)

        self.steps_frame.columnconfigure(0, weight=1)

        self.scrollable_steps_frame = ScrolledFrame(self.steps_frame)
        self.scrollable_steps_frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            sticky="news",
        )

        # self.scrollable_steps_frame.rowconfigure(0, weight=1)
        # self.scrollable_steps_frame.rowconfigure(1, weight=1)
        # self.scrollable_steps_frame.rowconfigure(2, weight=1)
        # self.scrollable_steps_frame.rowconfigure(3, weight=1)
        # self.scrollable_steps_frame.rowconfigure(4, weight=1)

        self.scrollable_steps_frame.columnconfigure(
            0, weight=2
        )  # First row has the header
        self.scrollable_steps_frame.columnconfigure(
            1, weight=1
        )  # These rows have entries
        self.scrollable_steps_frame.columnconfigure(
            2, weight=2
        )  # These rows have entries
        self.scrollable_steps_frame.columnconfigure(
            3, weight=1
        )  # These rows have entries
        self.scrollable_steps_frame.columnconfigure(
            4, weight=2
        )  # First row has the header
        self.scrollable_steps_frame.columnconfigure(
            5, weight=1
        )  # These rows have entries
        self.scrollable_steps_frame.columnconfigure(
            6, weight=1
        )  # These rows have entries

        # PV step size
        self.pv_label = ttk.Label(
            self.scrollable_steps_frame, text="PV", bootstyle=DARK
        )
        self.pv_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.pv_min_label = ttk.Label(self.scrollable_steps_frame, text="min")
        self.pv_min_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.pv_min = ttk.IntVar(self, 5)
        self.pv_min_entry = ttk.Entry(
            self.scrollable_steps_frame, bootstyle=INFO, textvariable=self.pv_min
        )
        self.pv_min_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.pv_min_unit = ttk.Label(self.scrollable_steps_frame, text="panels")
        self.pv_min_unit.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        self.pv_max_label = ttk.Label(self.scrollable_steps_frame, text="max")
        self.pv_max_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        self.pv_max = ttk.IntVar(self, 20)
        self.pv_max_entry = ttk.Entry(
            self.scrollable_steps_frame, bootstyle=INFO, textvariable=self.pv_max
        )
        self.pv_max_entry.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        self.pv_max_unit = ttk.Label(self.scrollable_steps_frame, text="panels")
        self.pv_max_unit.grid(row=0, column=4, padx=10, pady=5, sticky="w")

        self.pv_step_label = ttk.Label(self.scrollable_steps_frame, text="step")
        self.pv_step_label.grid(row=0, column=4, padx=10, pady=5, sticky="e")
        self.pv_step = ttk.IntVar(self, 5)

        self.pv_step_entry = ttk.Entry(
            self.scrollable_steps_frame, bootstyle=INFO, textvariable=self.pv_step
        )
        self.pv_step_entry.grid(row=0, column=5, padx=10, pady=5, sticky="ew")

        self.pv_step_unit = ttk.Label(self.scrollable_steps_frame, text="panels")
        self.pv_step_unit.grid(row=0, column=6, padx=10, pady=5, sticky="w")

        # Storage step size
        self.storage_label = ttk.Label(self.scrollable_steps_frame, text="Batteries")
        self.storage_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.storage_min_label = ttk.Label(self.scrollable_steps_frame, text="min")
        self.storage_min_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.storage_min = ttk.IntVar(self, 5)
        self.storage_min_entry = ttk.Entry(
            self.scrollable_steps_frame, bootstyle=INFO, textvariable=self.storage_min
        )
        self.storage_min_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.storage_min_unit = ttk.Label(self.scrollable_steps_frame, text="batteries")
        self.storage_min_unit.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        self.storage_max_label = ttk.Label(self.scrollable_steps_frame, text="max")
        self.storage_max_label.grid(row=1, column=2, padx=10, pady=5, sticky="e")

        self.storage_max = ttk.IntVar(self, 30)
        self.storage_max_entry = ttk.Entry(
            self.scrollable_steps_frame, bootstyle=INFO, textvariable=self.storage_max
        )
        self.storage_max_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")

        self.storage_max_unit = ttk.Label(self.scrollable_steps_frame, text="batteries")
        self.storage_max_unit.grid(row=1, column=4, padx=10, pady=5, sticky="w")

        self.storage_step_label = ttk.Label(self.scrollable_steps_frame, text="step")
        self.storage_step_label.grid(row=1, column=4, padx=10, pady=5, sticky="e")
        self.storage_step = ttk.IntVar(self, 5)

        self.storage_step_entry = ttk.Entry(
            self.scrollable_steps_frame, bootstyle=INFO, textvariable=self.storage_step
        )
        self.storage_step_entry.grid(row=1, column=5, padx=10, pady=5, sticky="ew")

        self.storage_step_unit = ttk.Label(
            self.scrollable_steps_frame, text="batteries"
        )
        self.storage_step_unit.grid(row=1, column=6, padx=10, pady=5, sticky="w")

        # PV-T step size
        self.pv_t_label = ttk.Label(self.scrollable_steps_frame, text="PV-T")
        self.pv_t_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.pv_t_min_label = ttk.Label(self.scrollable_steps_frame, text="min")
        self.pv_t_min_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.pv_t_min = ttk.IntVar(self, 5)
        self.pv_t_min_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.pv_t_min,
            state=DISABLED,
        )
        self.pv_t_min_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.pv_t_min_unit = ttk.Label(self.scrollable_steps_frame, text="panels")
        self.pv_t_min_unit.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        self.pv_t_max_label = ttk.Label(self.scrollable_steps_frame, text="max")
        self.pv_t_max_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")

        self.pv_t_max = ttk.IntVar(self, 20)
        self.pv_t_max_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.pv_t_max,
            state=DISABLED,
        )
        self.pv_t_max_entry.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        self.pv_t_max_unit = ttk.Label(self.scrollable_steps_frame, text="panels")
        self.pv_t_max_unit.grid(row=2, column=4, padx=10, pady=5, sticky="w")

        self.pv_t_step_label = ttk.Label(self.scrollable_steps_frame, text="step")
        self.pv_t_step_label.grid(row=2, column=4, padx=10, pady=5, sticky="e")
        self.pv_t_step = ttk.IntVar(self, 5)

        self.pv_t_step_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.pv_t_step,
            state=DISABLED,
        )
        self.pv_t_step_entry.grid(row=2, column=5, padx=10, pady=5, sticky="ew")

        self.pv_t_step_unit = ttk.Label(self.scrollable_steps_frame, text="panels")
        self.pv_t_step_unit.grid(row=2, column=6, padx=10, pady=5, sticky="w")

        # Solar Thermal step size
        self.solar_thermal_label = ttk.Label(
            self.scrollable_steps_frame, text="Solar-thermal"
        )
        self.solar_thermal_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.solar_thermal_min_label = ttk.Label(
            self.scrollable_steps_frame, text="min"
        )
        self.solar_thermal_min_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

        self.solar_thermal_min = ttk.IntVar(self, 5)
        self.solar_thermal_min_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.solar_thermal_min,
            state=DISABLED,
        )
        self.solar_thermal_min_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.solar_thermal_min_unit = ttk.Label(
            self.scrollable_steps_frame, text="panels"
        )
        self.solar_thermal_min_unit.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        self.solar_thermal_max_label = ttk.Label(
            self.scrollable_steps_frame, text="max"
        )
        self.solar_thermal_max_label.grid(row=3, column=2, padx=10, pady=5, sticky="e")

        self.solar_thermal_max = ttk.IntVar(self, 20)
        self.solar_thermal_max_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.solar_thermal_max,
            state=DISABLED,
        )
        self.solar_thermal_max_entry.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        self.solar_thermal_max_unit = ttk.Label(
            self.scrollable_steps_frame, text="panels"
        )
        self.solar_thermal_max_unit.grid(row=3, column=4, padx=10, pady=5, sticky="w")

        self.solar_thermal_step_label = ttk.Label(
            self.scrollable_steps_frame, text="step"
        )
        self.solar_thermal_step_label.grid(row=3, column=4, padx=10, pady=5, sticky="e")
        self.solar_thermal_step = ttk.IntVar(self, 5)

        self.solar_thermal_step_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.solar_thermal_step,
            state=DISABLED,
        )
        self.solar_thermal_step_entry.grid(
            row=3, column=5, padx=10, pady=5, sticky="ew"
        )

        self.solar_thermal_step_unit = ttk.Label(
            self.scrollable_steps_frame, text="panels"
        )
        self.solar_thermal_step_unit.grid(row=3, column=6, padx=10, pady=5, sticky="w")

        # Hot Water Tanks step size
        self.hot_water_tanks_label = ttk.Label(
            self.scrollable_steps_frame, text="Hot-water tanks"
        )
        self.hot_water_tanks_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.hot_water_tanks_min_label = ttk.Label(
            self.scrollable_steps_frame, text="min"
        )
        self.hot_water_tanks_min_label.grid(
            row=4, column=0, padx=10, pady=5, sticky="e"
        )

        self.hot_water_tanks_min = ttk.IntVar(self, 5)
        self.hot_water_tanks_min_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.hot_water_tanks_min,
            state=DISABLED,
        )
        self.hot_water_tanks_min_entry.grid(
            row=4, column=1, padx=10, pady=5, sticky="ew"
        )

        self.hot_water_tanks_min_unit = ttk.Label(
            self.scrollable_steps_frame, text="tanks"
        )
        self.hot_water_tanks_min_unit.grid(row=4, column=2, padx=10, pady=5, sticky="w")

        self.hot_water_tanks_max_label = ttk.Label(
            self.scrollable_steps_frame, text="max"
        )
        self.hot_water_tanks_max_label.grid(
            row=4, column=2, padx=10, pady=5, sticky="e"
        )

        self.hot_water_tanks_max = ttk.IntVar(self, 20)
        self.hot_water_tanks_max_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.hot_water_tanks_max,
        )
        self.hot_water_tanks_max_entry.grid(
            row=4, column=3, padx=10, pady=5, sticky="ew"
        )

        self.hot_water_tanks_max_unit = ttk.Label(
            self.scrollable_steps_frame, text="tanks"
        )
        self.hot_water_tanks_max_unit.grid(row=4, column=4, padx=10, pady=5, sticky="w")

        self.hot_water_tanks_step_label = ttk.Label(
            self.scrollable_steps_frame, text="step"
        )
        self.hot_water_tanks_step_label.grid(
            row=4, column=4, padx=10, pady=5, sticky="e"
        )
        self.hot_water_tanks_step = ttk.IntVar(self, 5)

        self.hot_water_tanks_step_entry = ttk.Entry(
            self.scrollable_steps_frame,
            bootstyle=SECONDARY,
            textvariable=self.solar_thermal_step,
            state=DISABLED,
        )
        self.hot_water_tanks_step_entry.grid(
            row=4, column=5, padx=10, pady=5, sticky="ew"
        )

        self.hot_water_tanks_step_unit = ttk.Label(
            self.scrollable_steps_frame, text="tanks"
        )
        self.hot_water_tanks_step_unit.grid(
            row=4, column=6, padx=10, pady=5, sticky="w"
        )

        # Optimisation criterion frame
        self.optimisation_criterion_frame = ttk.Labelframe(
            self, style="info.TLabelframe", text="Optimisation criterion"
        )
        self.optimisation_criterion_frame.grid(
            row=2,
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
            row=3,
            column=0,
            padx=5,
            pady=10,
            ipady=40,
            ipadx=20,
            sticky="news",
        )

        self.threshold_criteria_frame.columnconfigure(0, weight=1)
        self.threshold_criteria_frame.columnconfigure(1, weight=1)
        self.threshold_criteria_frame.columnconfigure(2, weight=1)
        self.threshold_criteria_frame.columnconfigure(3, weight=1)

        self.threshold_criteria_frame.rowconfigure(0, weight=1)
        self.threshold_criteria_frame.rowconfigure(1, weight=8)

        threshold_criteria: list[ThresholdCriterion] = [
            ThresholdCriterion(
                ttk.StringVar(self, "LCUE ($/kWh)"),
                ttk.BooleanVar(self, True),
                ttk.DoubleVar(self, 3.15),
            ),
            ThresholdCriterion(
                ttk.StringVar(self, "Total cost ($)"),
                ttk.BooleanVar(self, True),
                ttk.DoubleVar(self, 10000),
            ),
        ]

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
            ipady=40,
        )

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

    def __init__(
        self, open_details_window: Callable, system_lifetime: ttk.IntVar
    ) -> None:
        """
        Instantiate a :class:`ConfigureFrame` instance.

        :param: open_details_window
            A callable function to open the details screen.

        :param: system_lifetime
            The lifetime of the system, in years.

        """

        super().__init__()

        self.system_lifetime: ttk.IntVar = system_lifetime

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

        self.optimisation_frame = OptimisationFrame(
            self.configuration_notebook, self.system_lifetime
        )
        self.configuration_notebook.add(self.optimisation_frame, text="Optimise")

        self.advanced_settings_button = ttk.Button(
            self, bootstyle=INFO, text="Advanced settings", command=open_details_window
        )
        self.advanced_settings_button.grid(
            row=2, column=1, sticky="w", pady=20, ipadx=80, ipady=20
        )
