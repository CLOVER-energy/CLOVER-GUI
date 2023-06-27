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

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


__all__ = ("StorageFrame",)


class BatteryFrame(ttk.Frame):
    """
    Represents the Battery frame.

    Contains settings for the battery units.

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

        # Battery being selected
        self.battery_selected_label = ttk.Label(self, text="Battery to model")
        self.battery_selected_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.battery_selected = ttk.StringVar(self, "Li-Ion", "battery_selected")
        self.battery_selected_entry = ttk.Combobox(
            self, bootstyle=WARNING, textvariable=self.battery_selected
        )
        self.battery_selected_entry.grid(
            row=0, column=1, padx=10, pady=5, sticky="w", ipadx=60
        )
        self.populate_available_batteries()

        # Battery name
        self.battery_name_label = ttk.Label(self, text="Battery name")
        self.battery_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.battery_name_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.battery_selected
        )
        self.battery_name_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        # Battery capacity
        self.battery_capacity_label = ttk.Label(self, text="Capacity")
        self.battery_capacity_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.battery_capacity = ttk.DoubleVar()

        self.battery_capacity_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.battery_capacity
        )
        self.battery_capacity_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.battery_capacity_unit = ttk.Label(self, text="kWh")
        self.battery_capacity_unit.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # Maximum charge
        self.maximum_charge_label = ttk.Label(self, text="Maximum state of charge")
        self.maximum_charge_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.maximum_charge = ttk.DoubleVar(self, 90, "maximum_charge")

        def scalar_maximum_charge(_):
            self.minimum_charge.set(
                min(self.maximum_charge.get(), self.minimum_charge.get())
            )
            self.maximum_charge_entry.update()

        self.maximum_charge_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_maximum_charge,
            bootstyle=WARNING,
            variable=self.maximum_charge,
            # state=DISABLED
        )
        self.maximum_charge_slider.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        def enter_maximum_charge(_):
            self.minimum_charge.set(
                min(self.maximum_charge.get(), self.minimum_charge.get())
            )
            self.maximum_charge.set(self.maximum_charge_entry.get())
            self.maximum_charge_slider.set(self.maximum_charge.get())

        self.maximum_charge_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.maximum_charge
        )
        self.maximum_charge_entry.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
        self.maximum_charge_entry.bind("<Return>", enter_maximum_charge)

        self.maximum_charge_unit = ttk.Label(self, text=f"%")
        self.maximum_charge_unit.grid(row=3, column=3, padx=10, pady=5, sticky="ew")

        # Minimum charge
        self.minimum_charge_label = ttk.Label(self, text="Minimum state of charge")
        self.minimum_charge_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.minimum_charge = ttk.DoubleVar(self, 20, "minimum_charge")

        def scalar_minimum_charge(_):
            self.maximum_charge.set(
                max(self.maximum_charge.get(), self.minimum_charge.get())
            )
            self.minimum_charge_entry.update()

        self.minimum_charge_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_minimum_charge,
            bootstyle=WARNING,
            variable=self.minimum_charge,
            # state=DISABLED
        )
        self.minimum_charge_slider.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        def enter_minimum_charge(_):
            self.minimum_charge.set(self.minimum_charge_entry.get())
            self.maximum_charge.set(
                max(self.maximum_charge.get(), self.minimum_charge.get())
            )
            self.minimum_charge_slider.set(self.minimum_charge.get())

        self.minimum_charge_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.minimum_charge
        )
        self.minimum_charge_entry.grid(row=4, column=2, padx=10, pady=5, sticky="ew")
        self.minimum_charge_entry.bind("<Return>", enter_minimum_charge)

        self.minimum_charge_unit = ttk.Label(self, text=f"%")
        self.minimum_charge_unit.grid(row=4, column=3, padx=10, pady=5, sticky="ew")

        # Leakage
        self.leakage_label = ttk.Label(self, text="Leakage")
        self.leakage_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.leakage = ttk.DoubleVar(self, 30, "leakage")
        self.leakage_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.leakage
        )
        self.leakage_entry.grid(row=5, column=1, padx=10, pady=5, sticky="ew", ipadx=80)

        self.leakage_unit = ttk.Label(self, text="% / hour")
        self.leakage_unit.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # Conversion efficiency in
        self.conversion_efficiency_in_label = ttk.Label(
            self, text="Conversion efficiency in"
        )
        self.conversion_efficiency_in_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        self.conversion_efficiency_in = ttk.DoubleVar(
            self, 97, "conversion_efficiency_in"
        )

        def scalar_conversion_efficiency_in(_):
            self.conversion_efficiency_in.set(
                self.conversion_efficiency_in_slider.get()
            )
            self.conversion_efficiency_in_entry.update()

        self.conversion_efficiency_in_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_conversion_efficiency_in,
            bootstyle=WARNING,
            variable=self.conversion_efficiency_in,
        )
        self.conversion_efficiency_in_slider.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew"
        )

        def enter_conversion_efficiency_in(_):
            self.conversion_efficiency_in.set(self.conversion_efficiency_in_entry.get())
            self.conversion_efficiency_in_slider.set(
                self.conversion_efficiency_in.get()
            )

        self.conversion_efficiency_in_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.conversion_efficiency_in
        )
        self.conversion_efficiency_in_entry.grid(
            row=6, column=2, padx=10, pady=5, sticky="ew"
        )
        self.conversion_efficiency_in_entry.bind(
            "<Return>", enter_conversion_efficiency_in
        )

        self.conversion_efficiency_in_unit = ttk.Label(self, text=f"%")
        self.conversion_efficiency_in_unit.grid(
            row=6, column=3, padx=10, pady=5, sticky="ew"
        )

        # Conversion Efficiency (Output)
        self.conversion_efficiency_out_label = ttk.Label(
            self, text="Conversion efficiency out"
        )
        self.conversion_efficiency_out_label.grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )

        self.conversion_efficiency_out = ttk.DoubleVar(
            self, 95, "conversion_efficiency_out"
        )

        def scalar_conversion_efficiency_out(_):
            self.conversion_efficiency_out.set(
                self.conversion_efficiency_out_slider.get()
            )
            self.conversion_efficiency_out_entry.update()

        self.conversion_efficiency_out_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_conversion_efficiency_out,
            bootstyle=WARNING,
            variable=self.conversion_efficiency_out,
        )
        self.conversion_efficiency_out_slider.grid(
            row=7, column=1, padx=10, pady=5, sticky="ew"
        )

        def enter_conversion_efficiency_out(_):
            self.conversion_efficiency_out.set(
                self.conversion_efficiency_out_entry.get()
            )
            self.conversion_efficiency_out_slider.set(
                self.conversion_efficiency_out.get()
            )

        self.conversion_efficiency_out_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.conversion_efficiency_out
        )
        self.conversion_efficiency_out_entry.grid(
            row=7, column=2, padx=10, pady=5, sticky="ew"
        )
        self.conversion_efficiency_out_entry.bind(
            "<Return>", enter_conversion_efficiency_out
        )

        self.conversion_efficiency_out_unit = ttk.Label(self, text=f"%")
        self.conversion_efficiency_out_unit.grid(
            row=7, column=3, padx=10, pady=5, sticky="ew"
        )

        # Cycle lifetime
        self.cycle_lifetime_label = ttk.Label(self, text="Cycle lifetime")
        self.cycle_lifetime_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        self.cycle_lifetime = ttk.IntVar(self, 2000, "cycle_lifetime")
        self.cycle_lifetime_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.cycle_lifetime
        )
        self.cycle_lifetime_entry.grid(
            row=8, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.cycle_lifetime_unit = ttk.Label(self, text="cycles")
        self.cycle_lifetime_unit.grid(row=8, column=2, padx=10, pady=5, sticky="w")

        # Lifetime capacity loss
        self.lifetime_capacity_loss_label = ttk.Label(
            self, text="Lifetime capacity loss"
        )
        self.lifetime_capacity_loss_label.grid(
            row=9, column=0, padx=10, pady=5, sticky="w"
        )

        self.lifetime_capacity_loss = ttk.DoubleVar(self, 0, "lifetime_capacity_loss")

        def scalar_lifetime_capacity_loss(_):
            self.lifetime_capacity_loss.set(self.lifetime_capacity_loss_slider.get())
            # self.lifetime_capacity_loss_entry.configure(str(self.lifetime_capacity_loss.get()))
            self.lifetime_capacity_loss_entry.update()

        self.lifetime_capacity_loss_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_lifetime_capacity_loss,
            bootstyle=WARNING,
            variable=self.lifetime_capacity_loss,
            # state=DISABLED
        )
        self.lifetime_capacity_loss_slider.grid(
            row=9, column=1, padx=10, pady=5, sticky="ew"
        )

        def enter_lifetime_capacity_loss(_):
            self.lifetime_capacity_loss.set(self.lifetime_capacity_loss_entry.get())
            self.lifetime_capacity_loss_slider.set(self.lifetime_capacity_loss.get())

        self.lifetime_capacity_loss_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.lifetime_capacity_loss
        )
        self.lifetime_capacity_loss_entry.grid(
            row=9, column=2, padx=10, pady=5, sticky="ew"
        )
        self.lifetime_capacity_loss_entry.bind("<Return>", enter_lifetime_capacity_loss)

        self.lifetime_capacity_loss_unit = ttk.Label(self, text=f"%")
        self.lifetime_capacity_loss_unit.grid(
            row=9, column=3, padx=10, pady=5, sticky="ew"
        )

        # C-rate discharging
        self.c_rate_discharging_label = ttk.Label(self, text="C-rate discharging")
        self.c_rate_discharging_label.grid(
            row=10, column=0, padx=10, pady=5, sticky="w"
        )

        self.c_rate_discharging = ttk.DoubleVar(self, 0, "c_rate_discharging")
        self.c_rate_discharging_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.c_rate_discharging
        )
        self.c_rate_discharging_entry.grid(
            row=10, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.c_rate_discharging_unit = ttk.Label(self, text="% of capacity / hour")
        self.c_rate_discharging_unit.grid(row=10, column=2, padx=10, pady=5, sticky="w")

        # C-rate charging
        self.c_rate_charging_label = ttk.Label(self, text="C-rate charging")
        self.c_rate_charging_label.grid(row=11, column=0, padx=10, pady=5, sticky="w")

        self.c_rate_charging = ttk.DoubleVar(self, 0, "c_rate_charging")
        self.c_rate_charging_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.c_rate_charging
        )
        self.c_rate_charging_entry.grid(
            row=11, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.c_rate_charging_unit = ttk.Label(self, text="% of  capacity / hour")
        self.c_rate_charging_unit.grid(row=11, column=2, padx=10, pady=5, sticky="w")

        # Cost
        self.cost_label = ttk.Label(self, text="Cost")
        self.cost_label.grid(row=12, column=0, padx=10, pady=5, sticky="w")

        self.cost = ttk.DoubleVar(self, 0, "cost")
        self.cost_entry = ttk.Entry(self, bootstyle=WARNING, textvariable=self.cost)
        self.cost_entry.grid(row=12, column=1, padx=10, pady=5, sticky="ew", ipadx=80)

        self.cost_unit = ttk.Label(self, text="USD ($)")
        self.cost_unit.grid(row=12, column=2, padx=10, pady=5, sticky="w")

        # Cost decrease
        self.cost_decrease_label = ttk.Label(self, text="Cost decrease")
        self.cost_decrease_label.grid(row=13, column=0, padx=10, pady=5, sticky="w")

        self.cost_decrease = ttk.DoubleVar(self, 0, "cost_decrease")
        self.cost_decrease_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.cost_decrease
        )
        self.cost_decrease_entry.grid(
            row=13, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.cost_decrease_unit = ttk.Label(self, text="% decrease / year")
        self.cost_decrease_unit.grid(row=13, column=2, padx=10, pady=5, sticky="w")

        # OPEX costs
        self.opex_costs_label = ttk.Label(self, text="OPEX (O&M) costs")
        self.opex_costs_label.grid(row=14, column=0, padx=10, pady=5, sticky="w")

        self.o_and_m_costs = ttk.DoubleVar(self, 0, "o_and_m_costs")
        self.o_and_m_costs_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.o_and_m_costs
        )
        self.o_and_m_costs_entry.grid(
            row=14, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.o_and_m_costs_unit = ttk.Label(self, text="USD ($)")
        self.o_and_m_costs_unit.grid(row=14, column=2, padx=10, pady=5, sticky="w")

        # Embedded emissions
        self.embedded_emissions_label = ttk.Label(self, text="Embedded emissions")
        self.embedded_emissions_label.grid(
            row=15, column=0, padx=10, pady=5, sticky="w"
        )

        self.embedded_emissions = ttk.DoubleVar(self, 0, "ghgs")
        self.embedded_emissions_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.embedded_emissions
        )
        self.embedded_emissions_entry.grid(
            row=15, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.embedded_emissions_unit = ttk.Label(self, text="kgCO2eq / unit")
        self.embedded_emissions_unit.grid(row=15, column=2, padx=10, pady=5, sticky="w")

        # O&M emissions
        self.om_emissions_label = ttk.Label(self, text="O&M emissions")
        self.om_emissions_label.grid(row=16, column=0, padx=10, pady=5, sticky="w")

        self.om_emissions = ttk.DoubleVar(self, 0, "o_and_m_ghgs")
        self.om_emissions_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.om_emissions
        )
        self.om_emissions_entry.grid(
            row=16, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.om_emissions_unit = ttk.Label(self, text="kgCO2eq / year")
        self.om_emissions_unit.grid(row=16, column=2, padx=10, pady=5, sticky="w")

        # Annual emissions decrease
        self.annual_emissions_decrease_label = ttk.Label(
            self, text="Annual emissions decrease"
        )
        self.annual_emissions_decrease_label.grid(
            row=17, column=0, padx=10, pady=5, sticky="w"
        )

        self.annual_emissions_decrease = ttk.DoubleVar(self, 0, "ghgs_decrease")
        self.annual_emissions_decrease_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.annual_emissions_decrease
        )
        self.annual_emissions_decrease_entry.grid(
            row=17, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.annual_emissions_decrease_unit = ttk.Label(self, text="% / year")
        self.annual_emissions_decrease_unit.grid(
            row=17, column=2, padx=10, pady=5, sticky="w"
        )

        # TODO: Add configuration frame widgets and layout

    def populate_available_batteries(self) -> None:
        """Populate the combo box with the set of avialable batteries."""

        self.battery_selected_entry["values"] = ["Li-Ion", "Pb-Acid", "New Pb-Acid"]


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
        self.storage_notebook.add(
            self.tank_frame, text="Water tanks", sticky="news", state=DISABLED
        )

        # TODO: Add configuration frame widgets and layout
