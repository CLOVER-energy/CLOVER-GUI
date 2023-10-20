#!/usr/bin/python3.10
########################################################################################
# configuration.py - The configuration module for CLOVER-GUI application.              #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import datetime
import os
import tkinter as tk

import customtkinter as ctk
import ttkbootstrap as ttk

from typing import Callable

from clover import (
    OperatingMode,
    OPTIMISATION_OUTPUTS_FOLDER,
    OUTPUTS_FOLDER,
    Simulation,
    SIMULATION_OUTPUTS_FOLDER,
)
from clover.__utils__ import (
    get_locations_foldername,
    ITERATION_LENGTH,
    LOCATIONS_FOLDER_NAME,
    MAX,
    MIN,
    NUMBER_OF_ITERATIONS,
    STEP,
)
from clover.fileparser import OPTIMISATIONS
from clover.optimisation import Optimisation, OptimisationParameters, ThresholdMode
from clover.optimisation.__utils__ import (
    Criterion,
    OPTIMISATION_CRITERIA,
    OptimisationComponent,
    THRESHOLD_CRITERIA,
    THRESHOLD_CRITERION_TO_MODE,
)
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.tooltip import ToolTip

from .__utils__ import BaseScreen, clover_thread, IMAGES_DIRECTORY
from .scenario import ConfigurationFrame


__all__ = ("ConfigurationScreen",)


class SimulationFrame(BaseScreen, show_navigation=False):

    """
    Represents the simulation frame.

    The simulation frame contains the necessary parameters needed to launch a simulation
    in CLOVER as well as a launch button for initiating the run.

    TODO: Update attributes.

    """

    def __init__(
        self,
        parent,
        help_image: ttk.PhotoImage,
        launch_clover_run: Callable,
    ) -> None:
        super().__init__(parent)

        """
        Instantiate a :class:`ConfigureFrame` instance.

        :param: help_image
            The :class:`ttk.PhotoImage` to use for help boxes.

        :param: launch_clover_run
            A callable function to launch a simulation.

        """

        self.pack(fill="both", expand=True)

        self.help_image = help_image

        # Set the physical distance weights of the rows and columns
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.start_year = ttk.DoubleVar()
        self.end_year = ttk.DoubleVar()

        # self.end_year_slider = ttk.Scale(self, bootstyle="danger")
        # self.end_year_slider.grid(row=3, column=1, padx=20)
        self.generate_plots = ttk.BooleanVar()

        # Style
        bold_head = ttk.Style()
        bold_head.configure("Bold.TLabel", font=("TkDefaultFont", 12, "bold"))

        self.help_frame = ttk.Frame(self)
        self.help_frame.grid(row=0, column=0, columnspan=4, padx=0, sticky="news")

        self.help_frame.columnconfigure(0, weight=1)
        self.help_frame.columnconfigure(1, weight=1)
        self.help_frame.columnconfigure(2, weight=1)
        self.help_frame.columnconfigure(3, weight=1)
        self.help_frame.columnconfigure(4, weight=1)
        self.help_frame.rowconfigure(0, weight=1)
        self.help_frame.rowconfigure(1, weight=1)

        # Help text
        self.help_text_label = ttk.Label(
            self.help_frame, text="Simulate a system", style="Bold.TLabel"
        )
        self.help_text_label.grid(
            row=0, column=0, columnspan=2, padx=20, pady=10, sticky="w"
        )
        self.simulation_help_icon = ttk.Label(
            self.help_frame,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )

        self.simulation_help_tooltip = ToolTip(
            self.simulation_help_icon,
            text="You can run a simulation of an energy system within CLOVER by "
            "specifying the capacity of the energy-generation components and the "
            "lifetime of your system. Specify whether to generate plots within CLOVER"
            " as well as the output folder name.",
            bootstyle=f"{INFO}-{INVERSE}",
        )
        self.simulation_help_icon.grid(row=0, column=0, padx=20, pady=10, sticky="e")

        self.separator = ttk.Separator(self.help_frame)
        self.separator.grid(row=1, column=0, columnspan=6, sticky="sew", padx=(20, 20))

        self.capacity_header = ttk.Label(
            self, text="Component sizes", style="Bold.TLabel"
        )
        self.capacity_header.grid(
            row=1, column=0, columnspan=5, padx=20, pady=10, sticky="w"
        )

        # PV size
        self.pv_size_label = ttk.Label(self, text="PV System Size")
        self.pv_size_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.pv_size: ttk.DoubleVar = ttk.DoubleVar(self, value=0)
        self.pv_size_entry = ttk.Entry(self, bootstyle=INFO, textvariable=self.pv_size)
        self.pv_size_entry.grid(
            row=2, column=1, columnspan=2, padx=20, pady=10, sticky="ew", ipadx=20
        )

        self.pv_size_info = ttk.Label(self, text="kWp")
        self.pv_size_info.grid(row=2, column=3, sticky="w")

        # Storage size
        self.storage_size_label = ttk.Label(self, text="Storage Size")
        self.storage_size_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.storage_size: ttk.DoubleVar = ttk.DoubleVar(self, value=0)
        self.storage_size_entry = ttk.Entry(
            self, bootstyle=INFO, textvariable=self.storage_size
        )
        self.storage_size_entry.grid(
            row=3, column=1, columnspan=2, padx=20, pady=10, sticky="ew", ipadx=20
        )
        self.storage_size_info = ttk.Label(self, text="kWh")
        self.storage_size_info.grid(row=3, column=3, sticky="w")

        # Simulation period
        self.simulation_period_label = ttk.Label(self, text="Simulation period")
        self.simulation_period_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.simulation_period = ttk.IntVar(self, 20, "simulation_period")

        # self.simulation_period_info = ttk.Label(self, text="Years")
        # self.simulation_period_info.grid(row=3, column=3)

        self.scalerber = ttk.Label(
            self, text=f"{int(self.simulation_period.get())} years"
        )
        self.scalerber.grid(row=4, column=3, sticky="w")

        def scaler(e):
            self.scalerber.config(
                text=f"{' ' * (int(self.years_slider.get()) < 10)}{int(self.years_slider.get())} years"
            )

        self.years_slider = ttk.Scale(
            self,
            from_=1,
            to=30,
            orient=tk.HORIZONTAL,
            length=320,
            command=scaler,
            bootstyle=INFO,
            variable=self.simulation_period,
        )
        self.years_slider.grid(
            row=4, column=1, columnspan=2, padx=20, pady=10, sticky="ew"
        )

        # Horizontal divider
        self.horizontal_divider = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.horizontal_divider.grid(
            row=5, column=0, columnspan=5, padx=20, pady=10, sticky="ew"
        )

        self.outputs_header = ttk.Label(self, text="Outputs", style="Bold.TLabel")
        self.outputs_header.grid(
            row=6, column=0, columnspan=5, padx=20, pady=10, sticky="w"
        )

        # Generate plots
        self.generate_plots_label = ttk.Label(self, text="Generate plots")
        self.generate_plots_label.grid(row=7, column=0, padx=20, pady=10, sticky="w")

        self.generate_plots: ttk.BooleanVar = ttk.BooleanVar(
            self, True, "generate_plots"
        )
        self.not_generate_plots: ttk.BooleanVar = ttk.BooleanVar(
            self, not self.generate_plots.get(), "not_generate_plots"
        )

        self.generate_plots_true_button = ttk.Checkbutton(
            self,
            variable=self.generate_plots,
            command=self._generate_plots_callback,
            bootstyle=f"{INFO}-{TOOLBUTTON}",
            text="ON",
        )
        self.generate_plots_true_button.grid(
            row=7, column=1, padx=20, pady=10, sticky="ew"
        )

        self.generate_plots_false_button = ttk.Checkbutton(
            self,
            variable=self.not_generate_plots,
            command=self._not_generate_plots_callback,
            bootstyle=f"{INFO}-{TOOLBUTTON}",
            text="OFF",
        )
        self.generate_plots_false_button.grid(
            row=7, column=2, padx=20, pady=10, sticky="ew"
        )

        # Output name
        self.output_name_label = ttk.Label(self, text="Output name")
        self.output_name_label.grid(row=8, column=0, padx=20, pady=10, sticky="w")

        self.output_name: ttk.StringVar = ttk.StringVar(self, "results")
        self.output_name_entry = ttk.Entry(
            self, bootstyle=INFO, textvariable=self.output_name
        )
        self.output_name_entry.grid(
            row=8, column=1, columnspan=2, padx=20, pady=10, sticky="ew", ipadx=80
        )

        # Combines the functions to open the run screen and launch the simulation.
        self.run_simulation_frame = ttk.Frame(self)
        self.run_simulation_frame.grid(row=9, column=0, columnspan=4)

        self.run_simulation_frame.columnconfigure(0, weight=4, minsize=800)
        self.run_simulation_frame.columnconfigure(1, weight=1)
        self.run_simulation_frame.rowconfigure(0, weight=1)

        self.run_simulation_button = ttk.Button(
            self.run_simulation_frame,
            text="Run Simulation",
            bootstyle=f"{INFO}-outline",
            command=lambda operating_mode=OperatingMode.SIMULATION: launch_clover_run(
                operating_mode
            ),
        )
        self.run_simulation_button.grid(
            row=0,
            column=1,
            columnspan=2,
            padx=5,
            pady=10,
            ipadx=80,
            ipady=20,
            sticky="es",
        )

        # TODO: Add configuration frame widgets and layout

    def _generate_plots_callback(self) -> None:
        """Called when the not-generate-plots button is pressed."""

        self.generate_plots.set(True)
        self.not_generate_plots.set(False)

    def _not_generate_plots_callback(self) -> None:
        """Called when the not-generate-plots button is pressed."""

        self.generate_plots.set(False)
        self.not_generate_plots.set(True)

    def set_simulation(self, simulation: Simulation) -> None:
        """
        Set the information from the simulation loaded.

        :param: simulation
            The simulation to set.

        """

        # Update the simulation period from the simulations file.
        self.start_year.set(simulation.start_year)
        self.end_year.set(simulation.end_year)
        self.simulation_period.set(self.end_year.get() - self.start_year.get())

        self.years_slider.set(self.simulation_period.get())


