#!/usr/bin/python3.10
########################################################################################
# storage.py - The storage module for CLOVER-GUI application.                          #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################


import tkinter as tk

from typing import Callable

import ttkbootstrap as ttk

from clover.impact.finance import COST, COST_DECREASE, OM
from clover.impact.ghgs import GHGS, GHG_DECREASE, OM_GHGS
from clover.simulation.storage_utils import Battery
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from ..__utils__ import COSTS, EMISSIONS

__all__ = ("StorageFrame",)


class BatteryFrame(ttk.Frame):
    """
    Represents the Battery frame.

    Contains settings for the battery units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scrollable_frame = ScrolledFrame(self)
        self.scrollable_frame.grid(row=0, column=0, padx=10, pady=5, sticky="news")

        self.scrollable_frame.rowconfigure(0, weight=1)
        self.scrollable_frame.rowconfigure(1, weight=1)
        self.scrollable_frame.rowconfigure(2, weight=1)
        self.scrollable_frame.rowconfigure(3, weight=1)
        self.scrollable_frame.rowconfigure(4, weight=1)
        self.scrollable_frame.rowconfigure(5, weight=1)
        self.scrollable_frame.rowconfigure(6, weight=1)
        self.scrollable_frame.rowconfigure(7, weight=1)
        self.scrollable_frame.rowconfigure(8, weight=1)
        self.scrollable_frame.rowconfigure(9, weight=1)
        self.scrollable_frame.rowconfigure(10, weight=1)
        self.scrollable_frame.rowconfigure(11, weight=1)
        self.scrollable_frame.rowconfigure(12, weight=1)
        self.scrollable_frame.rowconfigure(13, weight=1)
        self.scrollable_frame.rowconfigure(14, weight=1)
        self.scrollable_frame.rowconfigure(15, weight=1)
        self.scrollable_frame.rowconfigure(16, weight=1)

        self.scrollable_frame.columnconfigure(0, weight=10)
        self.scrollable_frame.columnconfigure(1, weight=10)
        self.scrollable_frame.columnconfigure(2, weight=1)
        self.scrollable_frame.columnconfigure(3, weight=1)

        self.add_battery_to_scenario_frame: Callable | None = None
        self.set_batteries_on_system_frame: Callable | None = None

        # Battery being selected
        self.battery_selected_label = ttk.Label(
            self.scrollable_frame, text="Battery to configure"
        )
        self.battery_selected_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.battery_selected = ttk.StringVar(self, "Li-Ion", "battery_selected")
        self.battery_name_values = {
            "Li-Ion": self.battery_selected,
            (battery_name := "Pb-Acid"): ttk.StringVar(self, battery_name),
            (battery_name := "New Pb-Acid"): ttk.StringVar(self, battery_name),
        }

        self.battery_selected_combobox = ttk.Combobox(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.battery_selected,
            state=READONLY,
        )
        self.battery_selected_combobox.grid(
            row=0, column=1, padx=10, pady=5, sticky="w", ipadx=60
        )
        self.battery_selected_combobox.bind("<<ComboboxSelected>>", self.select_battery)
        self.populate_available_batteries()

        # New battery
        self.new_battery_button = ttk.Button(
            self.scrollable_frame,
            bootstyle=f"{WARNING}-{OUTLINE}",
            command=self.add_battery,
            text="New battery",
        )
        self.new_battery_button.grid(row=0, column=2, padx=10, pady=5, ipadx=80)

        # Battery name
        self.battery_name_label = ttk.Label(self.scrollable_frame, text="Battery name")
        self.battery_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.battery_name_entry = ttk.Entry(
            self.scrollable_frame, bootstyle=WARNING, textvariable=self.battery_selected
        )
        self.battery_name_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )
        self.battery_name_entry.bind("<Return>", self.enter_battery_name)

        # Save battery name button
        self.save_battery_name_button = ttk.Button(
            self.scrollable_frame,
            bootstyle=f"{WARNING}-{TOOLBUTTON}",
            text="Save",
            command=self.enter_battery_name,
        )
        self.save_battery_name_button.grid(
            row=1, column=2, padx=10, pady=5, sticky="w", ipadx=20
        )

        # Battery capacity
        self.battery_capacity_label = ttk.Label(self.scrollable_frame, text="Capacity")
        self.battery_capacity_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.battery_capacities: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 1, f"{battery_name}_battery_capacity")
            for battery_name in self.battery_name_values
        }

        self.battery_capacity_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.battery_capacities[self.battery_selected.get()],
        )
        self.battery_capacity_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.battery_capacity_unit = ttk.Label(self.scrollable_frame, text="kWh")
        self.battery_capacity_unit.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # Maximum charge
        self.maximum_charge_label = ttk.Label(
            self.scrollable_frame, text="Maximum state of charge"
        )
        self.maximum_charge_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.maximum_charge: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 90, f"{battery_name}_maximum_charge")
            for battery_name in self.battery_name_values
        }

        def scalar_maximum_charge(_):
            self.minimum_charge[self.battery_selected.get()].set(
                round(
                    min(
                        self.maximum_charge[self.battery_selected.get()].get(),
                        self.minimum_charge[self.battery_selected.get()].get(),
                    ),
                    1,
                )
            )
            self.minimum_charge_entry.update()

            self.maximum_charge[self.battery_selected.get()].set(
                round(self.maximum_charge[self.battery_selected.get()].get(), 1)
            )
            self.maximum_charge_entry.update()

        self.maximum_charge_slider = ttk.Scale(
            self.scrollable_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_maximum_charge,
            bootstyle=WARNING,
            variable=self.maximum_charge[self.battery_selected.get()],
            # state=DISABLED
        )
        self.maximum_charge_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        def enter_maximum_charge(_):
            self.minimum_charge[self.battery_selected.get()].set(
                round(
                    min(
                        self.maximum_charge[self.battery_selected.get()].get(),
                        self.minimum_charge[self.battery_selected.get()].get(),
                    ),
                    2,
                )
            )
            self.minimum_charge_slider.set(
                self.minimum_charge[self.battery_selected.get()].get()
            )
            self.maximum_charge[self.battery_selected.get()].set(
                round(self.maximum_charge_entry.get(), 2)
            )
            self.maximum_charge_slider.set(
                round(self.maximum_charge[self.battery_selected.get()].get(), 2)
            )

        self.maximum_charge_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.maximum_charge[self.battery_selected.get()],
        )
        self.maximum_charge_entry.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
        self.maximum_charge_entry.bind("<Return>", enter_maximum_charge)

        self.maximum_charge_unit = ttk.Label(self.scrollable_frame, text=f"%")
        self.maximum_charge_unit.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        # Minimum charge
        self.minimum_charge_label = ttk.Label(
            self.scrollable_frame, text="Minimum state of charge"
        )
        self.minimum_charge_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.minimum_charge: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 20, f"{battery_name}_minimum_charge")
            for battery_name in self.battery_name_values
        }

        def scalar_minimum_charge(_):
            self.maximum_charge[self.battery_selected.get()].set(
                round(
                    max(
                        self.maximum_charge[self.battery_selected.get()].get(),
                        self.minimum_charge[self.battery_selected.get()].get(),
                    ),
                    1,
                )
            )
            self.maximum_charge_entry.update()

            self.minimum_charge[self.battery_selected.get()].set(
                round(self.minimum_charge[self.battery_selected.get()].get(), 1)
            )
            self.minimum_charge_entry.update()

        self.minimum_charge_slider = ttk.Scale(
            self.scrollable_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_minimum_charge,
            bootstyle=WARNING,
            variable=self.minimum_charge[self.battery_selected.get()],
            # state=DISABLED
        )
        self.minimum_charge_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        def enter_minimum_charge(_):
            self.minimum_charge[self.battery_selected.get()].set(
                round(self.minimum_charge_entry.get(), 2)
            )
            self.maximum_charge[self.battery_selected.get()].set(
                round(
                    max(
                        self.maximum_charge[self.battery_selected.get()].get(),
                        self.minimum_charge[self.battery_selected.get()].get(),
                    ),
                    2,
                )
            )
            self.maximum_charge_slider.set(
                self.maximum_charge[self.battery_selected.get()].get()
            )
            self.minimum_charge_slider.set(
                int(self.minimum_charge[self.battery_selected.get()].get())
            )

        self.minimum_charge_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.minimum_charge[self.battery_selected.get()],
        )
        self.minimum_charge_entry.grid(row=4, column=2, padx=10, pady=5, sticky="ew")
        self.minimum_charge_entry.bind("<Return>", enter_minimum_charge)

        self.minimum_charge_unit = ttk.Label(self.scrollable_frame, text=f"%")
        self.minimum_charge_unit.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        # Leakage
        self.leakage_label = ttk.Label(self.scrollable_frame, text="Leakage")
        self.leakage_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.leakage: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 30, f"{battery_name}_leakage")
            for battery_name in self.battery_name_values
        }
        self.leakage_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.leakage[self.battery_selected.get()],
        )
        self.leakage_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew", ipadx=80)

        self.leakage_unit = ttk.Label(self.scrollable_frame, text="% / hour")
        self.leakage_unit.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # Conversion efficiency in
        self.conversion_efficiency_in_label = ttk.Label(
            self.scrollable_frame, text="Conversion efficiency in"
        )
        self.conversion_efficiency_in_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        self.conversion_efficiency_in: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(
                self, 97, f"{battery_name}_conversion_efficiency_in"
            )
            for battery_name in self.battery_name_values
        }

        def scalar_conversion_efficiency_in(_):
            self.conversion_efficiency_in[self.battery_selected.get()].set(
                round(self.conversion_efficiency_in_slider.get(), 1)
            )
            self.conversion_efficiency_in_entry.update()

        self.conversion_efficiency_in_slider = ttk.Scale(
            self.scrollable_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_conversion_efficiency_in,
            bootstyle=WARNING,
            variable=self.conversion_efficiency_in[self.battery_selected.get()],
        )
        self.conversion_efficiency_in_slider.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew"
        )

        def enter_conversion_efficiency_in(_):
            self.conversion_efficiency_in[self.battery_selected.get()].set(
                round(self.conversion_efficiency_in_entry.get(), 2)
            )
            self.conversion_efficiency_in_slider.set(
                round(
                    self.conversion_efficiency_in[self.battery_selected.get()].get(), 2
                )
            )

        self.conversion_efficiency_in_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.conversion_efficiency_in[self.battery_selected.get()],
        )
        self.conversion_efficiency_in_entry.grid(
            row=6, column=2, padx=10, pady=5, sticky="ew"
        )
        self.conversion_efficiency_in_entry.bind(
            "<Return>", enter_conversion_efficiency_in
        )

        self.conversion_efficiency_in_unit = ttk.Label(self.scrollable_frame, text=f"%")
        self.conversion_efficiency_in_unit.grid(
            row=6, column=3, padx=10, pady=5, sticky="ew"
        )

        # Conversion Efficiency (Output)
        self.conversion_efficiency_out_label = ttk.Label(
            self.scrollable_frame, text="Conversion efficiency out"
        )
        self.conversion_efficiency_out_label.grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )

        self.conversion_efficiency_out: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(
                self, 95, f"{battery_name}_conversion_efficiency_out"
            )
            for battery_name in self.battery_name_values
        }

        def scalar_conversion_efficiency_out(_):
            self.conversion_efficiency_out[self.battery_selected.get()].set(
                round(self.conversion_efficiency_out_slider.get(), 1)
            )
            self.conversion_efficiency_out_entry.update()

        self.conversion_efficiency_out_slider = ttk.Scale(
            self.scrollable_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_conversion_efficiency_out,
            bootstyle=WARNING,
            variable=self.conversion_efficiency_out[self.battery_selected.get()],
        )
        self.conversion_efficiency_out_slider.grid(
            row=7, column=1, padx=10, pady=5, sticky="ew"
        )

        def enter_conversion_efficiency_out(_):
            self.conversion_efficiency_out[self.battery_selected.get()].set(
                round(self.conversion_efficiency_out_entry.get(), 2)
            )
            self.conversion_efficiency_out_slider.set(
                round(
                    self.conversion_efficiency_out[self.battery_selected.get()].get(), 2
                )
            )

        self.conversion_efficiency_out_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.conversion_efficiency_out[self.battery_selected.get()],
        )
        self.conversion_efficiency_out_entry.grid(
            row=7, column=2, padx=10, pady=5, sticky="ew"
        )
        self.conversion_efficiency_out_entry.bind(
            "<Return>", enter_conversion_efficiency_out
        )

        self.conversion_efficiency_out_unit = ttk.Label(
            self.scrollable_frame, text=f"%"
        )
        self.conversion_efficiency_out_unit.grid(
            row=7, column=3, padx=10, pady=5, sticky="ew"
        )

        # Cycle lifetime
        self.cycle_lifetime_label = ttk.Label(
            self.scrollable_frame, text="Cycle lifetime"
        )
        self.cycle_lifetime_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.cycle_lifetime: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 2000, f"{battery_name}_cycle_lifetime")
            for battery_name in self.battery_name_values
        }
        self.cycle_lifetime_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.cycle_lifetime[self.battery_selected.get()],
        )
        self.cycle_lifetime_entry.grid(
            row=8, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.cycle_lifetime_unit = ttk.Label(self.scrollable_frame, text="cycles")
        self.cycle_lifetime_unit.grid(row=8, column=2, padx=10, pady=5, sticky="w")

        # Lifetime capacity loss
        self.lifetime_capacity_loss_label = ttk.Label(
            self.scrollable_frame, text="Lifetime capacity loss"
        )
        self.lifetime_capacity_loss_label.grid(
            row=9, column=0, padx=10, pady=5, sticky="w"
        )

        self.lifetime_capacity_loss: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(
                self, 0, f"{battery_name}_lifetime_capacity_loss"
            )
            for battery_name in self.battery_name_values
        }

        def scalar_lifetime_capacity_loss(_):
            self.lifetime_capacity_loss[self.battery_selected.get()].set(
                round(self.lifetime_capacity_loss_slider.get(), 1)
            )
            # self.lifetime_capacity_loss_entry.configure(str(self.lifetime_capacity_loss.get()))
            self.lifetime_capacity_loss_entry.update()

        self.lifetime_capacity_loss_slider = ttk.Scale(
            self.scrollable_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_lifetime_capacity_loss,
            bootstyle=WARNING,
            variable=self.lifetime_capacity_loss[self.battery_selected.get()],
            # state=DISABLED
        )
        self.lifetime_capacity_loss_slider.grid(
            row=9, column=1, padx=10, pady=5, sticky="ew"
        )

        def enter_lifetime_capacity_loss(_):
            self.lifetime_capacity_loss[self.battery_selected.get()].set(
                round(self.lifetime_capacity_loss_entry.get(), 2)
            )
            self.lifetime_capacity_loss_slider.set(
                round(self.lifetime_capacity_loss[self.battery_selected.get()].get(), 2)
            )

        self.lifetime_capacity_loss_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.lifetime_capacity_loss[self.battery_selected.get()],
        )
        self.lifetime_capacity_loss_entry.grid(
            row=9, column=2, padx=10, pady=5, sticky="ew"
        )
        self.lifetime_capacity_loss_entry.bind("<Return>", enter_lifetime_capacity_loss)

        self.lifetime_capacity_loss_unit = ttk.Label(self.scrollable_frame, text=f"%")
        self.lifetime_capacity_loss_unit.grid(
            row=9, column=3, padx=10, pady=5, sticky="ew"
        )

        # C-rate discharging
        self.c_rate_discharging_label = ttk.Label(
            self.scrollable_frame, text="C-rate discharging"
        )
        self.c_rate_discharging_label.grid(
            row=10, column=0, padx=10, pady=5, sticky="w"
        )

        self.c_rate_discharging: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(
                self, 0.33, f"{battery_name}_c_rate_discharging"
            )
            for battery_name in self.battery_name_values
        }
        self.c_rate_discharging_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.c_rate_discharging[self.battery_selected.get()],
        )
        self.c_rate_discharging_entry.grid(
            row=10, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.c_rate_discharging_unit = ttk.Label(
            self.scrollable_frame, text="fraction of capacity / hour"
        )
        self.c_rate_discharging_unit.grid(row=10, column=2, padx=10, pady=5, sticky="w")

        # C-rate charging
        self.c_rate_charging_label = ttk.Label(
            self.scrollable_frame, text="C-rate charging"
        )
        self.c_rate_charging_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")

        self.c_rate_charging: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 0.33, f"{battery_name}_c_rate_charging")
            for battery_name in self.battery_name_values
        }
        self.c_rate_charging_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.c_rate_charging[self.battery_selected.get()],
        )
        self.c_rate_charging_entry.grid(
            row=11, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.c_rate_charging_unit = ttk.Label(
            self.scrollable_frame, text="fraction of  capacity / hour"
        )
        self.c_rate_charging_unit.grid(row=11, column=2, padx=10, pady=5, sticky="w")

        # Cost
        self.cost_label = ttk.Label(self.scrollable_frame, text="Storage cost")
        self.cost_label.grid(row=12, column=0, padx=10, pady=5, sticky="w")

        self.costs: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 0, f"{battery_name}_cost")
            for battery_name in self.battery_name_values
        }
        self.cost_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.costs[self.battery_selected.get()],
        )
        self.cost_entry.grid(row=12, column=1, padx=10, pady=5, sticky="ew", ipadx=80)

        self.cost_unit = ttk.Label(self.scrollable_frame, text="$ / kWh")
        self.cost_unit.grid(row=12, column=2, padx=10, pady=5, sticky="w")

        # Cost decrease
        self.cost_decrease_label = ttk.Label(
            self.scrollable_frame, text="Storage cost change"
        )
        self.cost_decrease_label.grid(row=13, column=0, padx=10, pady=5, sticky="w")

        self.cost_decrease: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 0, f"{battery_name}_cost_decrease")
            for battery_name in self.battery_name_values
        }
        self.cost_decrease_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.cost_decrease[self.battery_selected.get()],
        )
        self.cost_decrease_entry.grid(
            row=13, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.cost_decrease_unit = ttk.Label(self.scrollable_frame, text="%  / year")
        self.cost_decrease_unit.grid(row=13, column=2, padx=10, pady=5, sticky="w")

        # OPEX costs
        self.opex_costs_label = ttk.Label(
            self.scrollable_frame, text="OPEX (O&M) costs"
        )
        self.opex_costs_label.grid(row=14, column=0, padx=10, pady=5, sticky="w")

        self.o_and_m_costs: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 0, f"{battery_name}_o_and_m_costs")
            for battery_name in self.battery_name_values
        }
        self.o_and_m_costs_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.o_and_m_costs[self.battery_selected.get()],
        )
        self.o_and_m_costs_entry.grid(
            row=14, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.o_and_m_costs_unit = ttk.Label(
            self.scrollable_frame, text="$ / kWh / year"
        )
        self.o_and_m_costs_unit.grid(row=14, column=2, padx=10, pady=5, sticky="w")

        # Embedded emissions
        self.embedded_emissions_label = ttk.Label(
            self.scrollable_frame, text="Storage embedded emissions"
        )
        self.embedded_emissions_label.grid(
            row=15, column=0, padx=10, pady=5, sticky="w"
        )

        self.embedded_emissions: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 0, f"{battery_name}_ghgs")
            for battery_name in self.battery_name_values
        }
        self.embedded_emissions_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.embedded_emissions[self.battery_selected.get()],
        )
        self.embedded_emissions_entry.grid(
            row=15, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.embedded_emissions_unit = ttk.Label(
            self.scrollable_frame, text="kgCO2eq / unit"
        )
        self.embedded_emissions_unit.grid(row=15, column=2, padx=10, pady=5, sticky="w")

        # O&M emissions
        self.om_emissions_label = ttk.Label(self.scrollable_frame, text="O&M emissions")
        self.om_emissions_label.grid(row=16, column=0, padx=10, pady=5, sticky="w")

        self.om_emissions: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 0, f"{battery_name}_o_and_m_ghgs")
            for battery_name in self.battery_name_values
        }
        self.om_emissions_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.om_emissions[self.battery_selected.get()],
        )
        self.om_emissions_entry.grid(
            row=16, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.om_emissions_unit = ttk.Label(
            self.scrollable_frame, text="kgCO2eq / kWh / year"
        )
        self.om_emissions_unit.grid(row=16, column=2, padx=10, pady=5, sticky="w")

        # Annual emissions decrease
        self.annual_emissions_decrease_label = ttk.Label(
            self.scrollable_frame, text="Storage embedded emissions change"
        )
        self.annual_emissions_decrease_label.grid(
            row=17, column=0, padx=10, pady=5, sticky="w"
        )

        self.annual_emissions_decrease: dict[str, ttk.DoubleVar] = {
            battery_name: ttk.DoubleVar(self, 0, f"{battery_name}_ghgs_decrease")
            for battery_name in self.battery_name_values
        }
        self.annual_emissions_decrease_entry = ttk.Entry(
            self.scrollable_frame,
            bootstyle=WARNING,
            textvariable=self.annual_emissions_decrease[self.battery_selected.get()],
        )
        self.annual_emissions_decrease_entry.grid(
            row=17, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.annual_emissions_decrease_unit = ttk.Label(
            self.scrollable_frame, text="% / year"
        )
        self.annual_emissions_decrease_unit.grid(
            row=17, column=2, padx=10, pady=5, sticky="w"
        )

        # TODO: Add configuration frame widgets and layout

    def add_battery(self) -> None:
        """Called when a user presses the new battery button."""

        # Determine the new name
        new_name = "New{suffix}"
        index = 0
        suffix = ""
        while new_name.format(suffix=suffix) in self.battery_name_values:
            index += 1
            suffix = f"_{index}"

        new_name = new_name.format(suffix=suffix)

        self.battery_name_values[new_name] = ttk.StringVar(self, new_name)
        self.populate_available_batteries()

        # Update all the mappings stored
        self.battery_capacities[new_name] = ttk.DoubleVar(self, 0)
        self.maximum_charge[new_name] = ttk.DoubleVar(self, 100)
        self.minimum_charge[new_name] = ttk.DoubleVar(self, 0)
        self.leakage[new_name] = ttk.DoubleVar(self, 0)
        self.conversion_efficiency_in[new_name] = ttk.DoubleVar(self, 100)
        self.conversion_efficiency_out[new_name] = ttk.DoubleVar(self, 100)
        self.cycle_lifetime[new_name] = ttk.DoubleVar(self, 0)
        self.lifetime_capacity_loss[new_name] = ttk.DoubleVar(self, 100)
        self.c_rate_discharging[new_name] = ttk.DoubleVar(self, 1)
        self.c_rate_charging[new_name] = ttk.DoubleVar(self, 1)
        self.costs[new_name] = ttk.DoubleVar(self, 0)
        self.cost_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.o_and_m_costs[new_name] = ttk.DoubleVar(self, 0)
        self.embedded_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.om_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.annual_emissions_decrease[new_name] = ttk.DoubleVar(self, 0)

        # Select the new battery and update the screen
        self.battery_selected = self.battery_name_values[new_name]
        self.battery_selected_combobox.configure(textvariable=self.battery_selected)
        self.battery_name_entry.configure(textvariable=self.battery_selected)
        self.update_battery_frame()

        # Add the battery to the system frame
        self.add_battery_to_scenario_frame(new_name)

    @property
    def batteries(self) -> list[dict[str, float | dict[str, float]]]:
        """
        Return a list of batteries based on the information provided in the frame.

        :return:
            The batteries based on the frame's information.


        """

        batteries: list[dict[str, float | dict[str, float]]] = []

        for battery_name in self.battery_name_values:
            battery_dict = Battery(
                self.battery_capacities[battery_name].get(),
                self.cycle_lifetime[battery_name].get(),
                self.leakage[battery_name].get() / 100,
                self.maximum_charge[battery_name].get() / 100,
                self.minimum_charge[battery_name].get() / 100,
                battery_name,
                self.c_rate_charging[battery_name].get(),
                self.conversion_efficiency_in[battery_name].get() / 100,
                self.conversion_efficiency_out[battery_name].get() / 100,
                self.c_rate_discharging[battery_name].get(),
                self.lifetime_capacity_loss[battery_name].get() / 100,
                self.battery_capacities[battery_name].get(),
                True,
            ).as_dict

            # Append cost and emissions information
            battery_dict[COSTS] = {
                COST: self.costs[battery_name].get(),
                COST_DECREASE: -(self.cost_decrease[battery_name].get()),
                OM: self.o_and_m_costs[battery_name].get(),
            }

            battery_dict[EMISSIONS] = {
                GHGS: self.embedded_emissions[battery_name].get(),
                GHG_DECREASE: -(self.annual_emissions_decrease[battery_name].get()),
                OM_GHGS: self.om_emissions[battery_name].get(),
            }

            batteries.append(battery_dict)

        return batteries

    def enter_battery_name(self, _=None) -> None:
        """Called when someone enters a new battery name."""
        self.populate_available_batteries()

        # Update all the mappings stored
        self.battery_capacities = {
            self.battery_name_values[key].get(): value
            for key, value in self.battery_capacities.items()
        }
        self.maximum_charge = {
            self.battery_name_values[key].get(): value
            for key, value in self.maximum_charge.items()
        }
        self.minimum_charge = {
            self.battery_name_values[key].get(): value
            for key, value in self.minimum_charge.items()
        }
        self.leakage = {
            self.battery_name_values[key].get(): value
            for key, value in self.leakage.items()
        }
        self.conversion_efficiency_in = {
            self.battery_name_values[key].get(): value
            for key, value in self.conversion_efficiency_in.items()
        }
        self.conversion_efficiency_out = {
            self.battery_name_values[key].get(): value
            for key, value in self.conversion_efficiency_out.items()
        }
        self.cycle_lifetime = {
            self.battery_name_values[key].get(): value
            for key, value in self.cycle_lifetime.items()
        }
        self.lifetime_capacity_loss = {
            self.battery_name_values[key].get(): value
            for key, value in self.lifetime_capacity_loss.items()
        }
        self.c_rate_discharging = {
            self.battery_name_values[key].get(): value
            for key, value in self.c_rate_discharging.items()
        }
        self.c_rate_charging = {
            self.battery_name_values[key].get(): value
            for key, value in self.c_rate_charging.items()
        }
        self.costs = {
            self.battery_name_values[key].get(): value
            for key, value in self.costs.items()
        }
        self.cost_decrease = {
            self.battery_name_values[key].get(): value
            for key, value in self.cost_decrease.items()
        }
        self.o_and_m_costs = {
            self.battery_name_values[key].get(): value
            for key, value in self.o_and_m_costs.items()
        }
        self.embedded_emissions = {
            self.battery_name_values[key].get(): value
            for key, value in self.embedded_emissions.items()
        }
        self.om_emissions = {
            self.battery_name_values[key].get(): value
            for key, value in self.om_emissions.items()
        }
        self.annual_emissions_decrease = {
            self.battery_name_values[key].get(): value
            for key, value in self.annual_emissions_decrease.items()
        }

        # Update the battery-name values.
        self.battery_name_values = {
            entry.get(): entry for entry in self.battery_name_values.values()
        }

        # Update the battery names on the sysetm frame
        self.set_batteries_on_system_frame(list(self.battery_name_values.keys()))

    def populate_available_batteries(self) -> None:
        """Populate the combo box with the set of avialable batteries."""

        self.battery_selected_combobox["values"] = [
            entry.get() for entry in self.battery_name_values.values()
        ]

    def select_battery(self, _) -> None:
        # Determine the battery name pre- and post-selection
        previous_battery_name: str = {
            (entry == self.battery_selected): key
            for key, entry in self.battery_name_values.items()
        }[True]
        selected_battery_name: str = self.battery_selected_combobox.get()

        # Reset the value of the old variable
        self.battery_name_values[previous_battery_name].set(previous_battery_name)

        # Set the variable to be the new selected variable
        self.battery_selected = self.battery_name_values[selected_battery_name]
        self.battery_selected_combobox.configure(textvariable=self.battery_selected)
        self.battery_name_entry.configure(textvariable=self.battery_selected)

        # Update the variables being displayed.
        self.update_battery_frame()

    def set_batteries(
        self,
        batteries: list[Battery],
        battery_costs: dict[str, dict[str, float]],
        battery_emissions: dict[str, dict[str, float]],
    ) -> None:
        """
        Set the battery information for the frame based on the inputs provided.

        :param: batteries
            The `list` of :class:`storage_utils.Battery` instances defined;

        :param: battery_costs
            The battery cost information

        :param: battery_emissions
            The battery emissions information;

        """

        self.battery_name_values: dict[str, ttk.StringVar] = {}
        self.battery_capacities = {}
        self.maximum_charge = {}
        self.minimum_charge = {}
        self.leakage = {}
        self.conversion_efficiency_in = {}
        self.conversion_efficiency_out = {}
        self.cycle_lifetime = {}
        self.lifetime_capacity_loss = {}
        self.c_rate_charging = {}
        self.c_rate_discharging = {}
        self.costs = {}
        self.cost_decrease = {}
        self.o_and_m_costs = {}
        self.embedded_emissions = {}
        self.om_emissions = {}
        self.annual_emissions_decrease = {}

        for battery in batteries:
            self.battery_name_values[battery.name] = ttk.StringVar(self, battery.name)

            # Performance characteristics
            self.battery_capacities[battery.name] = ttk.DoubleVar(
                self, battery.capacity
            )
            self.maximum_charge[battery.name] = ttk.DoubleVar(
                self, 100 * battery.maximum_charge
            )
            self.minimum_charge[battery.name] = ttk.DoubleVar(
                self, 100 * battery.minimum_charge
            )
            self.leakage[battery.name] = ttk.DoubleVar(self, 100 * battery.leakage)
            self.conversion_efficiency_in[battery.name] = ttk.DoubleVar(
                self, 100 * battery.conversion_in
            )
            self.conversion_efficiency_out[battery.name] = ttk.DoubleVar(
                self, 100 * battery.conversion_out
            )
            self.cycle_lifetime[battery.name] = ttk.DoubleVar(
                self, battery.cycle_lifetime
            )
            self.lifetime_capacity_loss[battery.name] = ttk.DoubleVar(
                self, 100 * battery.lifetime_loss
            )
            self.c_rate_discharging[battery.name] = ttk.DoubleVar(
                self, battery.discharge_rate
            )
            self.c_rate_charging[battery.name] = ttk.DoubleVar(
                self, battery.charge_rate
            )

            # Costs
            self.costs[battery.name] = ttk.DoubleVar(
                self, (this_battery_costs := battery_costs[battery.name]).get(COST, 0)
            )
            self.cost_decrease[battery.name] = ttk.DoubleVar(
                self, -(this_battery_costs.get(COST_DECREASE, 0))
            )
            self.o_and_m_costs[battery.name] = ttk.DoubleVar(
                self, this_battery_costs.get(OM, 0)
            )

            # Emissions
            self.embedded_emissions[battery.name] = ttk.DoubleVar(
                self,
                (this_battery_emissions := battery_emissions[battery.name]).get(
                    GHGS, 0
                ),
            )
            self.om_emissions[battery.name] = ttk.DoubleVar(
                self, this_battery_emissions.get(OM_GHGS, 0)
            )
            self.annual_emissions_decrease[battery.name] = ttk.DoubleVar(
                self, -(this_battery_emissions.get(GHG_DECREASE, 0))
            )

        self.battery_selected = self.battery_name_values[batteries[0].name]
        self.battery_selected_combobox["values"] = [
            battery.name for battery in batteries
        ]
        self.battery_selected_combobox.set(self.battery_selected.get())
        self.select_battery(self.battery_selected.get())

    def update_battery_frame(self) -> None:
        """
        Updates the entries so that the correct variables are displayed on the screen.

        """

        self.battery_capacity_entry.configure(
            textvariable=self.battery_capacities[self.battery_selected.get()]
        )
        self.maximum_charge_entry.configure(
            textvariable=self.maximum_charge[self.battery_selected.get()]
        )
        self.maximum_charge_slider.configure(
            variable=self.maximum_charge[self.battery_selected.get()]
        )
        self.minimum_charge_entry.configure(
            textvariable=self.minimum_charge[self.battery_selected.get()]
        )
        self.minimum_charge_slider.configure(
            variable=self.minimum_charge[self.battery_selected.get()]
        )
        self.leakage_entry.configure(
            textvariable=self.leakage[self.battery_selected.get()]
        )
        self.conversion_efficiency_in_slider.configure(
            variable=self.conversion_efficiency_in[self.battery_selected.get()]
        )
        self.conversion_efficiency_in_entry.configure(
            textvariable=self.conversion_efficiency_in[self.battery_selected.get()]
        )
        self.conversion_efficiency_out_slider.configure(
            variable=self.conversion_efficiency_out[self.battery_selected.get()]
        )
        self.conversion_efficiency_out_entry.configure(
            textvariable=self.conversion_efficiency_out[self.battery_selected.get()]
        )
        self.cycle_lifetime_entry.configure(
            textvariable=self.cycle_lifetime[self.battery_selected.get()]
        )
        self.lifetime_capacity_loss_slider.configure(
            variable=self.lifetime_capacity_loss[self.battery_selected.get()]
        )
        self.lifetime_capacity_loss_entry.configure(
            textvariable=self.lifetime_capacity_loss[self.battery_selected.get()]
        )
        self.c_rate_discharging_entry.configure(
            textvariable=self.c_rate_discharging[self.battery_selected.get()]
        )
        self.c_rate_charging_entry.configure(
            textvariable=self.c_rate_charging[self.battery_selected.get()]
        )
        self.cost_entry.configure(textvariable=self.costs[self.battery_selected.get()])
        self.cost_decrease_entry.configure(
            textvariable=self.cost_decrease[self.battery_selected.get()]
        )
        self.o_and_m_costs_entry.configure(
            textvariable=self.o_and_m_costs[self.battery_selected.get()]
        )
        self.embedded_emissions_entry.configure(
            textvariable=self.embedded_emissions[self.battery_selected.get()]
        )
        self.annual_emissions_decrease_entry.configure(
            textvariable=self.annual_emissions_decrease[self.battery_selected.get()]
        )
        self.om_emissions_entry.configure(
            textvariable=self.om_emissions[self.battery_selected.get()]
        )

        # Update the entries
        self.battery_capacity_entry.update()
        self.maximum_charge_entry.update()
        self.minimum_charge_entry.update()
        self.maximum_charge_slider.update()
        self.minimum_charge_slider.update()
        self.leakage_entry.update()
        self.conversion_efficiency_in_slider.update()
        self.conversion_efficiency_in_entry.update()
        self.conversion_efficiency_out_slider.update()
        self.conversion_efficiency_out_entry.update()
        self.cycle_lifetime_entry.update()
        self.lifetime_capacity_loss_slider.update()
        self.lifetime_capacity_loss_entry.update()
        self.c_rate_discharging_entry.update()
        self.c_rate_charging_entry.update()
        self.cost_entry.update()
        self.cost_decrease_entry.update()
        self.o_and_m_costs_entry.update()
        self.embedded_emissions_entry.update()
        self.annual_emissions_decrease_entry.update()
        self.om_emissions_entry.update()


class TankFrame(ttk.Frame):
    """
    Represents the Tank frame.

    Contains settings for the tank units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Tank frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class StorageFrame(ttk.Frame):
    """
    Represents the Storage frame.

    Contains settings for storage units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.storage_notebook = ttk.Notebook(self, bootstyle=WARNING)
        self.storage_notebook.grid(row=0, column=0, padx=20, pady=10, sticky="news")

        self.battery_frame = BatteryFrame(self)
        self.storage_notebook.add(self.battery_frame, text="Batteries", sticky="news")

        self.tank_frame = TankFrame(self)
        # self.storage_notebook.add(
        #     self.tank_frame, text="Water tanks", sticky="news", state=DISABLED
        # )

        # TODO: Add configuration frame widgets and layout
