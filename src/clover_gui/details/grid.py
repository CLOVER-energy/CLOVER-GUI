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

from typing import Callable

import pandas as pd
import ttkbootstrap as ttk

from clover.impact.finance import COST, ImpactingComponent
from clover.impact.ghgs import INITIAL_GHGS, FINAL_GHGS
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from ..__utils__ import DETAILS_GEOMETRY

__all__ = ("GridFrame",)

# Infrastructure costs:
#   Keyword for the infrastructure costs.
_INFRASTRUCTURE_COSTS: str = "infrastructure_costs"


class GridFrame(ttk.Frame):
    """
    Represents the Grid frame.

    Contains settings for grid connection.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.add_grid_profile_to_scenario_frame: Callable | None = None
        self.set_profiles_on_system_frame: Callable | None = None

        self.rowconfigure(0, weight=1, minsize=40)
        self.rowconfigure(1, weight=1, minsize=40)
        self.rowconfigure(2, weight=1, minsize=40)
        self.rowconfigure(3, weight=1, minsize=40)
        self.rowconfigure(4, weight=6, minsize=500)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        for index in range(4):
            self.columnconfigure(index, weight=1)

        # Grid-profile combobox
        self.grid_profile_name = ttk.StringVar(value="default")

        self.grid_profile_values: dict[str, ttk.StringVar] = {
            "default": self.grid_profile_name,
            "all": ttk.StringVar(value="all"),
            "none": ttk.StringVar(value="none"),
        }

        self.grid_profile_combobox = ttk.Combobox(
            self,
            bootstyle=SUCCESS,
            textvariable=self.grid_profile_name,
            state=READONLY,
        )
        self.grid_profile_combobox.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.populate_available_profiles()

        # Grid profile name
        self.grid_profile_label = ttk.Label(self, text="Profile name")
        self.grid_profile_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.grid_profile_entry = ttk.Entry(
            self, bootstyle=SUCCESS, textvariable=self.grid_profile_name
        )
        self.grid_profile_entry.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
        self.grid_profile_entry.bind("<Return>", self.enter_grid_profile_name)
        self.grid_profile_combobox.bind(
            "<<ComboboxSelected>>", self.select_grid_profile
        )

        # Save grid-profile name button
        self.save_profile_name_button = ttk.Button(
            self,
            bootstyle=f"{SUCCESS}-{TOOLBUTTON}",
            text="Save",
            command=self.enter_grid_profile_name,
        )
        self.save_profile_name_button.grid(
            row=0, column=3, padx=10, pady=5, sticky="w", ipadx=20
        )

        # New profile
        self.new_profile_button = ttk.Button(
            self,
            bootstyle=f"{SUCCESS}-{OUTLINE}",
            command=self.add_profile,
            text="New grid profile",
        )
        self.new_profile_button.grid(row=1, column=0, rowspan=3, padx=10, pady=5)

        # Grid costs
        self.grid_cost_label = ttk.Label(self, text="Grid Cost")
        self.grid_cost_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.grid_cost = ttk.DoubleVar(self, 0)

        self.grid_cost_entry = ttk.Entry(
            self, textvariable=self.grid_cost, bootstyle=SUCCESS
        )
        self.grid_cost_entry.grid(
            row=1, column=2, padx=10, pady=5, ipadx=20, sticky="ew"
        )
        self.grid_cost_units_label = ttk.Label(self, text="$/kWh")
        self.grid_cost_units_label.grid(row=1, column=3, padx=10, pady=5, sticky="w")

        # Initial Grid Emissions
        self.initial_grid_ghgs_label = ttk.Label(self, text="Initial Grid Emissions")
        self.initial_grid_ghgs_label.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.initial_grid_ghgs = ttk.DoubleVar(value=0)

        self.initial_grid_ghgs_entry = ttk.Entry(
            self, textvariable=self.initial_grid_ghgs, bootstyle=SUCCESS
        )
        self.initial_grid_ghgs_entry.grid(
            row=2, column=2, padx=10, pady=5, ipadx=20, sticky="ew"
        )

        self.initial_grid_ghgs_units = ttk.Label(self, text="kgCO2/kWh")
        self.initial_grid_ghgs_units.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Final Grid Emissions
        self.final_grid_ghgs_label = ttk.Label(self, text="Final Grid Emissions")
        self.final_grid_ghgs_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.final_grid_ghgs = ttk.DoubleVar(value=0)

        self.final_grid_ghgs_entry = ttk.Entry(
            self, textvariable=self.final_grid_ghgs, bootstyle=SUCCESS
        )
        self.final_grid_ghgs_entry.grid(
            row=3, column=2, padx=10, pady=5, ipadx=20, sticky="ew"
        )

        self.final_grid_ghgs_units = ttk.Label(self, text="kgCO2/kWh")
        self.final_grid_ghgs_units.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        # Graph
        self.graph_frame = ttk.Labelframe(
            self,
            style="success.TLabelframe",
        )
        self.graph_frame.grid(
            row=4,
            column=0,
            columnspan=4,
            padx=5,
            pady=10,
            ipady=100,
            ipadx=20,
            sticky="news",
        )

        self.graph_frame.rowconfigure(0, weight=10)
        self.graph_frame.rowconfigure(1, weight=1)
        self.graph_frame.rowconfigure(2, weight=1)

        for index in range(25):
            self.graph_frame.columnconfigure(index, weight=1)

        self.update_graph_frame_label()

        self.probabilities: dict[str, dict[int, ttk.DoubleVar]] = {
            key: {hour: ttk.DoubleVar(self.graph_frame, 0.3) for hour in range(24)}
            for key in self.grid_profile_values
        }
        self.probability_sliders: dict[str, dict[int, ttk.Scale]] = {
            key: {} for key in self.grid_profile_values
        }
        self.probability_entries: dict[str, dict[int, ttk.Entry]] = {
            key: {} for key in self.grid_profile_values
        }

        for grid_profile in self.grid_profile_values:
            for hour in range(24):
                self.probability_sliders[grid_profile][hour] = ttk.Scale(
                    self.graph_frame,
                    from_=1,
                    to=0,
                    value=self.probabilities[grid_profile][hour].get(),
                    variable=self.probabilities[grid_profile][hour],
                    style=SUCCESS,
                    orient=VERTICAL,
                    length=300,
                )

                self.probability_entries[grid_profile][hour] = ttk.Entry(
                    self.graph_frame,
                    bootstyle=SUCCESS,
                    textvariable=self.probabilities[grid_profile][hour],
                    width=4,
                )
                self.probability_entries[grid_profile][hour].bind(
                    "<Return>",
                    lambda _, grid_profile=grid_profile, hour=hour: self.enter_probability(
                        grid_profile, hour
                    ),
                )

        self.update_sliders()

        self.hour_labels: dict[int, ttk.Label] = {}

        for hour in range(24):
            self.hour_labels[hour] = ttk.Label(
                self.graph_frame,
                text=f"{'12' if (twelve_hour:=hour % 12) == 0 else twelve_hour} {'am' if hour < 12 else 'pm'}",
            )
            self.hour_labels[hour].grid(row=2, column=hour, sticky="news")

        self.x_axis_label = ttk.Label(self.graph_frame, text="Hour of the day")
        self.x_axis_label.grid(row=3, column=11, columnspan=3, sticky="ew")

        # TODO: Add configuration frame widgets and layout

    def add_profile(
        self,
        seed_profile_name: str | None = None,
        seed_profile_probabilities: dict[int, float] | None = None,
    ) -> None:
        """
        Called when a user presses the new grid-profile button.

        :param: seed_profile_name
            The name to use for the profile.

        :param: seed_profile_proababilities
            The grid profile probabilities, as a map between the hour and the
            probabilities at each hour, to use.

        """

        if seed_profile_name is None:
            # Determine the new name
            new_name = "new{suffix}"
            index = 0
            suffix = ""
            while new_name.format(suffix=suffix) in self.grid_profile_values:
                index += 1
                suffix = f"_{index}"

            new_name = new_name.format(suffix=suffix)
        else:
            new_name = seed_profile_name

        self.grid_profile_values[new_name] = ttk.StringVar(self, new_name)

        # Add the new profile to the system frame.
        self.add_grid_profile_to_scenario_frame(new_name)

        # Create new probabilities and sliders
        if seed_profile_probabilities is None:
            self.probabilities[new_name] = {
                hour: ttk.DoubleVar(self.graph_frame, 0.3) for hour in range(24)
            }
        else:
            self.probabilities[new_name] = {
                hour: ttk.DoubleVar(self.graph_frame, probability)
                for hour, probability in seed_profile_probabilities.items()
            }

        self.probability_sliders[new_name] = {}
        self.probability_entries[new_name] = {}
        for hour in range(24):
            self.probability_sliders[new_name][hour] = ttk.Scale(
                self.graph_frame,
                from_=1,
                to=0,
                value=self.probabilities[new_name][hour].get(),
                variable=self.probabilities[new_name][hour],
                style=SUCCESS,
                orient=VERTICAL,
                length=300,
            )

            self.probability_entries[new_name][hour] = ttk.Entry(
                self.graph_frame,
                bootstyle=SUCCESS,
                textvariable=self.probabilities[new_name][hour],
                width=4,
            )
            self.probability_entries[new_name][hour].bind(
                "<Return>",
                lambda _, grid_profile=new_name, hour=hour: self.enter_probability(
                    new_name, hour
                ),
            )

        # Update the probability sliders on the screen
        self.grid_profile_name = self.grid_profile_values[new_name]
        self.populate_available_profiles()
        self.grid_profile_combobox.configure(textvariable=self.grid_profile_name)
        self.grid_profile_entry.configure(textvariable=self.grid_profile_name)
        self.update_graph_frame_label()

        # Update the sliders
        self.update_sliders()

    @property
    def as_dataframe(self) -> pd.DataFrame:
        """
        Return the grid profiles as a :class:`pandas.DataFrame` for saving.

        :returns:
            A :class:`pandas.DataFrame` containing the grid-profile information.

        """

        return pd.DataFrame(
            {
                profile_name: [
                    self.probability_entries[profile_name][hour].get()
                    for hour in range(24)
                ]
                for profile_name in self.grid_profile_values
            }
        )

    @property
    def impact_information(self) -> dict[str, float]:
        return {
            COST: self.grid_cost.get(),
            INITIAL_GHGS: self.initial_grid_ghgs.get(),
            FINAL_GHGS: self.final_grid_ghgs.get(),
        }

    def enter_grid_profile_name(self, _=None) -> None:
        """Called when someone enters a new grid profile name."""
        self.probability_sliders = {
            self.grid_profile_values[key].get(): value
            for key, value in self.probability_sliders.items()
        }
        self.probability_entries = {
            self.grid_profile_values[key].get(): value
            for key, value in self.probability_entries.items()
        }
        self.probabilities = {
            self.grid_profile_values[key].get(): value
            for key, value in self.probabilities.items()
        }
        self.grid_profile_values = {
            entry.get(): entry for entry in self.grid_profile_values.values()
        }
        self.populate_available_profiles()
        self.update_graph_frame_label()

        # Update the profile names on the system frame.
        self.set_profiles_on_system_frame(list(self.grid_profile_values.keys()))

    def enter_probability(self, grid_profile, hour):
        self.probabilities[grid_profile][hour].set(
            max(min(float(self.probability_entries[hour].get()), 1), 0)
        )
        self.probability_sliders[hour].set(self.probabilities[hour].get())

    def populate_available_profiles(self) -> None:
        self.grid_profile_combobox["values"] = [
            entry.get() for entry in self.grid_profile_values.values()
        ]

    def select_grid_profile(self, _) -> None:
        # Determine the grid profile name pre- and post-selection
        previous_grid_profile_name: str = {
            (entry == self.grid_profile_name): key
            for key, entry in self.grid_profile_values.items()
        }[True]
        selected_grid_profile_name: str = self.grid_profile_combobox.get()

        # Reset the value of the old variable
        self.grid_profile_values[previous_grid_profile_name].set(
            previous_grid_profile_name
        )

        # Set the variable to be the new selected variable
        self.grid_profile_name = self.grid_profile_values[selected_grid_profile_name]
        self.grid_profile_combobox.configure(textvariable=self.grid_profile_name)
        self.grid_profile_entry.configure(textvariable=self.grid_profile_name)
        self.update_graph_frame_label()

        # Update the sliders
        self.update_sliders()

    def set_profiles(
        self, grid_times: pd.DataFrame, impact_inputs: dict[str, float]
    ) -> None:
        """
        Set the grid profile times based on the inputs.

        :param: grid_times
            A :class:`pd.DataFrame` containing the grid-times frame.

        :param: impact_inputs
            The impact inputs information

        """

        self.grid_profile_values = {}
        self.probabilities = {}
        self.probability_sliders = {}
        self.probability_entries = {}

        for profile_name, profile_probabilities in grid_times.to_dict().items():
            self.add_profile(
                seed_profile_name=profile_name,
                seed_profile_probabilities=profile_probabilities,
            )

        # Costs
        self.grid_cost.set(impact_inputs[ImpactingComponent.GRID.value][COST])

        # GHGs
        self.initial_grid_ghgs.set(
            impact_inputs[ImpactingComponent.GRID.value][INITIAL_GHGS]
        )
        self.initial_grid_ghgs_entry.update()

        self.final_grid_ghgs.set(
            impact_inputs[ImpactingComponent.GRID.value][FINAL_GHGS]
        )
        self.final_grid_ghgs_entry.update()

    def update_graph_frame_label(self) -> None:
        self.graph_frame.configure(
            text="Hourly probability of grid availability for grid "
            f"'{self.grid_profile_name.get().capitalize()}'."
        )

    def update_sliders(self) -> None:
        """Updates the sliders to display those for the current grid profile."""
        # Clear the previous sliders
        for profile in self.grid_profile_values:
            for slider in self.probability_sliders[profile].values():
                slider.grid_forget()
            for entry in self.probability_entries[profile].values():
                entry.grid_forget()

        # Display the probabilitiy sliders for the current grid profile
        for hour in range(24):
            self.probability_sliders[self.grid_profile_name.get()][hour].grid(
                row=0, column=hour, padx=0, pady=5, sticky="ns"
            )
            self.probability_entries[self.grid_profile_name.get()][hour].grid(
                row=1, column=hour, padx=0, pady=5, sticky="ew"
            )