# Criterion-to-name map
#   A map between the criteria and their nicely-displayed names.
CRITERION_TO_NAME_MAP: dict[Criterion, str] = {
    Criterion.BLACKOUTS: "Blackouts fraction",
    Criterion.CLEAN_WATER_BLACKOUTS: "Clean water blackouts fraction",
    Criterion.CUMULATIVE_COST: "Cumulative cost / $",
    Criterion.CUMULATIVE_GHGS: "Cumulative ghgs / kgCO2eq",
    Criterion.CUMULATIVE_SYSTEM_COST: "Cumulative system cost / $",
    Criterion.CUMULATIVE_SYSTEM_GHGS: "Cumulative system ghgs / kgCO2eq",
    Criterion.EMISSIONS_INTENSITY: "Emissions intensity / gCO2/kWh",
    Criterion.KEROSENE_COST_MITIGATED: "Kerosene cost mitigated / $",
    Criterion.KEROSENE_GHGS_MITIGATED: "Kerosene ghgs mitigated / kgCO2eq",
    Criterion.LCUE: "LCUE / $/kWh",
    Criterion.RENEWABLES_FRACTION: "Renewables fraction",
    Criterion.TOTAL_GHGS: "Total ghgs / kgCO2eq",
    Criterion.TOTAL_SYSTEM_COST: "Total system cost / $",
    Criterion.TOTAL_SYSTEM_GHGS: "Total system ghgs / kgCO2eq",
    Criterion.TOTAL_COST: "Total cost / $",
    Criterion.UNMET_ENERGY_FRACTION: "Unmet energy fraction",
    Criterion.UPTIME: "Uptime",
}

# Criterion-to-units map
#   A map between the criteria and their corresponding untis.
CRITERION_TO_UNITS_MAP: dict[Criterion, str] = {
    Criterion.BLACKOUTS: "\% of hours",
    Criterion.CLEAN_WATER_BLACKOUTS: "\% of hours",
    Criterion.CUMULATIVE_COST: "currency unit",
    Criterion.CUMULATIVE_GHGS: "kgCO2eq",
    Criterion.CUMULATIVE_SYSTEM_COST: "currency unit",
    Criterion.CUMULATIVE_SYSTEM_GHGS: "kgCO2eq",
    Criterion.EMISSIONS_INTENSITY: "gCO2/kWh",
    Criterion.KEROSENE_COST_MITIGATED: "currency unit",
    Criterion.KEROSENE_GHGS_MITIGATED: "kgCO2eq",
    Criterion.LCUE: "currency/kWh",
    Criterion.RENEWABLES_FRACTION: "\% of energy used",
    Criterion.TOTAL_GHGS: "kgCO2eq",
    Criterion.TOTAL_SYSTEM_COST: "currenty unit",
    Criterion.TOTAL_SYSTEM_GHGS: "kgCO2eq",
    Criterion.TOTAL_COST: "currency unit",
    Criterion.UNMET_ENERGY_FRACTION: "\% of energy used",
    Criterion.UPTIME: "\% of hours",
}

