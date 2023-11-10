#!/usr/bin/python3.10
########################################################################################
# diesel.py - The diesel module for CLOVER-GUI application.                            #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 30/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################


import tkinter as tk

from typing import Callable

import ttkbootstrap as ttk

from clover.fileparser import (
    COSTS,
    DIESEL_CONSUMPTION,
    DIESEL_GENERATORS,
    EMISSIONS,
    MINIMUM_LOAD,
    NAME,
)
from clover.impact.finance import (
    COST,
    COST_DECREASE,
    ImpactingComponent,
    INSTALLATION_COST,
    INSTALLATION_COST_DECREASE,
    OM,
)
from clover.impact.ghgs import (
    GHGS,
    GHG_DECREASE,
    INSTALLATION_GHGS,
    INSTALLATION_GHGS_DECREASE,
    OM_GHGS,
)
from clover.simulation.diesel import DieselGenerator
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


__all__ = ("DieselFrame",)


class GeneratorFrame(ttk.Frame):
    """
    Represents the Diesel generator frame.

    Contains settings for the diesel generator units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scrolled_frame = ScrolledFrame(self)
        self.scrolled_frame.grid(row=0, column=0, padx=10, pady=5, sticky="news")

        self.scrolled_frame.rowconfigure(0, weight=1)
        self.scrolled_frame.rowconfigure(1, weight=1)
        self.scrolled_frame.rowconfigure(2, weight=1)
        self.scrolled_frame.rowconfigure(3, weight=1)
        self.scrolled_frame.rowconfigure(4, weight=1)
        self.scrolled_frame.rowconfigure(5, weight=1)
        self.scrolled_frame.rowconfigure(6, weight=1)
        self.scrolled_frame.rowconfigure(7, weight=1)
        self.scrolled_frame.rowconfigure(8, weight=1)
        self.scrolled_frame.rowconfigure(9, weight=1)
        self.scrolled_frame.rowconfigure(10, weight=1)
        self.scrolled_frame.rowconfigure(11, weight=1)
        self.scrolled_frame.rowconfigure(12, weight=1)
        self.scrolled_frame.rowconfigure(13, weight=1)
        self.scrolled_frame.rowconfigure(14, weight=1)
        self.scrolled_frame.rowconfigure(15, weight=1)
        self.scrolled_frame.rowconfigure(16, weight=1)

        self.scrolled_frame.columnconfigure(0, weight=10)  # First row has the header
        self.scrolled_frame.columnconfigure(1, weight=10)  # These rows have entries
        self.scrolled_frame.columnconfigure(2, weight=1)  # These rows have entries
        self.scrolled_frame.columnconfigure(3, weight=1)  # These rows have entries

        self.add_generator_to_scenario_frame: Callable | None = None
        self.set_generators_on_system_frame: Callable | None = None

        # Diesel generator being selected
        self.diesel_generator_selected_label = ttk.Label(
            self.scrolled_frame, text="Diesel generator to\nconfigure"
        )
        self.diesel_generator_selected_label.grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )

        self.diesel_generator_selected = ttk.StringVar(
            self, "Load-following", "diesel_generator_selected"
        )
        self.diesel_generator_name_values = {
            (diesel_generator_name := "Load-following"): self.diesel_generator_selected,
            (diesel_generator_name := "Cycle-charging"): ttk.StringVar(
                self, diesel_generator_name
            ),
        }

        self.diesel_generator_selected_combobox = ttk.Combobox(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.diesel_generator_selected,
        )
        self.diesel_generator_selected_combobox.grid(
            row=0, column=1, padx=10, pady=5, sticky="w", ipadx=60
        )
        self.diesel_generator_selected_combobox.bind(
            "<<ComboboxSelected>>", self.select_diesel_generator
        )
        self.populate_available_generators()

        # New generator
        self.new_generator_button = ttk.Button(
            self.scrolled_frame,
            bootstyle=f"{DANGER}-{OUTLINE}",
            command=self.add_diesel_generator,
            text="New generator",
        )
        self.new_generator_button.grid(row=0, column=2, padx=10, pady=5, ipadx=80)

        # Diesel generator name
        self.diesel_generator_name_label = ttk.Label(
            self.scrolled_frame, text="Diesel generator name"
        )
        self.diesel_generator_name_label.grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )

        self.diesel_generator_name_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.diesel_generator_selected,
        )
        self.diesel_generator_name_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )
        self.diesel_generator_name_entry.bind(
            "<Return>", self.enter_diesel_generator_name
        )

        # Save diesel-generator name button
        self.save_generator_name_button = ttk.Button(
            self.scrolled_frame,
            bootstyle=f"{DANGER}-{TOOLBUTTON}",
            text="Save",
            command=self.enter_diesel_generator_name,
        )
        self.save_generator_name_button.grid(
            row=1, column=2, padx=10, pady=5, sticky="w", ipadx=20
        )

        # Diesel generator capacity
        self.diesel_generator_capacity_label = ttk.Label(
            self.scrolled_frame, text="Capacity"
        )
        self.diesel_generator_capacity_label.grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )

        self.diesel_generator_capacities: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 1, f"{diesel_generator_name}_diesel_generator_capacity"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }

        self.diesel_generator_capacity_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.diesel_generator_capacities[
                self.diesel_generator_selected.get()
            ],
            style=DANGER,
        )
        self.diesel_generator_capacity_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.diesel_generator_capacity_unit = ttk.Label(self.scrolled_frame, text="kW")
        self.diesel_generator_capacity_unit.grid(
            row=2, column=2, padx=10, pady=5, sticky="w"
        )

        # Fuel consumption
        self.fuel_consumption_label = ttk.Label(
            self.scrolled_frame, text="Fuel consumption"
        )
        self.fuel_consumption_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.fuel_consumption: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0.4, f"{diesel_generator_name}_fuel_consumption"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }

        self.fuel_consumption_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.fuel_consumption[self.diesel_generator_selected.get()],
        )
        self.fuel_consumption_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        self.fuel_consumption_unit = ttk.Label(
            self.scrolled_frame, text=f"litres / kW-hour"
        )
        self.fuel_consumption_unit.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        # Minimum load
        self.minimum_load_label = ttk.Label(
            self.scrolled_frame, text="Minimum capacity factor"
        )
        self.minimum_load_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.minimum_load: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 20, f"{diesel_generator_name}_minimum_load"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }

        def scalar_minimum_load(_):
            self.minimum_load[self.diesel_generator_selected.get()].set(
                round(self.minimum_load_slider.get(), 1),
            )
            self.minimum_load_entry.update()

        self.minimum_load_slider = ttk.Scale(
            self.scrolled_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_minimum_load,
            bootstyle=DANGER,
            variable=self.minimum_load[self.diesel_generator_selected.get()],
            # state=DISABLED
        )
        self.minimum_load_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        def enter_minimum_load(_):
            self.minimum_load_entry.set(
                round(min(max(self.minimum_load_entry.get(), 0), 100), 2)
            )
            self.minimum_load[self.diesel_generator_selected.get()].set(
                round(self.minimum_load_entry.get(), 2)
            )
            self.minimum_load_slider.set(
                round(self.minimum_load[self.diesel_generator_selected.get()].get(), 2)
            )

        self.minimum_load_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.minimum_load[self.diesel_generator_selected.get()],
        )
        self.minimum_load_entry.grid(row=4, column=2, padx=10, pady=5, sticky="ew")
        self.minimum_load_entry.bind("<Return>", enter_minimum_load)

        self.minimum_load_unit = ttk.Label(self.scrolled_frame, text=f"% of capacity")
        self.minimum_load_unit.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        # Cost
        self.cost_label = ttk.Label(self.scrolled_frame, text="Diesel generator cost")
        self.cost_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.costs: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self.scrolled_frame, 0, f"{diesel_generator_name}_cost"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.cost_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.costs[self.diesel_generator_selected.get()],
        )
        self.cost_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew", ipadx=80)

        self.cost_unit = ttk.Label(self.scrolled_frame, text="$ / kW")
        self.cost_unit.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # Cost decrease
        self.cost_decrease_label = ttk.Label(
            self.scrolled_frame, text="Diesel generator cost\nchange"
        )
        self.cost_decrease_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.cost_decrease: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_cost_decrease"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.cost_decrease_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.cost_decrease[self.diesel_generator_selected.get()],
        )
        self.cost_decrease_entry.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.cost_decrease_unit = ttk.Label(self.scrolled_frame, text="%  / year")
        self.cost_decrease_unit.grid(row=6, column=2, padx=10, pady=5, sticky="w")

        # Installation costs
        self.installation_cost_label = ttk.Label(
            self.scrolled_frame, text="Diesel generator installation\ncost"
        )
        self.installation_cost_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.installation_costs: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_installation_cost"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.installation_cost_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.installation_costs[self.diesel_generator_selected.get()],
        )
        self.installation_cost_entry.grid(
            row=7, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.installation_cost_unit = ttk.Label(
            self.scrolled_frame, text="$ / kW installed"
        )
        self.installation_cost_unit.grid(row=7, column=2, padx=10, pady=5, sticky="w")

        # Cost decrease
        self.installation_cost_decrease_label = ttk.Label(
            self.scrolled_frame, text="Diesel generator installation\ncost change"
        )
        self.installation_cost_decrease_label.grid(
            row=8, column=0, padx=10, pady=5, sticky="w"
        )

        self.installation_cost_decrease: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_installation_cost_decrease"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.installation_cost_decrease_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.installation_cost_decrease[
                self.diesel_generator_selected.get()
            ],
        )
        self.installation_cost_decrease_entry.grid(
            row=8, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.installation_cost_decrease_unit = ttk.Label(
            self.scrolled_frame, text="%  / year"
        )
        self.installation_cost_decrease_unit.grid(
            row=8, column=2, padx=10, pady=5, sticky="w"
        )

        # OPEX costs
        self.opex_costs_label = ttk.Label(self.scrolled_frame, text="OPEX (O&M) costs")
        self.opex_costs_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        self.o_and_m_costs: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_o_and_m_costs"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.o_and_m_costs_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.o_and_m_costs[self.diesel_generator_selected.get()],
        )
        self.o_and_m_costs_entry.grid(
            row=9, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.o_and_m_costs_unit = ttk.Label(self.scrolled_frame, text="$ / kW / year")
        self.o_and_m_costs_unit.grid(row=9, column=2, padx=10, pady=5, sticky="w")

        # Embedded emissions
        self.embedded_emissions_label = ttk.Label(
            self.scrolled_frame, text="Diesel generator embedded\nemissions"
        )
        self.embedded_emissions_label.grid(
            row=10, column=0, padx=10, pady=5, sticky="w"
        )

        self.embedded_emissions: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_ghgs"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.embedded_emissions_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.embedded_emissions[self.diesel_generator_selected.get()],
        )
        self.embedded_emissions_entry.grid(
            row=10, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.embedded_emissions_unit = ttk.Label(
            self.scrolled_frame, text="kgCO2eq / kW"
        )
        self.embedded_emissions_unit.grid(row=10, column=2, padx=10, pady=5, sticky="w")

        # Annual emissions decrease
        self.annual_emissions_decrease_label = ttk.Label(
            self.scrolled_frame, text="Diesel generator embedded\nemissions change"
        )
        self.annual_emissions_decrease_label.grid(
            row=11, column=0, padx=10, pady=5, sticky="w"
        )

        self.annual_emissions_decrease: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_ghgs_decrease"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.annual_emissions_decrease_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.annual_emissions_decrease[
                self.diesel_generator_selected.get()
            ],
        )
        self.annual_emissions_decrease_entry.grid(
            row=11, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.annual_emissions_decrease_unit = ttk.Label(
            self.scrolled_frame, text="% / year"
        )
        self.annual_emissions_decrease_unit.grid(
            row=11, column=2, padx=10, pady=5, sticky="w"
        )

        # Embedded installation emissions
        self.installation_emissions_label = ttk.Label(
            self.scrolled_frame, text="Diesel installation emissions"
        )
        self.installation_emissions_label.grid(
            row=12, column=0, padx=10, pady=5, sticky="w"
        )

        self.installation_emissions: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_installation_ghgs"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.installation_emissions_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.installation_emissions[
                self.diesel_generator_selected.get()
            ],
        )
        self.installation_emissions_entry.grid(
            row=12, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.installation_emissions_unit = ttk.Label(
            self.scrolled_frame, text="kgCO2eq / kW installed"
        )
        self.installation_emissions_unit.grid(
            row=12, column=2, padx=10, pady=5, sticky="w"
        )

        # Annual installation emissions decrease
        self.installation_emissions_decrease_label = ttk.Label(
            self.scrolled_frame, text="Diesel installation emissions\nchange"
        )
        self.installation_emissions_decrease_label.grid(
            row=13, column=0, padx=10, pady=5, sticky="w"
        )

        self.installation_emissions_decrease: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_installation_ghgs_decrease"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.installation_emissions_decrease_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.installation_emissions_decrease[
                self.diesel_generator_selected.get()
            ],
        )
        self.installation_emissions_decrease_entry.grid(
            row=13, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.installation_emissions_decrease_unit = ttk.Label(
            self.scrolled_frame, text="% / year"
        )
        self.installation_emissions_decrease_unit.grid(
            row=13, column=2, padx=10, pady=5, sticky="w"
        )

        # O&M emissions
        self.om_emissions_label = ttk.Label(self.scrolled_frame, text="O&M emissions")
        self.om_emissions_label.grid(row=14, column=0, padx=10, pady=5, sticky="w")

        self.om_emissions: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_o_and_m_ghgs"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.om_emissions_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=DANGER,
            textvariable=self.om_emissions[self.diesel_generator_selected.get()],
        )
        self.om_emissions_entry.grid(
            row=14, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.om_emissions_unit = ttk.Label(
            self.scrolled_frame, text="kgCO2eq / kW / year"
        )
        self.om_emissions_unit.grid(row=14, column=2, padx=10, pady=5, sticky="w")

    def add_diesel_generator(self) -> None:
        """Called when a user presses the new diesel generator button."""

        # Determine the new name
        new_name = "New generator {suffix}"
        index = 0
        suffix = ""
        while new_name.format(suffix=suffix) in self.diesel_generator_name_values:
            index += 1
            suffix = f"({index})"

        new_name = new_name.format(suffix=suffix)

        self.diesel_generator_name_values[new_name] = ttk.StringVar(self, new_name)
        self.populate_available_generators()

        # Update all the mappings stored
        self.diesel_generator_capacities[new_name] = ttk.DoubleVar(self, 0)
        self.fuel_consumption[new_name] = ttk.DoubleVar(self, 0)
        self.minimum_load[new_name] = ttk.DoubleVar(self, 50)
        self.costs[new_name] = ttk.DoubleVar(self, 0)
        self.cost_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.installation_costs[new_name] = ttk.DoubleVar(self, 0)
        self.installation_cost_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.o_and_m_costs[new_name] = ttk.DoubleVar(self, 0)
        self.embedded_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.annual_emissions_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.installation_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.installation_emissions_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.om_emissions[new_name] = ttk.DoubleVar(self, 0)

        # Select the new battery and update the screen
        self.diesel_generator_selected = self.diesel_generator_name_values[new_name]
        self.diesel_generator_selected_combobox.configure(
            textvariable=self.diesel_generator_selected
        )
        self.diesel_generator_name_entry.configure(
            textvariable=self.diesel_generator_selected
        )
        self.update_diesel_generator_frame()

        # Add the generator to the system frame
        self.add_generator_to_scenario_frame(new_name)

    def enter_diesel_generator_name(self, _=None) -> None:
        """Called when someone enters a new diesel_generator name."""
        self.populate_available_generators()

        # Update all the mappings stored
        self.diesel_generator_capacities = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.diesel_generator_capacities.items()
            if key in self.diesel_generator_name_values
        }
        self.fuel_consumption = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.fuel_consumption.items()
            if key in self.diesel_generator_name_values
        }
        self.minimum_load = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.minimum_load.items()
            if key in self.diesel_generator_name_values
        }
        self.costs = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.costs.items()
            if key in self.diesel_generator_name_values
        }
        self.cost_decrease = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.cost_decrease.items()
            if key in self.diesel_generator_name_values
        }
        self.installation_costs = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.installation_costs.items()
            if key in self.diesel_generator_name_values
        }
        self.installation_cost_decrease = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.installation_cost_decrease.items()
            if key in self.diesel_generator_name_values
        }
        self.o_and_m_costs = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.o_and_m_costs.items()
            if key in self.diesel_generator_name_values
        }
        self.embedded_emissions = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.embedded_emissions.items()
            if key in self.diesel_generator_name_values
        }
        self.annual_emissions_decrease = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.annual_emissions_decrease.items()
            if key in self.diesel_generator_name_values
        }
        self.installation_emissions = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.installation_emissions.items()
            if key in self.diesel_generator_name_values
        }
        self.installation_emissions_decrease = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.installation_emissions_decrease.items()
            if key in self.diesel_generator_name_values
        }
        self.om_emissions = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.om_emissions.items()
            if key in self.diesel_generator_name_values
        }

        # Update the diesel generator values.
        self.diesel_generator_name_values = {
            entry.get(): entry for entry in self.diesel_generator_name_values.values()
        }

        # Update the generator names on the system frame.
        self.set_generators_on_system_frame(
            list(self.diesel_generator_name_values.keys())
        )

    def get_generators(self) -> dict[str, dict[str, dict[str, float] | float | str]]:
        """
        Get a mapping containing all the diesel generator information.

        :return:
            The diesel generator information.

        """

        return {
            DIESEL_GENERATORS: [
                {
                    NAME: generator_name,
                    DIESEL_CONSUMPTION: self.fuel_consumption[generator_name].get(),
                    MINIMUM_LOAD: self.minimum_load[generator_name].get() / 100,
                    COSTS: {
                        COST: self.costs[generator_name].get(),
                        INSTALLATION_COST: self.installation_costs[
                            generator_name
                        ].get(),
                        INSTALLATION_COST_DECREASE: -(
                            self.installation_cost_decrease[generator_name].get()
                        ),
                        OM: self.o_and_m_costs[generator_name].get(),
                        COST_DECREASE: -(self.cost_decrease[generator_name].get()),
                    },
                    EMISSIONS: {
                        GHGS: self.embedded_emissions[generator_name].get(),
                        GHG_DECREASE: -(
                            self.annual_emissions_decrease[generator_name].get()
                        ),
                        INSTALLATION_GHGS: self.installation_emissions[
                            generator_name
                        ].get(),
                        INSTALLATION_GHGS_DECREASE: -(
                            self.installation_emissions_decrease[generator_name].get()
                        ),
                        OM_GHGS: self.om_emissions[generator_name].get(),
                    },
                }
                for generator_name in self.diesel_generator_name_values
            ]
        }

    def populate_available_generators(self) -> None:
        """Populate the combo box with the set of avialable batteries."""

        self.diesel_generator_selected_combobox["values"] = [
            entry.get() for entry in self.diesel_generator_name_values.values()
        ]

    def select_diesel_generator(self, _) -> None:
        # Determine the diesel_generator name pre- and post-selection
        previous_diesel_generator_name: str = {
            (entry == self.diesel_generator_selected): key
            for key, entry in self.diesel_generator_name_values.items()
        }[True]
        selected_diesel_generator_name: str = (
            self.diesel_generator_selected_combobox.get()
        )

        # Reset the value of the old variable
        self.diesel_generator_name_values[previous_diesel_generator_name].set(
            previous_diesel_generator_name
        )

        # Set the variable to be the new selected variable
        self.diesel_generator_selected = self.diesel_generator_name_values[
            selected_diesel_generator_name
        ]
        self.diesel_generator_selected_combobox.configure(
            textvariable=self.diesel_generator_selected
        )
        self.diesel_generator_name_entry.configure(
            textvariable=self.diesel_generator_selected
        )

        # Update the variables being displayed.
        self.update_diesel_generator_frame()

    def set_generators(
        self,
        diesel_generator_selected: DieselGenerator,
        diesel_generators: list[DieselGenerator],
        diesel_generator_costs: dict[str, dict[str, float]],
        diesel_generator_emissions: dict[str, dict[str, float]],
    ) -> None:
        """
        Sets the diesel generator information.

        :param: diesel_generator_selected
            The selected diesel generator for the run.

        :param: diesel_generators
            The `list` of :class:`clover.simulation.diesel.DieselGenerator` instances
            defined.

        :param: diesel_generator_costs
            The costs associated with the diesel generators.

        :param: diesel_generator_emissions
            The emissions associated with the diesel generators.

        """

        self.diesel_generator_name_values: dict[str, ttk.StringVar] = {}

        for diesel_generator in diesel_generators:
            self.diesel_generator_name_values[diesel_generator.name] = ttk.StringVar(
                self, diesel_generator.name
            )

            # Performance characteristics
            self.diesel_generator_capacities[diesel_generator.name] = ttk.DoubleVar(
                self, 1
            )
            self.fuel_consumption[diesel_generator.name] = ttk.DoubleVar(
                self, diesel_generator.diesel_consumption
            )
            self.minimum_load[diesel_generator.name] = ttk.DoubleVar(
                self, 100 * diesel_generator.minimum_load
            )

            # Costs
            self.costs[diesel_generator.name] = ttk.DoubleVar(
                self,
                (this_generator_costs := diesel_generator_costs[diesel_generator.name])[
                    COST
                ],
            )
            self.cost_decrease[diesel_generator.name] = ttk.DoubleVar(
                self, -(this_generator_costs.get(COST_DECREASE, 0))
            )
            self.installation_costs[diesel_generator.name] = ttk.DoubleVar(
                self, this_generator_costs.get(INSTALLATION_COST, 0)
            )
            self.installation_cost_decrease[diesel_generator.name] = ttk.DoubleVar(
                self, -(this_generator_costs.get(INSTALLATION_COST_DECREASE, 0))
            )
            self.o_and_m_costs[diesel_generator.name] = ttk.DoubleVar(
                self, this_generator_costs.get(OM, 0)
            )

            # Emissions
            self.embedded_emissions[diesel_generator.name] = ttk.DoubleVar(
                self,
                (
                    this_generator_emissions := diesel_generator_emissions[
                        diesel_generator.name
                    ]
                ).get(GHGS, 0),
            )
            self.annual_emissions_decrease[diesel_generator.name] = ttk.DoubleVar(
                self, -(this_generator_emissions.get(OM_GHGS, 0))
            )
            self.installation_emissions[diesel_generator.name] = ttk.DoubleVar(
                self, this_generator_emissions.get(INSTALLATION_GHGS, 0)
            )
            self.installation_emissions_decrease[diesel_generator.name] = ttk.DoubleVar(
                self, -(this_generator_emissions.get(INSTALLATION_GHGS_DECREASE, 0))
            )
            self.om_emissions[diesel_generator.name] = ttk.DoubleVar(
                self, this_generator_emissions.get(GHG_DECREASE, 0)
            )

        self.populate_available_generators()

        self.diesel_generator_selected = self.diesel_generator_name_values[
            diesel_generator_selected.name
        ]
        self.diesel_generator_selected_combobox.set(
            self.diesel_generator_selected.get()
        )
        self.select_diesel_generator(self.diesel_generator_selected.get())

    def update_diesel_generator_frame(self) -> None:
        """Updates the entries so that the correct variables are displayed on the screen."""

        # Update diesel generator capacity entry
        self.diesel_generator_capacity_entry.configure(
            textvariable=self.diesel_generator_capacities[
                self.diesel_generator_selected.get()
            ]
        )

        # Update fuel consumption entry
        self.fuel_consumption_entry.configure(
            textvariable=self.fuel_consumption[self.diesel_generator_selected.get()]
        )

        # Update minimum load entry and slider
        self.minimum_load_entry.configure(
            textvariable=self.minimum_load[self.diesel_generator_selected.get()]
        )
        self.minimum_load_slider.configure(
            variable=self.minimum_load[self.diesel_generator_selected.get()]
        )

        # Update cost entry
        self.cost_entry.configure(
            textvariable=self.costs[self.diesel_generator_selected.get()]
        )

        # Update cost decrease entry
        self.cost_decrease_entry.configure(
            textvariable=self.cost_decrease[self.diesel_generator_selected.get()]
        )

        # Update installation costs entry
        self.installation_cost_entry.configure(
            textvariable=self.installation_costs[self.diesel_generator_selected.get()]
        )

        # Update installation cost decrease entry
        self.installation_cost_decrease_entry.configure(
            textvariable=self.installation_cost_decrease[
                self.diesel_generator_selected.get()
            ]
        )

        # Update O&M costs entry
        self.o_and_m_costs_entry.configure(
            textvariable=self.o_and_m_costs[self.diesel_generator_selected.get()]
        )

        # Update embedded emissions entry
        self.embedded_emissions_entry.configure(
            textvariable=self.embedded_emissions[self.diesel_generator_selected.get()]
        )

        # Update annual emissions decrease entry
        self.annual_emissions_decrease_entry.configure(
            textvariable=self.annual_emissions_decrease[
                self.diesel_generator_selected.get()
            ]
        )

        # Update installation emissions entry
        self.installation_emissions_entry.configure(
            textvariable=self.installation_emissions[
                self.diesel_generator_selected.get()
            ]
        )

        # Update installation decrease emissions entry
        self.installation_emissions_decrease_entry.configure(
            textvariable=self.installation_emissions_decrease[
                self.diesel_generator_selected.get()
            ]
        )

        # Update O&M emissions entry
        self.om_emissions_entry.configure(
            textvariable=self.om_emissions[self.diesel_generator_selected.get()]
        )


class HeaterFrame(ttk.Frame):
    """
    Represents the diesel heater frame.

    Contains settings for the diesel heater units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Diesel heater frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class DieselFrame(ttk.Frame):
    """
    Represents the Diesel frame.

    Contains settings for diesel-powered units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=10, minsize=500)

        # Diesel Fuel Cost
        self.diesel_fuel_cost_label = ttk.Label(self, text="Fuel cost")
        self.diesel_fuel_cost_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.diesel_fuel_cost = ttk.DoubleVar(self, 0)

        self.diesel_fuel_cost_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.diesel_fuel_cost,
        )
        self.diesel_fuel_cost_entry.grid(
            row=0, column=1, padx=10, pady=5, ipadx=20, sticky="ew"
        )
        self.diesel_fuel_cost_units_label = ttk.Label(self, text="$/litre")
        self.diesel_fuel_cost_units_label.grid(
            row=0, column=2, padx=10, pady=5, sticky="w"
        )

        # Diesel Fuel Cost Decrease
        self.diesel_fuel_cost_decrease_label = ttk.Label(self, text="Fuel cost change")
        self.diesel_fuel_cost_decrease_label.grid(
            row=0, column=3, padx=10, pady=5, sticky="w"
        )
        self.diesel_fuel_cost_decrease = ttk.DoubleVar(self, 0)

        self.diesel_fuel_cost_decrease_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.diesel_fuel_cost_decrease,
        )
        self.diesel_fuel_cost_decrease_entry.grid(
            row=0, column=4, padx=10, pady=5, ipadx=20, sticky="ew"
        )
        self.diesel_fuel_cost_decrease_units_label = ttk.Label(self, text="% / year")
        self.diesel_fuel_cost_decrease_units_label.grid(
            row=0, column=5, padx=10, pady=5, sticky="w"
        )

        # Diesel Fuel Emissions
        self.diesel_fuel_emissions_label = ttk.Label(self, text="Fuel emissions")
        self.diesel_fuel_emissions_label.grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.diesel_fuel_emissions = ttk.DoubleVar(self, 0)

        self.diesel_fuel_emissions_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.diesel_fuel_emissions,
        )
        self.diesel_fuel_emissions_entry.grid(
            row=1, column=1, padx=10, pady=5, ipadx=20, sticky="ew"
        )
        self.diesel_fuel_emissions_units_label = ttk.Label(self, text="kgCO2eq/litre")
        self.diesel_fuel_emissions_units_label.grid(
            row=1, column=2, padx=10, pady=5, sticky="w"
        )

        # Diesel Fuel Emissions Decrease
        self.diesel_fuel_emissions_decrease_label = ttk.Label(
            self, text="Fuel emissions change"
        )
        self.diesel_fuel_emissions_decrease_label.grid(
            row=1, column=3, padx=10, pady=5, sticky="w"
        )
        self.diesel_fuel_emissions_decrease = ttk.DoubleVar(self, 0)

        self.diesel_fuel_emissions_decrease_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.diesel_fuel_emissions_decrease,
        )
        self.diesel_fuel_emissions_decrease_entry.grid(
            row=1, column=4, padx=10, pady=5, ipadx=20, sticky="ew"
        )
        self.diesel_fuel_emissions_decrease_units_label = ttk.Label(
            self, text="% / year"
        )
        self.diesel_fuel_emissions_decrease_units_label.grid(
            row=1, column=5, padx=10, pady=5, sticky="w"
        )

        self.diesel_notebook = ttk.Notebook(self, bootstyle=DANGER)
        self.diesel_notebook.grid(
            row=2, column=0, columnspan=6, padx=20, pady=10, sticky="news"
        )

        self.generator_frame = GeneratorFrame(self)
        self.diesel_notebook.add(self.generator_frame, text="Generators", sticky="news")

        self.heater_frame = HeaterFrame(self)
        # self.diesel_notebook.add(
        #     self.heater_frame,
        #     text="Space and water heaters",
        #     sticky="news",
        #     state=DISABLED,
        # )

        # TODO: Add configuration frame widgets and layout

    def set_fuel_impact(self, diesel_fuel_impact: dict[str, float]) -> None:
        """
        Set the diesel fuel impact.

        :param: diesel_fuel_impact
            The diesel fuel impact.

        """

        self.diesel_fuel_cost.set(diesel_fuel_impact.get(COST, 0))
        self.diesel_fuel_cost_decrease.set(-(diesel_fuel_impact.get(COST_DECREASE, 0)))

        self.diesel_fuel_emissions.set(diesel_fuel_impact.get(GHGS, 0))
        self.diesel_fuel_emissions_decrease.set(
            -(diesel_fuel_impact.get(GHG_DECREASE, 0))
        )

    def to_dict(self) -> dict[str, dict[str, dict[str, float] | float | str]]:
        """
        Return the information from the frame as a dictionary.

        :return:
            The information from the frame.

        """

        output_dict = {
            ImpactingComponent.DIESEL_FUEL.value: {
                COST: self.diesel_fuel_cost.get(),
                COST_DECREASE: -(self.diesel_fuel_cost_decrease.get()),
                GHGS: self.diesel_fuel_emissions.get(),
                GHG_DECREASE: -(self.diesel_fuel_emissions_decrease.get()),
            }
        }
        output_dict.update(self.generator_frame.get_generators())

        return output_dict
