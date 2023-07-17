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

import ttkbootstrap as ttk

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

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
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
        self.rowconfigure(13, weight=1)
        self.rowconfigure(14, weight=1)
        self.rowconfigure(15, weight=1)
        self.rowconfigure(16, weight=1)

        self.columnconfigure(0, weight=10)  # First row has the header
        self.columnconfigure(1, weight=10)  # These rows have entries
        self.columnconfigure(2, weight=1)  # These rows have entries
        self.columnconfigure(3, weight=1)  # These rows have entries

        # Diesel generator being selected
        self.diesel_generator_selected_label = ttk.Label(
            self, text="Diesel generator to model"
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
            self, bootstyle=DANGER, textvariable=self.diesel_generator_selected
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
            self,
            bootstyle=f"{DANGER}-{OUTLINE}",
            command=self.add_diesel_generator,
            text="New generator",
        )
        self.new_generator_button.grid(row=0, column=2, padx=10, pady=5, ipadx=80)

        # Diesel generator name
        self.diesel_generator_name_label = ttk.Label(self, text="Diesel generator name")
        self.diesel_generator_name_label.grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )

        self.diesel_generator_name_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.diesel_generator_selected
        )
        self.diesel_generator_name_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )
        self.diesel_generator_name_entry.bind(
            "<Return>", self.enter_diesel_generator_name
        )

        # Diesel generator capacity
        self.diesel_generator_capacity_label = ttk.Label(self, text="Capacity")
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
            self,
            bootstyle=DANGER,
            textvariable=self.diesel_generator_capacities[
                self.diesel_generator_selected.get()
            ],
        )
        self.diesel_generator_capacity_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.diesel_generator_capacity_unit = ttk.Label(self, text="kW")
        self.diesel_generator_capacity_unit.grid(
            row=2, column=2, padx=10, pady=5, sticky="w"
        )

        # Fuel consumption
        self.fuel_consumption_label = ttk.Label(self, text="Fuel consumption")
        self.fuel_consumption_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.fuel_consumption: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0.4, f"{diesel_generator_name}_fuel_consumption"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }

        self.fuel_consumption_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.fuel_consumption[self.diesel_generator_selected.get()],
        )
        self.fuel_consumption_entry.grid(
            row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew"
        )

        self.fuel_consumption_unit = ttk.Label(self, text=f"litres / kW-hour")
        self.fuel_consumption_unit.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        # Minimum load
        self.minimum_load_label = ttk.Label(self, text="Minimum capacity factor")
        self.minimum_load_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.minimum_load: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 20, f"{diesel_generator_name}_minimum_load"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }

        def scalar_minimum_load(_):
            self.minimum_load_entry.update()

        self.minimum_load_slider = ttk.Scale(
            self,
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
            self.minimum_load_entry.set(min(max(self.minimum_load_entry.get(), 0), 100))
            self.minimum_load[self.diesel_generator_selected.get()].set(
                self.minimum_load_entry.get()
            )
            self.minimum_load_slider.set(
                self.minimum_load[self.diesel_generator_selected.get()].get()
            )

        self.minimum_load_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.minimum_load[self.diesel_generator_selected.get()],
        )
        self.minimum_load_entry.grid(row=4, column=2, padx=10, pady=5, sticky="ew")
        self.minimum_load_entry.bind("<Return>", enter_minimum_load)

        self.minimum_load_unit = ttk.Label(self, text=f"% of capacity")
        self.minimum_load_unit.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        # Cost
        self.cost_label = ttk.Label(self, text="Cost")
        self.cost_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.costs: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_cost"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.cost_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.costs[self.diesel_generator_selected.get()],
        )
        self.cost_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew", ipadx=80)

        self.cost_unit = ttk.Label(self, text="USD ($)")
        self.cost_unit.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # Cost decrease
        self.cost_decrease_label = ttk.Label(self, text="Cost decrease")
        self.cost_decrease_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")

        self.cost_decrease: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_cost_decrease"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.cost_decrease_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.cost_decrease[self.diesel_generator_selected.get()],
        )
        self.cost_decrease_entry.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.cost_decrease_unit = ttk.Label(self, text="% decrease / year")
        self.cost_decrease_unit.grid(row=6, column=2, padx=10, pady=5, sticky="w")

        # OPEX costs
        self.opex_costs_label = ttk.Label(self, text="OPEX (O&M) costs")
        self.opex_costs_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

        self.o_and_m_costs: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_o_and_m_costs"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.o_and_m_costs_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.o_and_m_costs[self.diesel_generator_selected.get()],
        )
        self.o_and_m_costs_entry.grid(
            row=7, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.o_and_m_costs_unit = ttk.Label(self, text="USD ($)")
        self.o_and_m_costs_unit.grid(row=7, column=2, padx=10, pady=5, sticky="w")

        # Embedded emissions
        self.embedded_emissions_label = ttk.Label(self, text="Embedded emissions")
        self.embedded_emissions_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.embedded_emissions: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_ghgs"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.embedded_emissions_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.embedded_emissions[self.diesel_generator_selected.get()],
        )

        self.embedded_emissions_unit = ttk.Label(self, text="kgCO2eq / unit")
        self.embedded_emissions_unit.grid(row=8, column=2, padx=10, pady=5, sticky="w")

        # O&M emissions
        self.om_emissions_label = ttk.Label(self, text="O&M emissions")
        self.om_emissions_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        self.om_emissions: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_o_and_m_ghgs"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.om_emissions_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.om_emissions[self.diesel_generator_selected.get()],
        )
        self.om_emissions_entry.grid(
            row=9, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.om_emissions_unit = ttk.Label(self, text="kgCO2eq / year")
        self.om_emissions_unit.grid(row=9, column=2, padx=10, pady=5, sticky="w")

        # Annual emissions decrease
        self.annual_emissions_decrease_label = ttk.Label(
            self, text="Annual emissions decrease"
        )
        self.annual_emissions_decrease_label.grid(
            row=10, column=0, padx=10, pady=5, sticky="w"
        )

        self.annual_emissions_decrease: dict[str, ttk.DoubleVar] = {
            diesel_generator_name: ttk.DoubleVar(
                self, 0, f"{diesel_generator_name}_ghgs_decrease"
            )
            for diesel_generator_name in self.diesel_generator_name_values
        }
        self.annual_emissions_decrease_entry = ttk.Entry(
            self,
            bootstyle=DANGER,
            textvariable=self.annual_emissions_decrease[
                self.diesel_generator_selected.get()
            ],
        )
        self.annual_emissions_decrease_entry.grid(
            row=10, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.annual_emissions_decrease_unit = ttk.Label(self, text="% / year")
        self.annual_emissions_decrease_unit.grid(
            row=10, column=2, padx=10, pady=5, sticky="w"
        )

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
        self.o_and_m_costs[new_name] = ttk.DoubleVar(self, 0)
        self.embedded_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.om_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.annual_emissions_decrease[new_name] = ttk.DoubleVar(self, 0)

        # Select the new battery and update the screen
        self.diesel_generator_selected = self.diesel_generator_name_values[new_name]
        self.diesel_generator_selected_combobox.configure(
            textvariable=self.diesel_generator_selected
        )
        self.diesel_generator_name_entry.configure(
            textvariable=self.diesel_generator_selected
        )
        self.update_diesel_generator_frame()

    def enter_diesel_generator_name(self, _) -> None:
        """Called when someone enters a new diesel_generator name."""
        self.populate_available_generators()

        # Update all the mappings stored
        self.diesel_generator_capacities = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.diesel_generator_capacities.items()
        }
        self.fuel_consumption = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.fuel_consumption.items()
        }
        self.minimum_load = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.minimum_load.items()
        }
        self.costs = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.costs.items()
        }
        self.cost_decrease = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.cost_decrease.items()
        }
        self.o_and_m_costs = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.o_and_m_costs.items()
        }
        self.embedded_emissions = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.embedded_emissions.items()
        }
        self.om_emissions = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.om_emissions.items()
        }
        self.annual_emissions_decrease = {
            self.diesel_generator_name_values[key].get(): value
            for key, value in self.annual_emissions_decrease.items()
        }

        # Update the diesel generator values.
        self.diesel_generator_name_values = {
            entry.get(): entry for entry in self.diesel_generator_name_values.values()
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

        # Update O&M costs entry
        self.o_and_m_costs_entry.configure(
            textvariable=self.o_and_m_costs[self.diesel_generator_selected.get()]
        )

        # Update embedded emissions entry
        self.embedded_emissions_entry.configure(
            textvariable=self.embedded_emissions[self.diesel_generator_selected.get()]
        )

        # Update O&M emissions entry
        self.om_emissions_entry.configure(
            textvariable=self.om_emissions[self.diesel_generator_selected.get()]
        )

        # Update annual emissions decrease entry
        self.annual_emissions_decrease_entry.configure(
            textvariable=self.annual_emissions_decrease[
                self.diesel_generator_selected.get()
            ]
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
        self.rowconfigure(0, weight=1)

        self.diesel_notebook = ttk.Notebook(self, bootstyle=DANGER)
        self.diesel_notebook.grid(row=0, column=0, padx=20, pady=10, sticky="news")

        self.generator_frame = GeneratorFrame(self)
        self.diesel_notebook.add(self.generator_frame, text="Generators", sticky="news")

        self.heater_frame = HeaterFrame(self)
        self.diesel_notebook.add(
            self.heater_frame,
            text="Space and water heaters",
            sticky="news",
            state=DISABLED,
        )

        # TODO: Add configuration frame widgets and layout