# Percentage criteria
#   Criteria which should have their value adjusted when displayed only so that
#   users can deal with the numbers in terms of percentages rather than decimal
#   fractions.
PERCENTAGE_CRITERIA: list[Criterion] = [
    Criterion.BLACKOUTS,
    Criterion.CLEAN_WATER_BLACKOUTS,
    Criterion.RENEWABLES_FRACTION,
    Criterion.UNMET_ENERGY_FRACTION,
    Criterion.UPTIME,
]


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

    .. attribute:: index
        The index of the criteria as being created.

    """

    # Private attributes:
    #
    # .. attribute:: _name_to_criterion_map
    #   Map between the name of the criteria and the criteria.
    #
    # .. attribute:: _permissable_threshold_criteria
    #   The `list` of permissable threshold criteria.

    _name_to_criterion_map: dict[str, Criterion] | None = None

    # _permissable_chevrons: list[str] = sorted(["<", ">"])

    _permissable_threshold_criteria: list[str] = sorted(CRITERION_TO_NAME_MAP.values())

    def __init__(
        self,
        parent,
        criterion_name: ttk.StringVar,
        less_than: ttk.BooleanVar,
        value: ttk.DoubleVar,
        delete_criterion: Callable,
        index: int = 0,
    ) -> None:
        """
        Instnatiate a :class:`ThresholdCriterion` instance.

        :param: parent
            The parent :class:`ttk.Frame` in which the class is being created.

        :param: criterion_name
            The name of the criterion.

        :param: less_than
            Whether to use a less-than (True) or greater-than (False) condition for the
            criterion.

        :param: value
            The threshold value for the criterion.

        :param: delete_criterion
            `Callable` to delete the criterion.

        :param: index
            The index of the criteria as being created.

        """

        # Criterion name and entry
        self.criterion_name: ttk.StringVar = criterion_name
        self.criterion_name_combobox = ttk.Combobox(
            parent,
            bootstyle=INFO,
            textvariable=self.criterion_name,
            state=READONLY,
        )
        self.criterion_name_combobox["values"] = self._permissable_threshold_criteria
        self.criterion_name_combobox.bind("<<ComboboxSelected>>", self.select_criterion)

        self.less_than: ttk.BooleanVar = less_than
        self.less_than_string: ttk.StringVar = ttk.StringVar(
            parent, "less than" if self.less_than.get() else "greater than"
        )
        self.less_than_label = ttk.Label(
            parent, bootstyle=INFO, text=self.less_than_string.get()
        )

        self.value: ttk.DoubleVar = value
        self.percentage_value: ttk.DoubleVar = ttk.DoubleVar(parent, 100 * value.get())
        self.value_entry = ttk.Entry(
            parent,
            bootstyle=INFO,
            textvariable=self.value
            if self.name_to_criterion_map[criterion_name.get()]
            not in PERCENTAGE_CRITERIA
            else self.percentage_value,
        )
        self.value_entry.bind("<<Return>>", self._enter_value)

        self.units_string: ttk.StringVar = ttk.StringVar(
            parent,
            CRITERION_TO_UNITS_MAP[self.name_to_criterion_map[criterion_name.get()]],
        )
        self.units_label: ttk.Label = ttk.Label(parent, text=self.units_string.get())

        self.delete_criterion_button: ttk.Button = ttk.Button(
            parent,
            bootstyle=f"{DANGER}-{OUTLINE}",
            text="Delete",
            command=lambda criterion=self: delete_criterion(criterion),
        )

        self.index: int = index

    def __hash__(self) -> int:
        """Return a `str` based on the information in the threshold criteria."""

        return self.index

    def __str__(self) -> str:
        """Return a nice-looking string."""

        return (
            f"ThresholdCriterion('{self.criterion_name.get()}' "
            + ("less than" if self.less_than.get() else "greater than")
            + f" {self.value.get()}"
        )

    def __repr__(self) -> str:
        """Return the default representation of the class."""

        return self.__str__()

    def _enter_value(self, _=None) -> None:
        """Callback for when a value is entered."""

        if (
            self.name_to_criterion_map[self.criterion_name_combobox.get()]
            in PERCENTAGE_CRITERIA
        ):
            self.value.set(self.percentage_value.get())
        else:
            self.percentage_value.set(self.value.get())

    @classmethod
    def default_threshold_criterion(cls) -> str:
        """Return the default threshold criterion."""

        return cls._permissable_threshold_criteria[0]

    def display(self) -> None:
        """Display the criterion on the screen."""

        self.criterion_name_combobox.grid(
            row=(25 + self.index), column=0, columnspan=2, padx=20, pady=10, sticky="ew"
        )
        self.less_than_label.grid(
            row=(25 + self.index), column=2, padx=20, pady=10, sticky="ew"
        )
        self.value_entry.grid(
            row=(25 + self.index), column=3, padx=20, pady=10, sticky="ew"
        )
        self.units_label.grid(
            row=(25 + self.index), column=4, padx=20, pady=10, sticky="w"
        )
        self.delete_criterion_button.grid(
            row=(25 + self.index), column=5, padx=20, pady=10, sticky="w", ipadx=20
        )

    def grid_forget(self) -> None:
        """Remove the varoius items from the screen."""

        self.criterion_name_combobox.grid_forget()
        self.less_than_label.grid_forget()
        self.value_entry.grid_forget()
        self.units_label.grid_forget()
        self.delete_criterion_button.grid_forget()

    @classmethod
    @property
    def name_to_criterion_map(self) -> dict[str, Criterion]:
        """
        Return a mapping bewteen criteria and names to be stored.

        :return:
            A mapping between criteria and names to store them in-file.

        """

        if self._name_to_criterion_map is None:
            self._name_to_criterion_map: dict[str, Criterion] = {
                value: key for key, value in CRITERION_TO_NAME_MAP.items()
            }
        return self._name_to_criterion_map

    def select_criterion(self, _) -> None:
        """Called when the combobox is selected."""

        # Update the less-than variables based on the new variable.
        self.less_than.set(
            THRESHOLD_CRITERION_TO_MODE[
                (
                    criterion := self.name_to_criterion_map[
                        self.criterion_name_combobox.get()
                    ]
                )
            ]
            == ThresholdMode.MAXIMUM
        )
        self.less_than_string.set(
            "less than" if self.less_than.get() else "greater than"
        )
        self.less_than_label.configure(text=self.less_than_string.get())

        # Update the value entry based on whether the criterion should have a percentage
        # displayed or not.
        if criterion in PERCENTAGE_CRITERIA:
            self.value_entry.configure(textvariable=self.percentage_value)
        else:
            self.value_entry.configure(textvariable=self.value)

        # Update the units based on the new variable.
        self.units_string.set(CRITERION_TO_UNITS_MAP[criterion])
        self.units_label.configure(text=self.units_string.get())

    def set_index(self, index: int) -> None:
        """
        Sets the index attribute.

        :param: index
            The index to set.

        """

        self.index = index


class OptimisationFrame(ttk.Frame):
    """
    Represents the optimisation frame.

    The optimisation frame contains the launch parameters needed for launching an
    optimisation in CLOVER as well as a launch button for initiating the run.

    TODO: Update attributes.

    """

    def __init__(
        self,
        parent,
        help_image: ttk.PhotoImage,
        launch_clover_run: Callable,
        system_lifetime: ttk.IntVar,
    ):
        super().__init__(parent)

        self.help_image = help_image
        self.system_lifetime = system_lifetime

        # TODO: Add configuration frame widgets and layout
        self.pack(fill="both", expand=True)

        self.rowconfigure(0, weight=1)  # info frame
        self.rowconfigure(1, weight=1)  # separator
        self.rowconfigure(2, weight=20)  # scrolled frame
        self.rowconfigure(3, weight=1)  # separator
        self.rowconfigure(4, weight=1)  # run optimisation button

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        # Create the scrollable frame and rows
        self.scrollable_optimisation_frame = ScrolledFrame(
            self,
        )
        self.scrollable_optimisation_frame.grid(
            row=2,
            column=0,
            columnspan=5,
            padx=20,
            pady=10,
            ipady=0,
            ipadx=0,
            sticky="news",
        )
        self.scrollable_optimisation_frame.config(width=30)

        # rows
        self.scrollable_optimisation_frame.rowconfigure(0, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(1, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(2, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(3, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(4, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(5, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(6, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(7, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(8, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(9, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(10, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(11, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(12, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(13, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(14, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(15, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(16, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(17, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(18, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(19, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(20, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(21, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(22, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(23, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(24, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(25, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(26, weight=1)
        self.scrollable_optimisation_frame.rowconfigure(27, weight=1)

        # columns
        self.scrollable_optimisation_frame.columnconfigure(0, weight=1)
        self.scrollable_optimisation_frame.columnconfigure(
            1, weight=1, minsize=40, pad=20
        )
        self.scrollable_optimisation_frame.columnconfigure(2, weight=4, minsize=40)
        self.scrollable_optimisation_frame.columnconfigure(3, weight=4, minsize=80)
        self.scrollable_optimisation_frame.columnconfigure(4, weight=4, minsize=80)
        self.scrollable_optimisation_frame.columnconfigure(5, weight=4, minsize=80)
        # self.scrollable_optimisation_frame.columnconfigure(5, weight=1)
        # self.scrollable_optimisation_frame.columnconfigure(6, weight=1)

        # Iterations frame
        # self.iterations_frame = ttk.Labelframe(
        #     self, style="info.TLabelframe", text="Iterations"
        # )
        # self.iterations_frame.grid(
        #     row=0,
        #     column=0,
        #     columnspan=2,
        #     padx=5,
        #     pady=10,
        #     ipady=80,
        #     ipadx=40,
        #     sticky="news",
        # )

        # self.iterations_frame.rowconfigure(0, weight=4)
        # self.iterations_frame.rowconfigure(1, weight=4)
        # self.iterations_frame.rowconfigure(2, weight=1)

        # self.iterations_frame.columnconfigure(0, weight=10)  # First row has the header
        # self.iterations_frame.columnconfigure(1, weight=10)  # These rows have entries
        # self.iterations_frame.columnconfigure(2, weight=1)  # These rows have entries
        # self.iterations_frame.columnconfigure(3, weight=1)  # These rows have entries

        bold_head = ttk.Style()
        bold_head.configure("Bold.TLabel", font=("TkDefaultFont", 13, "bold"))

        # Help text
        self.help_text_label = ttk.Label(
            self, text="Optimise a system", style="Bold.TLabel"
        )
        self.help_text_label.grid(
            row=0, column=0, columnspan=2, padx=(40, 20), pady=20, sticky="w"
        )

        self.optimisation_help_icon = ttk.Label(
            self,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )
        self.optimisation_help_tooltip = ToolTip(
            self.optimisation_help_icon,
            text="You can run an optimisation of the capacity of various components "
            "within an energy system. Specify the length\nof time for which your "
            "system will run, along with target and threhold criteria.",
            bootstyle=f"{INFO}-{INVERSE}",
        )
        self.optimisation_help_icon.grid(
            row=0, column=2, padx=(20, 20), pady=20, sticky="w"
        )

        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=0, columnspan=6, sticky="ew", padx=(40, 40))

        # Warning about number of iterations
        self.iteration_length = ttk.IntVar(self, "5")
        self.number_of_iterations = ttk.IntVar(self, "2")

        self.warning_text = ttk.Label(
            self.scrollable_optimisation_frame, text="", bootstyle=SECONDARY
        )
        self.warning_text_displayed = ttk.BooleanVar(
            self, False, "warning_text_displayed"
        )
        self.warning_text.grid(
            row=3, column=0, columnspan=5, padx=20, pady=10, sticky="ew"
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
                    f"{optimisation_length} years which is "
                    + (
                        "less than "
                        if optimisation_length < self.system_lifetime.get()
                        else "equal to "
                    )
                    + f"the system lifetime of {self.system_lifetime.get()} years.",
                    bootstyle=SECONDARY,
                )

        # Iteration header
        self.iteration_header = ttk.Label(
            self.scrollable_optimisation_frame, text="Iterations", style="Bold.TLabel"
        )
        self.iteration_header.grid(
            row=0, column=0, columnspan=4, padx=20, pady=10, sticky="w"
        )

        # Iteration length
        self.iteration_length_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Iteration Length"
        )
        self.iteration_length_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.iteration_length_help = ttk.Label(
            self.scrollable_optimisation_frame,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )
        self.iteration_length_help.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.iteration_length_help_tooltip = ToolTip(
            self.iteration_length_help,
            bootstyle=f"{INFO}-{INVERSE}",
            text="An optimisation consists of several periods, at the begining of "
            "which the capacity of the system can be upgraded. The length of each one "
            "of these periods is defined here, in years, as the iteration length.",
        )

        def scalar_iteration_length(_):
            self.iteration_length.set(self.iteration_length.get())
            self.iteration_length_entry.update()
            update_optimisation_time_warning()

        self.iteration_length_slider = ttk.Scale(
            self.scrollable_optimisation_frame,
            from_=1,
            to=30,
            orient=tk.HORIZONTAL,
            # length=320,
            command=scalar_iteration_length,
            bootstyle=INFO,
            variable=self.iteration_length,
            # state=DISABLED
        )
        self.iteration_length_slider.grid(
            row=1, column=2, padx=20, pady=10, sticky="ew"
        )
        self.iteration_length_tooltip = ToolTip(
            self.iteration_length_label,
            text="The iteration length is the length of time for which a system will "
            "run without any component upgrades. After this time, the system will "
            "consider whether an increase in capacity is needed in order to meet demand.",
        )

        def enter_iteration_length(_):
            self.iteration_length.set(self.iteration_length_entry.get())
            self.iteration_length_slider.set(int(self.iteration_length.get()))
            update_optimisation_time_warning()

        self.iteration_length_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=INFO,
            textvariable=self.iteration_length,
        )
        self.iteration_length_entry.grid(row=1, column=3, padx=20, pady=10, sticky="ew")
        self.iteration_length_entry.bind("<Return>", enter_iteration_length)

        self.iteration_length_unit = ttk.Label(
            self.scrollable_optimisation_frame, text=f"years"
        )
        self.iteration_length_unit.grid(row=1, column=4, padx=20, pady=10, sticky="ew")

        # Number of iterations
        self.number_of_iterations_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Number of iterations"
        )
        self.number_of_iterations_label.grid(
            row=2, column=0, padx=20, pady=10, sticky="w"
        )
        self.number_of_iterations_tooltip = ToolTip(
            self.number_of_iterations_label,
            text="Each iteration is a period where no upgrades occur. The number of "
            "iterations corresponds to the number of times new capacity will be installed in the system.",
        )

        self.number_of_iterations_help = ttk.Label(
            self.scrollable_optimisation_frame,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )
        self.number_of_iterations_help.grid(
            row=2, column=1, padx=10, pady=10, sticky="w"
        )
        self.number_of_iterations_help_tooltip = ToolTip(
            self.number_of_iterations_help,
            bootstyle=f"{INFO}-{INVERSE}",
            text="An optimisation consists of several periods, at the begining of "
            "which the capacity of the system can be upgraded. The number of these "
            "periods that are considered for a system is defined here, referred to as "
            "the number of iterations.",
        )

        def scalarber_of_iterations(_):
            self.number_of_iterations.set(self.number_of_iterations.get())
            self.number_of_iterations_entry.update()
            update_optimisation_time_warning()

        self.number_of_iterations_slider = ttk.Scale(
            self.scrollable_optimisation_frame,
            from_=1,
            to=self.system_lifetime.get(),
            orient=tk.HORIZONTAL,
            # length=320,
            command=scalarber_of_iterations,
            bootstyle=INFO,
            variable=self.number_of_iterations,
            # state=DISABLED
        )
        self.number_of_iterations_slider.grid(
            row=2, column=2, padx=20, pady=10, sticky="ew"
        )

        def enterber_of_iterations(_):
            self.number_of_iterations.set(self.number_of_iterations_entry.get())
            self.number_of_iterations_slider.set(int(self.number_of_iterations.get()))
            update_optimisation_time_warning()

        self.number_of_iterations_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=INFO,
            textvariable=self.number_of_iterations,
        )
        self.number_of_iterations_entry.grid(
            row=2, column=3, padx=20, pady=10, sticky="ew"
        )
        self.number_of_iterations_entry.bind("<Return>", enterber_of_iterations)

        self.number_of_iterations_unit = ttk.Label(
            self.scrollable_optimisation_frame, text=f"iterations"
        )
        self.number_of_iterations_unit.grid(
            row=2, column=4, padx=20, pady=10, sticky="ew"
        )

        # Horizontal divider
        self.horizontal_divider = ttk.Separator(
            self.scrollable_optimisation_frame, orient=tk.HORIZONTAL
        )
        self.horizontal_divider.grid(
            row=4, column=0, columnspan=6, padx=20, pady=10, sticky="ew"
        )

        # Steps frame
        # self.steps_frame = ttk.Labelframe(
        #     self, style="info.TLabelframe", text="Optimisation configuration parameters"
        # )
        # self.steps_frame.grid(
        #     row=1,
        #     column=0,
        #     columnspan=2,
        #     padx=5,
        #     pady=10,
        #     ipady=0,
        #     ipadx=0,
        #     sticky="news",
        # )

        # self.steps_frame.rowconfigure(0, weight=1)

        # self.steps_frame.columnconfigure(0, weight=1)

        # self.scrollable_steps_frame = ScrolledFrame(self.steps_frame)
        # self.scrollable_steps_frame.grid(
        #     row=0,
        #     column=0,
        #     padx=20,
        #     pady=10,
        #     ipady=0,
        #     ipadx=0,
        #     sticky="news",
        # )

        # self.scrollable_steps_frame.rowconfigure(0, weight=1)
        # self.scrollable_steps_frame.rowconfigure(1, weight=1)
        # self.scrollable_steps_frame.rowconfigure(2, weight=1)
        # self.scrollable_steps_frame.rowconfigure(3, weight=1)
        # self.scrollable_steps_frame.rowconfigure(4, weight=1)

        # self.scrollable_steps_frame.columnconfigure(
        #     0, weight=2
        # )  # First row has the header
        # self.scrollable_steps_frame.columnconfigure(
        #     1, weight=1
        # )  # These rows have entries
        # self.scrollable_steps_frame.columnconfigure(
        #     2, weight=2
        # )  # These rows have entries
        # self.scrollable_steps_frame.columnconfigure(
        #     3, weight=1
        # )  # These rows have entries
        # self.scrollable_steps_frame.columnconfigure(
        #     4, weight=2
        # )  # First row has the header
        # self.scrollable_steps_frame.columnconfigure(
        #     5, weight=1
        # )  # These rows have entries
        # self.scrollable_steps_frame.columnconfigure(
        #     6, weight=1
        # )  # These rows have entries

        # Optimisation parameters header
        self.optimisation_parameters_header = ttk.Label(
            self.scrollable_optimisation_frame,
            text="Optimisation parameters",
            style="Bold.TLabel",
        )
        self.optimisation_parameters_header.grid(
            row=5, column=0, columnspan=6, padx=20, pady=10, sticky="w"
        )

        self.optimisation_parameters_frame = ttk.Frame(
            self.scrollable_optimisation_frame,
        )

        self.optimisation_parameters_frame.grid(
            row=6,
            column=0,
            rowspan=3,
            columnspan=6,
            padx=0,
            pady=0,
            sticky="news",
        )

        self.optimisation_parameters_frame.rowconfigure(0, weight=1)
        self.optimisation_parameters_frame.rowconfigure(1, weight=1)
        self.optimisation_parameters_frame.rowconfigure(2, weight=1)

        self.optimisation_parameters_frame.columnconfigure(0, weight=1)
        self.optimisation_parameters_frame.columnconfigure(1, weight=1)
        self.optimisation_parameters_frame.columnconfigure(2, weight=1)
        self.optimisation_parameters_frame.columnconfigure(3, weight=1)
        self.optimisation_parameters_frame.columnconfigure(4, weight=1)
        self.optimisation_parameters_frame.columnconfigure(5, weight=1)

        # PV step size
        self.pv_label = ttk.Label(self.optimisation_parameters_frame, text="PV min")
        self.pv_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.pv_min = ttk.IntVar(self, 5)
        self.pv_min_entry = ttk.Entry(
            self.optimisation_parameters_frame, bootstyle=INFO, textvariable=self.pv_min
        )
        self.pv_min_entry.grid(row=0, column=1, padx=20, pady=10, sticky="ew")

        self.pv_min_unit = ttk.Label(self.optimisation_parameters_frame, text="kWp")
        self.pv_min_unit.grid(row=0, column=2, padx=20, pady=10, sticky="w")

        self.pv_max_label = ttk.Label(self.optimisation_parameters_frame, text="PV max")
        self.pv_max_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.pv_max = ttk.IntVar(self, 20)
        self.pv_max_entry = ttk.Entry(
            self.optimisation_parameters_frame, bootstyle=INFO, textvariable=self.pv_max
        )
        self.pv_max_entry.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self.pv_max_unit = ttk.Label(self.optimisation_parameters_frame, text="kWp")
        self.pv_max_unit.grid(row=1, column=2, padx=20, pady=10, sticky="w")

        self.pv_step_label = ttk.Label(
            self.optimisation_parameters_frame, text="PV step size"
        )
        self.pv_step_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.pv_step = ttk.IntVar(self, 5)

        self.pv_step_entry = ttk.Entry(
            self.optimisation_parameters_frame,
            bootstyle=INFO,
            textvariable=self.pv_step,
        )
        self.pv_step_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self.pv_step_unit = ttk.Label(self.optimisation_parameters_frame, text="kWp")
        self.pv_step_unit.grid(row=2, column=2, padx=20, pady=10, sticky="w")

        # Storage step size
        self.storage_label = ttk.Label(
            self.optimisation_parameters_frame, text="Storage min"
        )
        self.storage_label.grid(row=0, column=3, padx=20, pady=10, sticky="w")

        # self.storage_min_label = ttk.Label(self.optimisation_parameters_frame, text="min")
        # self.storage_min_label.grid(row=7, column=0, padx=20, pady=10, sticky="e")

        self.storage_min = ttk.IntVar(self, 5)
        self.storage_min_entry = ttk.Entry(
            self.optimisation_parameters_frame,
            bootstyle=INFO,
            textvariable=self.storage_min,
        )
        self.storage_min_entry.grid(row=0, column=4, padx=20, pady=10, sticky="ew")

        self.storage_min_unit = ttk.Label(
            self.optimisation_parameters_frame, text="kWh"
        )
        self.storage_min_unit.grid(row=0, column=5, padx=20, pady=10, sticky="w")

        self.storage_max_label = ttk.Label(
            self.optimisation_parameters_frame, text="Storage max"
        )
        self.storage_max_label.grid(row=1, column=3, padx=20, pady=10, sticky="w")

        self.storage_max = ttk.IntVar(self, 30)
        self.storage_max_entry = ttk.Entry(
            self.optimisation_parameters_frame,
            bootstyle=INFO,
            textvariable=self.storage_max,
        )
        self.storage_max_entry.grid(row=1, column=4, padx=20, pady=10, sticky="ew")

        self.storage_max_unit = ttk.Label(
            self.optimisation_parameters_frame, text="kWh"
        )
        self.storage_max_unit.grid(row=1, column=5, padx=20, pady=10, sticky="w")

        self.storage_step_label = ttk.Label(
            self.optimisation_parameters_frame, text="Storage step size"
        )
        self.storage_step_label.grid(row=2, column=3, padx=20, pady=10, sticky="w")
        self.storage_step = ttk.IntVar(self, 5)

        self.storage_step_entry = ttk.Entry(
            self.optimisation_parameters_frame,
            bootstyle=INFO,
            textvariable=self.storage_step,
        )
        self.storage_step_entry.grid(row=2, column=4, padx=20, pady=10, sticky="ew")

        self.storage_step_unit = ttk.Label(
            self.optimisation_parameters_frame, text="kWh"
        )
        self.storage_step_unit.grid(row=2, column=5, padx=20, pady=10, sticky="w")

        # Hot-water PV-T step size
        self.hw_pv_t_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Hot-water PV-T min"
        )
        # self.hw_pv_t_label.grid(row=10, column=0, padx=20, pady=10, sticky="w")

        self.hw_pv_t_min_label = ttk.Label(
            self.scrollable_optimisation_frame, text="min"
        )
        # self.hw_pv_t_min_label.grid(row=2, column=0, padx=20, pady=10, sticky="e")

        self.hw_pv_t_min = ttk.IntVar(self, 0)
        self.hw_pv_t_min_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.hw_pv_t_min,
            state=DISABLED,
        )
        # self.hw_pv_t_min_entry.grid(row=10, column=1, padx=20, pady=10, sticky="ew")

        self.hw_pv_t_min_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.hw_pv_t_min_unit.grid(row=10, column=2, padx=20, pady=10, sticky="w")

        self.hw_pv_t_max_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Hot-water PV-T max"
        )
        # self.hw_pv_t_max_label.grid(row=10, column=2, padx=20, pady=10, sticky="e")

        self.hw_pv_t_max = ttk.IntVar(self, 0)
        self.hw_pv_t_max_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.hw_pv_t_max,
            state=DISABLED,
        )
        # self.hw_pv_t_max_entry.grid(row=10, column=3, padx=20, pady=10, sticky="ew")

        self.hw_pv_t_max_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.hw_pv_t_max_unit.grid(row=10, column=5, padx=20, pady=10, sticky="w")

        self.hw_pv_t_step_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Hot-water PV-T step size"
        )
        # self.hw_pv_t_step_label.grid(row=11, column=0, padx=20, pady=10, sticky="w")
        self.hw_pv_t_step = ttk.IntVar(self, 0)

        self.hw_pv_t_step_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.hw_pv_t_step,
            state=DISABLED,
        )
        # self.hw_pv_t_step_entry.grid(row=11, column=1, padx=20, pady=10, sticky="ew")

        self.hw_pv_t_step_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.hw_pv_t_step_unit.grid(row=11, column=2, padx=20, pady=10, sticky="w")

        # Clean-water PV-T step size
        self.cw_pv_t_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Clean-water PV-T min"
        )
        # self.cw_pv_t_label.grid(row=12, column=0, padx=20, pady=10, sticky="w")

        self.cw_pv_t_min = ttk.IntVar(self, 0)
        self.cw_pv_t_min_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.cw_pv_t_min,
            state=DISABLED,
        )
        # self.cw_pv_t_min_entry.grid(row=12, column=1, padx=20, pady=10, sticky="ew")

        self.cw_pv_t_min_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.cw_pv_t_min_unit.grid(row=12, column=2, padx=20, pady=10, sticky="w")

        self.cw_pv_t_max_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Clean-water PV-T max"
        )
        # self.cw_pv_t_max_label.grid(row=12, column=2, padx=20, pady=10, sticky="e")

        self.cw_pv_t_max = ttk.IntVar(self, 0)
        self.cw_pv_t_max_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.cw_pv_t_max,
            state=DISABLED,
        )
        # self.cw_pv_t_max_entry.grid(row=12, column=3, padx=20, pady=10, sticky="ew")

        self.cw_pv_t_max_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.cw_pv_t_max_unit.grid(row=12, column=5, padx=20, pady=10, sticky="w")

        self.cw_pv_t_step_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Clean-water PV-T step size"
        )
        # self.cw_pv_t_step_label.grid(row=13, column=0, padx=20, pady=10, sticky="w")
        self.cw_pv_t_step = ttk.IntVar(self, 0)

        self.cw_pv_t_step_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.cw_pv_t_step,
            state=DISABLED,
        )
        # self.cw_pv_t_step_entry.grid(row=13, column=1, padx=20, pady=10, sticky="ew")

        self.cw_pv_t_step_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.cw_pv_t_step_unit.grid(row=13, column=2, padx=20, pady=10, sticky="w")

        # Solar Thermal step size
        self.solar_thermal_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Solar-thermal min"
        )
        # self.solar_thermal_label.grid(row=14, column=0, padx=20, pady=10, sticky="w")

        self.solar_thermal_min = ttk.IntVar(self, 0)
        self.solar_thermal_min_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.solar_thermal_min,
            state=DISABLED,
        )
        # self.solar_thermal_min_entry.grid(
        #     row=14, column=1, padx=20, pady=10, sticky="ew"
        # )

        self.solar_thermal_min_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.solar_thermal_min_unit.grid(row=14, column=2, padx=20, pady=10, sticky="w")

        self.solar_thermal_max_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Solar-thermal max"
        )
        # self.solar_thermal_max_label.grid(row=14, column=2, padx=20, pady=10, sticky="e")

        self.solar_thermal_max = ttk.IntVar(self, 0)
        self.solar_thermal_max_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.solar_thermal_max,
            state=DISABLED,
        )
        # self.solar_thermal_max_entry.grid(
        #     row=14, column=3, padx=20, pady=10, sticky="ew"
        # )

        self.solar_thermal_max_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.solar_thermal_max_unit.grid(row=14, column=5, padx=20, pady=10, sticky="w")

        self.solar_thermal_step_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Solar-thermal step size"
        )
        # self.solar_thermal_step_label.grid(
        #     row=15, column=0, padx=20, pady=10, sticky="w"
        # )
        self.solar_thermal_step = ttk.IntVar(self, 0)

        self.solar_thermal_step_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.solar_thermal_step,
            state=DISABLED,
        )
        # self.solar_thermal_step_entry.grid(
        #     row=15, column=1, padx=20, pady=10, sticky="ew"
        # )

        self.solar_thermal_step_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="panels"
        )
        # self.solar_thermal_step_unit.grid(row=15, column=2, padx=20, pady=10, sticky="w")

        # Line break
        self.line_break_label = ttk.Label(self.scrollable_optimisation_frame, text="")
        self.line_break_label.grid(row=16, column=0, padx=20, pady=10, sticky="w")

        # Hot Water Tanks step size
        self.hot_water_tanks_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Hot-water tanks"
        )
        # self.hot_water_tanks_label.grid(row=14, column=0, padx=20, pady=10, sticky="w")

        self.hot_water_tanks_min_label = ttk.Label(
            self.scrollable_optimisation_frame, text="min"
        )
        # self.hot_water_tanks_min_label.grid(
        #     row=15, column=0, padx=20, pady=10, sticky="w"
        # )

        self.hot_water_tanks_min = ttk.IntVar(self, 0)
        self.hot_water_tanks_min_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.hot_water_tanks_min,
            state=DISABLED,
        )
        # self.hot_water_tanks_min_entry.grid(
        # #     row=15, column=1, padx=20, pady=10, sticky="ew"
        # # )

        self.hot_water_tanks_min_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="tanks"
        )
        # self.hot_water_tanks_min_unit.grid(row=15, column=2, padx=20, pady=10, sticky="w")

        self.hot_water_tanks_max_label = ttk.Label(
            self.scrollable_optimisation_frame, text="max"
        )
        # self.hot_water_tanks_max_label.grid(
        #     row=15, column=2, padx=20, pady=10, sticky="e"
        # )

        self.hot_water_tanks_max = ttk.IntVar(self, 0)
        self.hot_water_tanks_max_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.hot_water_tanks_max,
            state=DISABLED,
        )
        # self.hot_water_tanks_max_entry.grid(
        #     row=15, column=3, padx=20, pady=10, sticky="ew"
        # )

        self.hot_water_tanks_max_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="tanks"
        )
        # self.hot_water_tanks_max_unit.grid(row=15, column=5, padx=20, pady=10, sticky="w")

        self.hot_water_tanks_step_label = ttk.Label(
            self.scrollable_optimisation_frame, text="step"
        )
        # self.hot_water_tanks_step_label.grid(
        #     row=15, column=5, padx=20, pady=10, sticky="e"
        # )
        self.hot_water_tanks_step = ttk.IntVar(self, 0)

        self.hot_water_tanks_step_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.solar_thermal_step,
            state=DISABLED,
        )
        # self.hot_water_tanks_step_entry.grid(
        #     row=15, column=5, padx=20, pady=10, sticky="ew"
        # )

        self.hot_water_tanks_step_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="tanks"
        )
        # self.hot_water_tanks_step_unit.grid(
        #     row=15, column=6, padx=20, pady=10, sticky="w"
        # )

        # Clean-water Tanks step size
        self.clean_water_tanks_label = ttk.Label(
            self.scrollable_optimisation_frame, text="Clean-water tanks"
        )
        # self.clean_water_tanks_label.grid(row=16, column=0, padx=20, pady=10, sticky="w")

        self.clean_water_tanks_min_label = ttk.Label(
            self.scrollable_optimisation_frame, text="min"
        )
        # self.clean_water_tanks_min_label.grid(
        #     row=17, column=0, padx=20, pady=10, sticky="w"
        # )

        self.clean_water_tanks_min = ttk.IntVar(self, 0)
        self.clean_water_tanks_min_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.clean_water_tanks_min,
            state=DISABLED,
        )
        # self.clean_water_tanks_min_entry.grid(
        #     row=17, column=1, padx=20, pady=10, sticky="ew"
        # )

        self.clean_water_tanks_min_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="tanks"
        )
        # self.clean_water_tanks_min_unit.grid(
        #     row=17, column=2, padx=20, pady=10, sticky="w"
        # )

        self.clean_water_tanks_max_label = ttk.Label(
            self.scrollable_optimisation_frame, text="max"
        )
        # self.clean_water_tanks_max_label.grid(
        #     row=17, column=2, padx=20, pady=10, sticky="e"
        # )

        self.clean_water_tanks_max = ttk.IntVar(self, 0)
        self.clean_water_tanks_max_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.clean_water_tanks_max,
            state=DISABLED,
        )
        # self.clean_water_tanks_max_entry.grid(
        #     row=17, column=3, padx=20, pady=10, sticky="ew"
        # )

        self.clean_water_tanks_max_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="tanks"
        )
        # self.clean_water_tanks_max_unit.grid(
        #     row=17, column=5, padx=20, pady=10, sticky="w"
        # )

        self.clean_water_tanks_step_label = ttk.Label(
            self.scrollable_optimisation_frame, text="step"
        )
        # self.clean_water_tanks_step_label.grid(
        #     row=17, column=5, padx=20, pady=10, sticky="e"
        # )
        self.clean_water_tanks_step = ttk.IntVar(self, 0)

        self.clean_water_tanks_step_entry = ttk.Entry(
            self.scrollable_optimisation_frame,
            bootstyle=SECONDARY,
            textvariable=self.clean_water_tanks_step,
            state=DISABLED,
        )
        # self.clean_water_tanks_step_entry.grid(
        #     row=17, column=5, padx=20, pady=10, sticky="ew"
        # )

        self.clean_water_tanks_step_unit = ttk.Label(
            self.scrollable_optimisation_frame, text="tanks"
        )
        # self.clean_water_tanks_step_unit.grid(
        #     row=17, column=6, padx=20, pady=10, sticky="w"
        # )

        # Horizontal separator
        self.separator = ttk.Separator(self.scrollable_optimisation_frame)
        self.separator.grid(row=18, column=0, columnspan=6, sticky="ew", padx=(20, 20))

        # Optimisation criterion header
        self.optimisation_criterion_label = ttk.Label(
            self.scrollable_optimisation_frame,
            text="Optimisation criterion",
            style="Bold.TLabel",
        )
        self.optimisation_criterion_label.grid(
            row=19, column=0, columnspan=4, padx=20, pady=10, sticky="w"
        )

        # Optimisation criterion frame
        # self.scrollable_optimisation_frame = ttk.Labelframe(
        #     self, style="info.TLabelframe", text="Optimisation criterion"
        # )
        # self.scrollable_optimisation_frame.grid(
        #     row=2,
        #     column=0,
        #     columnspan=2,
        #     padx=5,
        #     pady=10,
        #     ipady=40,
        #     ipadx=20,
        #     sticky="news",
        # )

        # self.scrollable_optimisation_frame.rowconfigure(0, weight=1)

        # self.scrollable_optimisation_frame.columnconfigure(0, weight=3)
        # self.scrollable_optimisation_frame.columnconfigure(1, weight=1)
        # self.scrollable_optimisation_frame.columnconfigure(2, weight=3)

        # Optimisation Min/Max set
        self.optimisation_minmax = ttk.StringVar(self, "Minimise", "Minimum/Maximum")
        self.optimisation_minmax_entry = ttk.Combobox(
            self.scrollable_optimisation_frame,
            bootstyle=INFO,
            textvariable=self.optimisation_minmax,
            width=15,
            state=READONLY,
        )
        self.optimisation_minmax_entry.grid(
            row=20, column=0, padx=20, pady=10, sticky="ew"
        )
        self.populate_minmax()

        # Min-max help
        self.minmax_help = ttk.Label(
            self.scrollable_optimisation_frame,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )
        self.minmax_help.grid(row=20, column=1, padx=10, pady=10, sticky="w")
        self.minmax_tooltip = ToolTip(
            self.minmax_help,
            bootstyle=f"{INFO}-{INVERSE}",
            text="Optimisation criterion can either be maximised or minimised "
            "depending on the type of system you are trying to configure. Criteria "
            "like costs and emissions are usually minimised, whilst reliability and "
            "uptime are usually maximised.",
        )

        # the
        self.optimisation_minmax_label = ttk.Label(
            self.scrollable_optimisation_frame, text="the"
        )
        self.optimisation_minmax_label.grid(
            row=20, column=2, padx=20, pady=10, sticky="ew"
        )

        # Optimisation criterion set
        self.optimisation_criterion = ttk.StringVar(
            self, "LCUE", "Optimisation Criterion"
        )
        self.optimisation_criterion_entry = ttk.Combobox(
            self.scrollable_optimisation_frame,
            bootstyle=INFO,
            textvariable=self.optimisation_criterion,
            state=READONLY,
        )
        self.optimisation_criterion_entry.grid(
            row=20, column=3, padx=20, pady=10, sticky="ew", ipadx=20
        )
        self.populate_available_optimisation_criterion()

        # Min-max help
        self.criterion_help = ttk.Label(
            self.scrollable_optimisation_frame,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )
        self.criterion_help.grid(row=20, column=4, padx=10, pady=10, sticky="w")
        self.criterion_help_tooltip = ToolTip(
            self.criterion_help,
            bootstyle=f"{INFO}-{INVERSE}",
            text="The optimisation criterion that you wish to maximise or minimise can "
            "be selected here. For more information on what the different criteria are "
            "and how they are calculated, refer to the documentation.",
        )

        # Line break
        self.line_break = ttk.Label(self.scrollable_optimisation_frame, text="")
        self.line_break.grid(row=21, column=1, padx=20, pady=10, sticky="w")

        # Horizontal separator
        self.separator = ttk.Separator(self.scrollable_optimisation_frame)
        self.separator.grid(row=22, column=0, columnspan=6, sticky="ew", padx=(20, 20))

        # Threshold criteria header
        self.threshold_criteria_label = ttk.Label(
            self.scrollable_optimisation_frame,
            text="Threshold criteria",
            style="Bold.TLabel",
        )
        self.threshold_criteria_label.grid(
            row=23, column=0, columnspan=6, padx=20, pady=10, sticky="w"
        )

        # Threshold criteria frame
        # self.threshold_criteria_frame = ttk.Labelframe(
        #     self, style="info.TLabelframe", text="Threshold criteria"
        # )
        # self.threshold_criteria_frame.grid(
        #     row=3,
        #     column=0,
        #     columnspan=2,
        #     padx=5,
        #     pady=10,
        #     ipady=60,
        #     ipadx=20,
        #     sticky="news",
        # )

        # self.threshold_criteria_frame.rowconfigure(0, weight=1, pad=40)
        # self.threshold_criteria_frame.rowconfigure(1, weight=4)

        # self.threshold_criteria_frame.columnconfigure(0, weight=1)
        # self.threshold_criteria_frame.columnconfigure(1, weight=1)
        # self.threshold_criteria_frame.columnconfigure(2, weight=1)
        # self.threshold_criteria_frame.columnconfigure(3, weight=1)

        # # Create the scrollable frame for threshold criteria
        # self.scrollable_threshold_frame = ScrolledFrame(self.scrollable_optimisation_frame)
        # self.scrollable_threshold_frame.grid(
        #     row=1,
        #     column=0,
        #     columnspan=4,
        #     padx=20,
        #     pady=10,
        #     sticky="ew",
        #     ipadx=20,
        #     ipady=30,
        # )

        # self.scrollable_threshold_frame.columnconfigure(0, weight=1)
        # self.scrollable_threshold_frame.columnconfigure(1, weight=1)
        # self.scrollable_threshold_frame.columnconfigure(2, weight=1)
        # self.scrollable_threshold_frame.columnconfigure(3, weight=1)

        self.threshold_criteria: list[ThresholdCriterion] = []

        def add_threshold_criterion() -> None:
            """Add a new threshold criterion to the list."""
            self.threshold_criteria.append(
                ThresholdCriterion(
                    self.scrollable_optimisation_frame,
                    ttk.StringVar(
                        self, ThresholdCriterion.default_threshold_criterion()
                    ),
                    ttk.BooleanVar(self, True),
                    ttk.DoubleVar(self, 0),
                    self.delete_criterion,
                    len(self.threshold_criteria) + 1,
                )
            )
            self.update_threshold_criteria()

        self.add_threshold_criterion_button = ttk.Button(
            self.scrollable_optimisation_frame,
            bootstyle=f"{INFO}-{OUTLINE}",
            command=add_threshold_criterion,
            text="Add threshold criterion",
        )
        self.add_threshold_criterion_button.grid(
            row=24, column=0, columnspan=4, padx=20, pady=10, sticky="w", ipadx=40
        )

        self.update_threshold_criteria()

        self.separator = ttk.Separator(self)
        self.separator.grid(row=3, column=0, columnspan=6, sticky="ew", padx=(40, 40))

        # Combines the functions to open the run screen and launch the simulation.
        self.run_optimisation_frame = ttk.Frame(self)
        self.run_optimisation_frame.grid(row=4, column=0, columnspan=6)

        self.run_optimisation_frame.columnconfigure(0, weight=1, minsize=800)
        self.run_optimisation_frame.columnconfigure(2, weight=1)
        self.run_optimisation_frame.rowconfigure(0, weight=1)

        self.run_optimisation_button = ttk.Button(
            self.run_optimisation_frame,
            text="Run Optimisation",
            bootstyle=f"{INFO}-outline",
            command=lambda operating_mode=OperatingMode.OPTIMISATION: launch_clover_run(
                operating_mode
            ),
            state=DISABLED,
        )
        self.run_optimisation_button.grid(
            row=0, column=1, padx=5, pady=10, sticky="es", ipadx=80, ipady=20
        )

        # Bind the scrolled frame to enable the optimisation button
        self.scrollable_optimisation_frame.bind("<Configure>", self._check_scrolled)

    def _check_scrolled(self, _) -> None:
        """
        Checks whether the optimisation criterion frame has been scrolled.

        Once the optimisation frame has been scrolled to the bottom, the "Run
        Optimisation" button will be enabled.

        """

        if self.scrollable_optimisation_frame.vscroll.get()[1] == 1.0:
            self.run_optimisation_button.configure(state="enabled")
        else:
            self.run_optimisation_button.configure(state=DISABLED)

    @property
    def as_dict(
        self,
    ) -> dict[
        str,
        dict[str, float] | float | list[dict[str, list[dict[str, float | str]] | str]],
    ]:
        """
        Return the optimisation screen information as a `dict`.

        In order to update the optimisation inputs file ready to run a CLOVER
        optimisation, the optimisation inputs information needs to be saved.

        :returns:
            The optimisation information ready to be saved.

        """

        return {
            ITERATION_LENGTH: self.iteration_length.get(),
            NUMBER_OF_ITERATIONS: self.number_of_iterations.get(),
            OptimisationComponent.PV_SIZE.value: {
                MAX: self.pv_max.get(),
                MIN: self.pv_min.get(),
                STEP: self.pv_step.get(),
            },
            OptimisationComponent.STORAGE_SIZE.value: {
                MAX: self.storage_max.get(),
                MIN: self.storage_min.get(),
                STEP: self.storage_step.get(),
            },
            OPTIMISATIONS: [
                {
                    OPTIMISATION_CRITERIA: [
                        {
                            ThresholdCriterion.name_to_criterion_map[
                                self.optimisation_criterion.get()
                            ]
                            .value: self.optimisation_minmax.get()
                            .lower()
                        }
                    ],
                    THRESHOLD_CRITERIA: [
                        {
                            ThresholdCriterion.name_to_criterion_map[
                                criterion.criterion_name.get()
                            ].value: criterion.value.get()
                            for criterion in self.threshold_criteria
                        }
                    ],
                }
            ],
        }

    def delete_criterion(self, criterion_to_delete: ThresholdCriterion) -> None:
        """
        Remove a threshold criterion from the `list` and the screen.

        :param: criterion
            The :class:`ThresholdCriterion` to delete.

        """

        for criterion in self.threshold_criteria:
            criterion.grid_forget()

        self.threshold_criteria = [
            entry
            for entry in self.threshold_criteria
            if entry is not criterion_to_delete
        ]
        del criterion
        self.update_threshold_criteria()

    def populate_available_optimisation_criterion(self) -> None:
        """Populate the combo box with the set of avialable batteries."""

        self.optimisation_criterion_entry["values"] = [
            str(entry) for entry in CRITERION_TO_NAME_MAP.values()
        ]

    def populate_minmax(self) -> None:
        """Populate the combo box with minmax."""

        self.optimisation_minmax_entry["values"] = [
            "Minimise",
            "Maximise",
        ]

    def set_optimisation(
        self, optimisation: Optimisation, optimisation_inputs: OptimisationParameters
    ) -> None:
        """
        Set the optimisation information based on the inputs.

        :param: optimisation
            The optimisation to use.

        :param: optimisation_inputs
            The optimisation inputs to use.

        """

        # Iteration parameters
        self.iteration_length.set(optimisation_inputs.iteration_length)
        self.iteration_length_entry.update()
        self.iteration_length_slider.set(self.iteration_length.get())

        self.number_of_iterations.set(optimisation_inputs.number_of_iterations)
        self.number_of_iterations_entry.update()
        self.number_of_iterations_slider.set(self.number_of_iterations.get())

        # Steps
        # PV steps
        self.pv_min.set(optimisation_inputs.pv_size.min)
        self.pv_min_entry.update()
        self.pv_max.set(optimisation_inputs.pv_size.max)
        self.pv_max_entry.update()
        self.pv_step.set(optimisation_inputs.pv_size.step)
        self.pv_step_entry.update()

        # Storage steps
        self.storage_min.set(optimisation_inputs.storage_size.min)
        self.storage_min_entry.update()
        self.storage_max.set(optimisation_inputs.storage_size.max)
        self.storage_max_entry.update()
        self.storage_step.set(optimisation_inputs.storage_size.step)
        self.storage_step_entry.update()

        # PV-T steps
        self.hw_pv_t_min.set(optimisation_inputs.hw_pvt_size.min)
        self.hw_pv_t_min_entry.update()
        self.hw_pv_t_max.set(optimisation_inputs.hw_pvt_size.max)
        self.hw_pv_t_max_entry.update()
        self.hw_pv_t_step.set(optimisation_inputs.hw_pvt_size.step)
        self.hw_pv_t_step_entry.update()

        self.cw_pv_t_min.set(optimisation_inputs.cw_pvt_size.min)
        self.cw_pv_t_min_entry.update()
        self.cw_pv_t_max.set(optimisation_inputs.cw_pvt_size.max)
        self.cw_pv_t_max_entry.update()
        self.cw_pv_t_step.set(optimisation_inputs.cw_pvt_size.step)
        self.cw_pv_t_step_entry.update()

        # Solar-thermal steps
        # self.solar_thermal_min.set(optimisation_inputs.hw_st_size.min)
        # self.solar_thermal_min_entry.update()
        # self.solar_thermal_max.set(optimisation_inputs.hw_st_size.max)
        # self.solar_thermal_max_entry.update()
        # self.solar_thermal_step.set(optimisation_inputs.hw_st_size.step)
        # self.solar_thermal_step_entry.update()

        # Clean water tanks steps
        self.clean_water_tanks_min.set(optimisation_inputs.clean_water_tanks.min)
        self.clean_water_tanks_min_entry.update()
        self.clean_water_tanks_max.set(optimisation_inputs.clean_water_tanks.max)
        self.clean_water_tanks_max_entry.update()
        self.clean_water_tanks_step.set(optimisation_inputs.clean_water_tanks.step)
        self.clean_water_tanks_step_entry.update()

        # Hot-water tanks steps
        self.hot_water_tanks_min.set(optimisation_inputs.hot_water_tanks.min)
        self.hot_water_tanks_min_entry.update()
        self.hot_water_tanks_max.set(optimisation_inputs.hot_water_tanks.max)
        self.hot_water_tanks_max_entry.update()
        self.hot_water_tanks_step.set(optimisation_inputs.hot_water_tanks.step)
        self.hot_water_tanks_step_entry.update()

        # Update optimisation criteria
        for criterion, criterion_mode in optimisation.optimisation_criteria.items():
            self.optimisation_criterion.set(CRITERION_TO_NAME_MAP[criterion])
            self.optimisation_criterion_entry.update()

            self.optimisation_minmax.set(criterion_mode.value.capitalize())
            self.optimisation_minmax_entry.update()

        # Update threshold criteria
        self.threshold_criteria = []
        for index, criterion in enumerate(optimisation.threshold_criteria):
            self.threshold_criteria.append(
                ThresholdCriterion(
                    self.scrollable_optimisation_frame,
                    ttk.StringVar(self, CRITERION_TO_NAME_MAP[criterion]),
                    ttk.BooleanVar(
                        self,
                        THRESHOLD_CRITERION_TO_MODE[criterion] == ThresholdMode.MAXIMUM,
                    ),
                    ttk.DoubleVar(self, optimisation.threshold_criteria[criterion]),
                    self.delete_criterion,
                    index + 1,
                )
            )

        self.update_threshold_criteria()

    def update_threshold_criteria(self) -> None:
        """Updates the threshold criteria being displayed."""

        for index, criterion in enumerate(self.threshold_criteria):
            criterion.set_index(index + 1)
            criterion.display()


class ConfigurationScreen(BaseScreen, show_navigation=True):
    """
    Represents the configuration screen.

    The configure screen contains tabbed information for configuring the screen.

    TODO: Update attributes.

    """

    def __init__(
        self,
        data_directory: str,
        location_name: ttk.StringVar,
        open_details_window: Callable,
        open_run_screen: Callable,
        output_directory_name: ttk.StringVar,
        save_configuration: Callable,
        system_lifetime: ttk.IntVar,
        update_post_run_screen_output_directory_name: Callable,
    ) -> None:
        """
        Instantiate a :class:`ConfigureFrame` instance.

        :param: data_directory
            The path to the data directory.

        :param: location_name
            The name of the location being considered.

        :param: open_details_window
            A callable function to open the details screen.

        :param: open_run_screen
            A callable function to open the run screen.

        :param: output_directory_name
            The output filename for displaying files once a run has compmleted.

        :param: save_configuration
            A callable function to save the configuration.

        :param: system_lifetime
            The lifetime of the system, in years.

        :param: update_post_run_screen_output_directory_name
            Updates the post-run screen with the correct directory to look in for the
            outputs from the CLOVER run.

        """

        super().__init__()

        self.open_run_screen: Callable = open_run_screen
        self.output_directory_name: ttk.StringVar = output_directory_name
        self.save_configuration: Callable = save_configuration
        self.system_lifetime: ttk.IntVar = system_lifetime
        self.update_post_run_screen_output_directory_name: Callable = (
            update_post_run_screen_output_directory_name
        )

        self.pack(fill="both", expand=True)
        self.columnconfigure(0, weight=1, minsize=100)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=10)
        self.columnconfigure(4, weight=1)

        self.rowconfigure(0, weight=1, minsize=100)
        self.rowconfigure(1, weight=1, minsize=550)
        self.rowconfigure(2, weight=1, minsize=80)

        self.location_label = ttk.Label(
            self,
            bootstyle=INFO,
            text=location_name.get().capitalize(),
            font=("TkDefaultFont", "16", "bold"),
        )
        self.location_label.grid(
            row=0, column=0, columnspan=3, sticky="w", padx=(60, 20), pady=20
        )

        self.location_name: ttk.Stringvar = location_name

        # Helper
        self.help_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "QMark_unhovered.png",
            )
        )

        self.config_help_icon = ttk.Label(
            self,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )
        self.config_tooltip = ToolTip(
            self.config_help_icon,
            text="Configure the scenario for your location below within the 'Configure' tab. Then use the 'Simulate' tab to simulate a system for a given lifetime and capacity the or 'Optimise' tab whereby CLOVER will determine the optimum system.",
            bootstyle=f"{INFO}-{INVERSE}",
        )
        # self.help_button = ctk.CTkButton(
        #     master=self,
        #     command=None,
        #     fg_color="transparent",
        #     image=self.help_image,
        #     text="",
        # )

        # self.help_text = ttk.Label(
        #     self,
        #     bootstyle=INFO,
        #     text="1. Configure the scenario for your location below\n"
        #     "2. Use the tabs to either\n"
        #     "    a. Simulate: Run a simulation for a given lifetime and capacity\n"
        #     "    b. Optimise: Run an optimisation to determine the optimum system",
        #     font=("TkDefaultFont", "12", "bold"),
        # )
        # self.help_text.grid(
        #     row=0, column=3, columnspan=2, sticky="e", padx=(20, 60), pady=20
        # )
        self.config_help_icon.grid(
            row=0, column=0, columnspan=3, padx=(60, 20), pady=10, sticky="e"
        )

        self.notebook_style = ttk.Style()
        self.notebook_style.configure(
            "TNotebook.Tab", font=("TkDefaultFont", "14", "bold")
        )
        # self.notebook_style.configure("TScrollbar", width=50)

        self.configuration_notebook = ttk.Notebook(self, bootstyle=f"{INFO}")
        self.configuration_notebook.grid(
            row=1, column=0, columnspan=5, sticky="news", padx=60, pady=20
        )  # Use grid

        style = ttk.Style()
        style.configure("TNotebook.Tab", width=int(self.winfo_screenwidth() / 4))

        self.configuration_frame = ConfigurationFrame(
            self.configuration_notebook,
            data_directory,
            self.help_image,
            open_details_window,
            self.pv_button_configuration_callback,
            self.storage_button_configuration_callback,
        )
        self.configuration_notebook.add(
            self.configuration_frame, text="Configure", sticky="news"
        )

        self.simulation_frame = SimulationFrame(
            self.configuration_notebook,
            self.help_image,
            lambda operating_mode=OperatingMode.SIMULATION: self.launch_clover_run(
                operating_mode
            ),
        )
        self.configuration_notebook.add(self.simulation_frame, text="Simulate")

        self.optimisation_frame = OptimisationFrame(
            self.configuration_notebook,
            self.help_image,
            lambda operating_mode=OperatingMode.OPTIMISATION: self.launch_clover_run(
                operating_mode
            ),
            self.system_lifetime,
        )
        self.configuration_notebook.add(self.optimisation_frame, text="Optimise")

        self.bottom_bar_frame = ttk.Frame(self)
        self.bottom_bar_frame.grid(row=2, column=0, columnspan=5, sticky="news")

        self.bottom_bar_frame.columnconfigure(0, weight=1)
        self.bottom_bar_frame.columnconfigure(1, weight=1)
        self.bottom_bar_frame.columnconfigure(2, weight=1)
        self.bottom_bar_frame.columnconfigure(3, weight=10)
        self.bottom_bar_frame.columnconfigure(4, weight=1)

        self.back_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "back_arrow.png",
            )
        )
        self.back_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_back(self),
            image=self.back_button_image,
        )
        self.back_button.grid(
            row=0, column=0, padx=(60, 20), pady=(10, 20), sticky="news"
        )

        self.home_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "home_icon.png",
            )
        )
        self.home_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_home(self),
            image=self.home_button_image,
        )
        self.home_button.grid(row=0, column=1, padx=20, pady=(10, 20), sticky="news")

        self.forward_button_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                IMAGES_DIRECTORY,
                "forward_arrow.png",
            )
        )
        self.forward_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=f"{SECONDARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_forward(self),
            image=self.forward_button_image,
        )
        self.forward_button.grid(row=0, column=2, padx=20, pady=(10, 20), sticky="news")

        self.advanced_settings_button = ttk.Button(
            self.bottom_bar_frame,
            bootstyle=INFO,
            text="Advanced settings",
            command=open_details_window,
        )
        self.advanced_settings_button.grid(
            row=0,
            column=4,
            sticky="nes",
            padx=(20, 60),
            pady=(10, 20),
            ipadx=80,
            ipady=20,
        )

    def launch_clover_run(self, operating_mode: OperatingMode) -> None:
        """Launch a CLOVER simulation."""

        # Save all input files before running.
        self.save_configuration()

        # Assemble arguments and call to CLOVER.
        clover_args: list[str] = [
            "-l",
            str(self.location_name.get()),
        ]

        # Append simulation arguments:
        if operating_mode == OperatingMode.SIMULATION:
            clover_args.extend(["-sim", "-a"])

            # Append the PV size if PV is selected
            if self.configuration_frame.solar_pv_selected.get():
                clover_args.extend(
                    [
                        "-pv",
                        str(self.simulation_frame.pv_size.get()),
                    ]
                )

            # Append the battery size if batteries are selected
            if self.configuration_frame.battery_selected.get():
                clover_args.extend(
                    [
                        "-b",
                        str(self.simulation_frame.storage_size.get()),
                    ]
                )

            if not self.simulation_frame.generate_plots.get():
                clover_args.append("-sp")

            # Append the datetime to the output name then append to the arguments
            clover_args.extend(
                [
                    "-o",
                    (
                        output_name := str(self.simulation_frame.output_name.get())
                        + datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S_%f")
                    ),
                ]
            )

            # Set the output filename variable
            self.output_directory_name.set(output_name)
            self.update_post_run_screen_output_directory_name(
                os.path.join(
                    get_locations_foldername(),
                    self.location_name.get(),
                    SIMULATION_OUTPUTS_FOLDER
                    if operating_mode == OperatingMode.SIMULATION
                    else OPTIMISATION_OUTPUTS_FOLDER,
                    (self.output_directory_name.get()),
                )
            )

        if operating_mode == OperatingMode.OPTIMISATION:
            clover_args.extend(["-opt"])

            # Append the datetime to the output name then append to the arguments
            # self.simulation_frame.output_name.get() + datetime.datetime.now().strftime("_%Y_%m_%d_%H_%M_%S_%f")

        self.clover_thread = clover_thread(clover_args)
        self.open_run_screen(self.clover_thread)

    def pv_button_configuration_callback(self, solar_pv_selected: bool) -> None:
        """
        Used to toggle the PV buttons on other configuration screens based on scenario.

        :param: solar_pv_selected
            Whether solar PV is selected.

        """

        if solar_pv_selected:
            self.simulation_frame.pv_size_entry.configure(state=(_enabled := "enabled"))
            self.optimisation_frame.pv_max_entry.configure(state=_enabled)
            self.optimisation_frame.pv_min_entry.configure(state=_enabled)
            self.optimisation_frame.pv_step_entry.configure(state=_enabled)
        else:
            self.simulation_frame.pv_size_entry.configure(state=DISABLED)
            self.simulation_frame.pv_size.set(0)
            self.optimisation_frame.pv_max_entry.configure(state=DISABLED)
            self.optimisation_frame.pv_min_entry.configure(state=DISABLED)
            self.optimisation_frame.pv_step_entry.configure(state=DISABLED)

    def storage_button_configuration_callback(self, batteries_selected: bool) -> None:
        """
        Used to toggle the battery buttons on configuration screens based on scenario.

        :param: batteries_selected
            Whether batteries are selected.

        """

        if batteries_selected:
            self.simulation_frame.storage_size_entry.configure(
                state=(_enabled := "enabled")
            )
            self.optimisation_frame.storage_max_entry.configure(state=_enabled)
            self.optimisation_frame.storage_min_entry.configure(state=_enabled)
            self.optimisation_frame.storage_step_entry.configure(state=_enabled)
        else:
            self.simulation_frame.storage_size_entry.configure(state=DISABLED)
            self.simulation_frame.storage_size.set(0)
            self.optimisation_frame.storage_max_entry.configure(state=DISABLED)
            self.optimisation_frame.storage_min_entry.configure(state=DISABLED)
            self.optimisation_frame.storage_step_entry.configure(state=DISABLED)

    def set_location(self, location_name: str) -> None:
        """
        Set the location name on the screen.

        :param: location_name
            The name of the location to set.

        """

        self.location_name.set(location_name)
        self.location_label.configure(text=self.location_name.get())
