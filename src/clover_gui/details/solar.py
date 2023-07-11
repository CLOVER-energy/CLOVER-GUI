#!/usr/bin/python3.10
########################################################################################
# solar.py - The solar module for CLOVER-GUI application.                              #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 27/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import tkinter as tk

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


__all__ = ("SolarFrame",)


class SolarFrame(ttk.Frame):
    """
    Represents the Solar frame.

    Contains settings for solar collectors.

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

        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=10)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        self.renewables_ninja_token = tk.StringVar(value="YOUR API TOKEN")
        self.renewables_ninja_token_entry = ttk.Entry(
            self,
            bootstyle=f"{WARNING}-inverted",
            state=DISABLED,
            textvariable=self.renewables_ninja_token,
        )
        self.renewables_ninja_token_entry.grid(
            row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew", ipadx=80
        )

        # Panel selected
        self.panel_selected = tk.StringVar(value="m-Si")
        self.panel_name_values = {
            "m-Si": self.panel_selected,
            (panel_name := "p-Si"): ttk.StringVar(self, panel_name),
            (panel_name := "CdTe"): ttk.StringVar(self, panel_name),
        }

        self.pv_panel_label = ttk.Label(self, text="Panel to configure")
        self.pv_panel_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.pv_panel_combobox = ttk.Combobox(
            self, bootstyle=WARNING, textvariable=self.panel_selected
        )
        self.pv_panel_combobox.grid(
            row=1, column=1, padx=10, pady=5, sticky="w", ipadx=60
        )
        self.pv_panel_combobox.bind("<<ComboboxSelected>>", self.select_pv_panel)
        self.populate_available_panels()

        # New panel
        self.new_panel_button = ttk.Button(
            self,
            bootstyle=f"{WARNING}-{OUTLINE}",
            command=self.add_panel,
            text="New collector",
        )
        self.new_panel_button.grid(row=1, column=2, padx=10, pady=5, ipadx=80)

        # Panel name
        self.panel_name_label = ttk.Label(self, text="Panel name")
        self.panel_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.panel_name_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.panel_selected
        )
        self.panel_name_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )
        self.panel_name_entry.bind("<Return>", self.enter_panel_name)

        # Lifetime
        self.lifetime_label = ttk.Label(self, text="Lifetime")
        self.lifetime_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.panel_lifetimes: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 20, f"{panel_name}_lifetime")
            for panel_name in self.panel_name_values
        }

        def scalar_lifetime(_):
            self.panel_lifetimes[self.panel_selected.get()].set(
                int(self.lifetime_slider.get())
            )
            self.lifetime_entry.update()

        self.lifetime_slider = ttk.Scale(
            self,
            from_=0,
            to=30,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_lifetime,
            bootstyle=WARNING,
            variable=self.panel_lifetimes[self.panel_selected.get()],
        )
        self.lifetime_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        def enter_lifetime(_):
            self.panel_lifetimes[self.panel_selected.get()].set(
                int(self.lifetime_entry.get())
            )
            self.lifetime_slider.set(
                self.panel_lifetimes[self.panel_selected.get()].get()
            )

        self.lifetime_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.panel_lifetimes[self.panel_selected.get()],
        )
        self.lifetime_entry.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
        self.lifetime_entry.bind("<Return>", enter_lifetime)

        self.lifetime_unit = ttk.Label(self, text="years")
        self.lifetime_unit.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        # Tilt
        self.tilt_label = ttk.Label(self, text="Tilt")
        self.tilt_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.panel_tilt: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 22, f"{panel_name}_tilt")
            for panel_name in self.panel_name_values
        }

        def scalar_tilt(_):
            self.panel_tilt[self.panel_selected.get()].set(self.tilt_slider.get())
            self.tilt_entry.update()

        self.tilt_slider = ttk.Scale(
            self,
            from_=0,
            to=90,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_tilt,
            bootstyle=WARNING,
            variable=self.panel_tilt[self.panel_selected.get()],
        )
        self.tilt_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        def enter_tilt(_):
            self.panel_tilt[self.panel_selected.get()].set(self.tilt_entry.get())
            self.tilt_slider.set(self.panel_tilt[self.panel_selected.get()].get())

        self.tilt_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.panel_tilt[self.panel_selected.get()],
        )
        self.tilt_entry.grid(row=4, column=2, padx=10, pady=5, sticky="ew")
        self.tilt_entry.bind("<Return>", enter_tilt)

        self.tilt_unit = ttk.Label(self, text="degrees")
        self.tilt_unit.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        # Azimuthal orientation
        self.azimuthal_orientation_label = ttk.Label(self, text="Azimuthal orientation")
        self.azimuthal_orientation_label.grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )

        self.panel_orientation: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 180, f"{panel_name}_azimuthal_orientation")
            for panel_name in self.panel_name_values
        }

        def scalar_azimuthal_orientation(_):
            self.panel_orientation[self.panel_selected.get()].set(
                self.azimuthal_orientation_slider.get()
            )
            self.azimuthal_orientation_entry.update()

        self.azimuthal_orientation_slider = ttk.Scale(
            self,
            from_=0,
            to=360,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_azimuthal_orientation,
            bootstyle=WARNING,
            variable=self.panel_orientation[self.panel_selected.get()],
        )
        self.azimuthal_orientation_slider.grid(
            row=5, column=1, padx=10, pady=5, sticky="ew"
        )

        def enter_azimuthal_orientation(_):
            self.panel_orientation[self.panel_selected.get()].set(
                self.azimuthal_orientation_entry.get()
            )
            self.azimuthal_orientation_slider.set(
                self.panel_orientation[self.panel_selected.get()].get()
            )

        self.azimuthal_orientation_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.panel_orientation[self.panel_selected.get()],
        )
        self.azimuthal_orientation_entry.grid(
            row=5, column=2, padx=10, pady=5, sticky="ew"
        )
        self.azimuthal_orientation_entry.bind("<Return>", enter_azimuthal_orientation)

        self.azimuthal_orientation_unit = ttk.Label(self, text="degrees")
        self.azimuthal_orientation_unit.grid(
            row=5, column=3, padx=10, pady=5, sticky="ew"
        )

        # Reference efficiency
        self.reference_efficiency_label = ttk.Label(self, text="Reference efficiency")
        self.reference_efficiency_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        self.reference_efficiencies: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 15, f"{panel_name}_reference_efficiency")
            for panel_name in self.panel_name_values
        }

        def scalar_reference_efficiency(_):
            self.reference_efficiencies[self.panel_selected.get()].set(
                self.reference_efficiency_slider.get()
            )
            self.reference_efficiency_entry.update()

        self.reference_efficiency_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_reference_efficiency,
            bootstyle=f"{WARNING}-inverted",
            state=DISABLED,
            variable=self.reference_efficiencies[self.panel_selected.get()],
        )
        self.reference_efficiency_slider.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew"
        )

        def enter_reference_efficiency(_):
            self.reference_efficiencies[self.panel_selected.get()].set(
                self.reference_efficiency_entry.get()
            )
            self.reference_efficiency_slider.set(
                self.reference_efficiencies[self.panel_selected.get()].get()
            )

        self.reference_efficiency_entry = ttk.Entry(
            self,
            bootstyle=f"{WARNING}-inverted",
            state=DISABLED,
            textvariable=self.reference_efficiencies[self.panel_selected.get()],
        )
        self.reference_efficiency_entry.grid(
            row=6, column=2, padx=10, pady=5, sticky="ew"
        )
        self.reference_efficiency_entry.bind("<Return>", enter_reference_efficiency)

        self.reference_efficiency_unit = ttk.Label(self, text=f"%")
        self.reference_efficiency_unit.grid(
            row=6, column=3, padx=10, pady=5, sticky="ew"
        )

        # Reference temperature
        self.reference_temperature_label = ttk.Label(self, text="Reference temperature")
        self.reference_temperature_label.grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )

        self.reference_temperature: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 25, f"{panel_name}_reference_temperature")
            for panel_name in self.panel_name_values
        }
        self.reference_temperature_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.reference_temperature[self.panel_selected.get()],
            state=DISABLED,
        )
        self.reference_temperature_entry.grid(
            row=7, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.reference_temperature_unit = ttk.Label(self, text="degrees Celsius")
        self.reference_temperature_unit.grid(
            row=7, column=2, padx=10, pady=5, sticky="w"
        )

        # Thermal coefficient
        self.thermal_coefficient_label = ttk.Label(self, text="Thermal coefficient")
        self.thermal_coefficient_label.grid(
            row=8, column=0, padx=10, pady=5, sticky="w"
        )

        self.thermal_coefficient: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0.56, f"{panel_name}_thermal_coefficient")
            for panel_name in self.panel_name_values
        }
        self.thermal_coefficient_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.thermal_coefficient[self.panel_selected.get()],
            state=DISABLED,
        )
        self.thermal_coefficient_entry.grid(
            row=8, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.thermal_coefficient_unit = ttk.Label(self, text="% / degree Celsius")
        self.thermal_coefficient_unit.grid(row=8, column=2, padx=10, pady=5, sticky="w")

        # Cost
        self.cost_label = ttk.Label(self, text="Cost")
        self.cost_label.grid(row=9, column=0, padx=10, pady=5, sticky="w")

        self.costs: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_cost")
            for panel_name in self.panel_name_values
        }
        self.cost_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.costs[self.panel_selected.get()],
        )
        self.cost_entry.grid(row=9, column=1, padx=10, pady=5, sticky="ew", ipadx=80)

        self.cost_unit = ttk.Label(self, text="USD ($)")
        self.cost_unit.grid(row=9, column=2, padx=10, pady=5, sticky="w")

        # Cost decrease
        self.cost_decrease_label = ttk.Label(self, text="Cost decrease")
        self.cost_decrease_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")

        self.cost_decrease: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_cost_decrease")
            for panel_name in self.panel_name_values
        }
        self.cost_decrease_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.cost_decrease[self.panel_selected.get()],
        )
        self.cost_decrease_entry.grid(
            row=10, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.cost_decrease_unit = ttk.Label(self, text="% decrease / year")
        self.cost_decrease_unit.grid(row=10, column=2, padx=10, pady=5, sticky="w")

        # OPEX costs
        self.opex_costs_label = ttk.Label(self, text="OPEX (O&M) costs")
        self.opex_costs_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")

        self.o_and_m_costs: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_o_and_m_costs")
            for panel_name in self.panel_name_values
        }
        self.o_and_m_costs_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.o_and_m_costs[self.panel_selected.get()],
        )
        self.o_and_m_costs_entry.grid(
            row=11, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.o_and_m_costs_unit = ttk.Label(self, text="USD ($)")
        self.o_and_m_costs_unit.grid(row=11, column=2, padx=10, pady=5, sticky="w")

        # Embedded emissions
        self.embedded_emissions_label = ttk.Label(self, text="Embedded emissions")
        self.embedded_emissions_label.grid(
            row=12, column=0, padx=10, pady=5, sticky="w"
        )

        self.embedded_emissions: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_ghgs")
            for panel_name in self.panel_name_values
        }
        self.embedded_emissions_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.embedded_emissions[self.panel_selected.get()],
        )
        self.embedded_emissions_entry.grid(
            row=12, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.embedded_emissions_unit = ttk.Label(self, text="kgCO2eq / unit")
        self.embedded_emissions_unit.grid(row=12, column=2, padx=10, pady=5, sticky="w")

        # O&M emissions
        self.om_emissions_label = ttk.Label(self, text="O&M emissions")
        self.om_emissions_label.grid(row=13, column=0, padx=10, pady=5, sticky="w")

        self.om_emissions: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_o_and_m_ghgs")
            for panel_name in self.panel_name_values
        }
        self.om_emissions_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.om_emissions[self.panel_selected.get()],
        )
        self.om_emissions_entry.grid(
            row=13, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.om_emissions_unit = ttk.Label(self, text="kgCO2eq / year")
        self.om_emissions_unit.grid(row=13, column=2, padx=10, pady=5, sticky="w")

        # Annual emissions decrease
        self.annual_emissions_decrease_label = ttk.Label(
            self, text="Annual emissions decrease"
        )
        self.annual_emissions_decrease_label.grid(
            row=14, column=0, padx=10, pady=5, sticky="w"
        )

        self.annual_emissions_decrease: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_ghgs_decrease")
            for panel_name in self.panel_name_values
        }
        self.annual_emissions_decrease_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.annual_emissions_decrease[self.panel_selected.get()],
        )
        self.annual_emissions_decrease_entry.grid(
            row=14, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.annual_emissions_decrease_unit = ttk.Label(self, text="% / year")
        self.annual_emissions_decrease_unit.grid(
            row=14, column=2, padx=10, pady=5, sticky="w"
        )

    def add_panel(self) -> None:
        """Called when a user presses the new-panel button."""

        # Determine the new name
        new_name = "New panel {suffix}"
        index = 0
        suffix = ""
        while new_name.format(suffix=suffix) in self.panel_name_values:
            index += 1
            suffix = f"({index})"

        new_name = new_name.format(suffix=suffix)

        self.panel_name_values[new_name] = ttk.StringVar(self, new_name)
        self.populate_available_panels()

        # Update all the mappings stored
        self.panel_lifetimes[new_name] = ttk.DoubleVar(self, 15)
        self.panel_tilt[new_name] = ttk.DoubleVar(self, 0)
        self.panel_orientation[new_name] = ttk.DoubleVar(self, 180)
        self.reference_efficiencies[new_name] = ttk.DoubleVar(self, 0.015)
        self.reference_temperature[new_name] = ttk.DoubleVar(self, 25)
        self.thermal_coefficient[new_name] = ttk.DoubleVar(self, 0.56)
        self.costs[new_name] = ttk.DoubleVar(self, 0)
        self.cost_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.o_and_m_costs[new_name] = ttk.DoubleVar(self, 0)
        self.embedded_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.om_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.annual_emissions_decrease[new_name] = ttk.DoubleVar(self, 0)

        # Select the new panel and update the screen
        self.panel_selected = self.panel_name_values[new_name]
        self.pv_panel_combobox.configure(textvariable=self.panel_selected)
        self.panel_name_entry.configure(textvariable=self.panel_selected)
        self.update_panel_frame()

    def enter_panel_name(self, _) -> None:
        """Called when someone enters a new panel name."""

        self.populate_available_panels()

        # Update all the mappings stored
        self.panel_lifetimes = {
            self.panel_name_values[key].get(): value
            for key, value in self.panel_lifetimes.items()
        }
        self.panel_tilt = {
            self.panel_name_values[key].get(): value
            for key, value in self.panel_tilt.items()
        }
        self.panel_orientation = {
            self.panel_name_values[key].get(): value
            for key, value in self.panel_orientation.items()
        }
        self.reference_efficiencies = {
            self.panel_name_values[key].get(): value
            for key, value in self.reference_efficiencies.items()
        }
        self.reference_temperature = {
            self.panel_name_values[key].get(): value
            for key, value in self.reference_temperature.items()
        }
        self.thermal_coefficient = {
            self.panel_name_values[key].get(): value
            for key, value in self.thermal_coefficient.items()
        }
        self.costs = {
            self.panel_name_values[key].get(): value
            for key, value in self.costs.items()
        }
        self.cost_decrease = {
            self.panel_name_values[key].get(): value
            for key, value in self.cost_decrease.items()
        }
        self.o_and_m_costs = {
            self.panel_name_values[key].get(): value
            for key, value in self.o_and_m_costs.items()
        }
        self.embedded_emissions = {
            self.panel_name_values[key].get(): value
            for key, value in self.embedded_emissions.items()
        }
        self.om_emissions = {
            self.panel_name_values[key].get(): value
            for key, value in self.om_emissions.items()
        }
        self.annual_emissions_decrease = {
            self.panel_name_values[key].get(): value
            for key, value in self.annual_emissions_decrease.items()
        }

        # Update the panel-name values.
        self.panel_name_values = {
            entry.get(): entry for entry in self.panel_name_values.values()
        }

    def populate_available_panels(self) -> None:
        """Populate the combo box with the set of avialable panels."""

        self.pv_panel_combobox["values"] = [
            entry.get() for entry in self.panel_name_values.values()
        ]

    def select_pv_panel(self, _) -> None:
        """Select the PV panel."""

        # Determine the panel name pre- and post-selection
        previous_panel_name: str = {
            (entry == self.panel_selected): key
            for key, entry in self.panel_name_values.items()
        }[True]
        selected_panel_name: str = self.pv_panel_combobox.get()

        # Reset the value of the old variable
        self.panel_name_values[previous_panel_name].set(previous_panel_name)

        # Set the variable to be the new selected variable
        self.panel_selected = self.panel_name_values[selected_panel_name]
        self.pv_panel_combobox.configure(textvariable=self.panel_selected)
        self.panel_name_entry.configure(textvariable=self.panel_selected)

        # Update the variables being displayed.
        self.update_panel_frame()

    def update_panel_frame(self) -> None:
        """
        Updates the entries so that the correct variables are displayed on the screen.

        """

        self.lifetime_entry.configure(
            textvariable=self.panel_lifetimes[self.panel_selected.get()]
        )
        self.lifetime_slider.configure(
            variable=self.panel_lifetimes[self.panel_selected.get()]
        )
        self.tilt_entry.configure(
            textvariable=self.panel_tilt[self.panel_selected.get()]
        )
        self.tilt_slider.configure(variable=self.panel_tilt[self.panel_selected.get()])
        self.azimuthal_orientation_entry.configure(
            textvariable=self.panel_orientation[self.panel_selected.get()]
        )
        self.azimuthal_orientation_slider.configure(
            variable=self.panel_orientation[self.panel_selected.get()]
        )
        self.reference_efficiency_entry.configure(
            textvariable=self.reference_efficiencies[self.panel_selected.get()]
        )
        self.reference_efficiency_slider.configure(
            variable=self.reference_efficiencies[self.panel_selected.get()]
        )
        self.reference_temperature_entry.configure(
            textvariable=self.reference_temperature[self.panel_selected.get()]
        )
        self.thermal_coefficient_entry.configure(
            textvariable=self.thermal_coefficient[self.panel_selected.get()]
        )
        self.cost_entry.configure(textvariable=self.costs[self.panel_selected.get()])
        self.cost_decrease_entry.configure(
            textvariable=self.cost_decrease[self.panel_selected.get()]
        )
        self.o_and_m_costs_entry.configure(
            textvariable=self.o_and_m_costs[self.panel_selected.get()]
        )
        self.embedded_emissions_entry.configure(
            textvariable=self.embedded_emissions[self.panel_selected.get()]
        )
        self.om_emissions_entry.configure(
            textvariable=self.om_emissions[self.panel_selected.get()]
        )
        self.annual_emissions_decrease_entry.configure(
            textvariable=self.annual_emissions_decrease[self.panel_selected.get()]
        )

        # Update the entries
        self.lifetime_entry.update()
        self.lifetime_slider.update()
        self.tilt_entry.update()
        self.tilt_slider.update()
        self.azimuthal_orientation_entry.update()
        self.azimuthal_orientation_slider.update()
        self.reference_efficiency_entry.update()
        self.reference_efficiency_slider.update()
        self.reference_temperature_entry.update()
        self.thermal_coefficient_entry.update()
        self.cost_entry.update()
        self.cost_decrease_entry.update()
        self.o_and_m_costs_entry.update()
        self.embedded_emissions_entry.update()
        self.annual_emissions_decrease_entry.update()
        self.om_emissions_entry.update()
