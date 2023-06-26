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

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import DETAILS_GEOMETRY

__all__ = ("DetailsWindow",)


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

        self.columnconfigure(0, weight=2)  # First row has the header
        self.columnconfigure(1, weight=2)  # These rows have entries
        self.columnconfigure(2, weight=1)  # These rows have entries

        self.pv_panel_entry = ttk.Combobox(self, bootstyle=WARNING)
        self.pv_panel_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w", ipadx=60)
        self.populate_available_panels()

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

        # Panel name
        self.panel_name_label = ttk.Label(self, text="Panel name")
        self.panel_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.panel_name_variable = tk.StringVar(value="m-Si")
        self.panel_name_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.panel_name_variable
        )
        self.panel_name_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        # Panel lifetime
        self.panel_lifetime_label = ttk.Label(self, text="Lifetime")
        self.panel_lifetime_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.panel_lifetime = ttk.IntVar(self, 20, "panel_lifetime")

        self.scalar_lifetime_label = ttk.Label(
            self, text=f"{int(self.panel_lifetime.get())} years"
        )
        self.scalar_lifetime_label.grid(row=2, column=2, sticky="w")

        def scalar(e):
            self.scalar_lifetime_label.config(
                text=f"{' ' * (int(self.panel_lifetime.get()) < 10)}{int(self.panel_lifetime_entry.get())} years"
            )

        self.panel_lifetime_entry = ttk.Scale(
            self,
            from_=0,
            to=30,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar,
            bootstyle=WARNING,
            variable=self.panel_lifetime,
        )
        self.panel_lifetime_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Panel tilt
        self.panel_tilt_label = ttk.Label(self, text="Tilt")
        self.panel_tilt_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.panel_tilt = ttk.IntVar(self, 22, "panel_tilt")

        self.scalar_panel_tilt_label = ttk.Label(
            self, text=f"{int(self.panel_tilt.get())} degrees"
        )
        self.scalar_panel_tilt_label.grid(row=3, column=2, sticky="w")

        def scalar_tilt(_):
            self.scalar_panel_tilt_label.config(
                text=f"{' ' * (int(self.panel_tilt.get()) < 10)}"
                f"{int(self.panel_tilt_entry.get())} degrees"
            )

        self.panel_tilt_entry = ttk.Scale(
            self,
            from_=0,
            to=90,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_tilt,
            bootstyle=WARNING,
            variable=self.panel_tilt,
        )
        self.panel_tilt_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Azimuthal orientation
        self.panel_orientation_label = ttk.Label(self, text="Azimuthal orientation")
        self.panel_orientation_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.panel_orientation = ttk.IntVar(self, 180, "panel_orientation")

        self.scalar_panel_orientation_label = ttk.Label(
            self, text=f"{int(self.panel_orientation.get())} degrees"
        )
        self.scalar_panel_orientation_label.grid(row=4, column=2, sticky="w")

        def scalar_orientation(e):
            self.scalar_panel_orientation_label.config(
                text=f"{' ' * (int(self.panel_orientation.get()) < 100)}"
                f"{' ' * (int(self.panel_orientation.get()) < 10)}"
                f"{int(self.panel_orientation_entry.get())} degrees"
            )

        self.panel_orientation_entry = ttk.Scale(
            self,
            from_=0,
            to=360,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_orientation,
            bootstyle=WARNING,
            variable=self.panel_orientation,
        )
        self.panel_orientation_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Panel present in the system
        self.panel_present_label = ttk.Label(self, text="Panel present")
        self.panel_present_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.panel_present = ttk.BooleanVar(self, True, "panel_present")
        self.panel_present_toggle = ttk.Checkbutton(
            self, variable=self.panel_present, bootstyle=f"round-toggle-{WARNING}"
        )
        self.panel_present_toggle.grid(row=5, column=1, padx=160, sticky="ew")

        # Reference efficiency
        self.reference_efficiency_label = ttk.Label(self, text="Reference efficiency")
        self.reference_efficiency_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        self.reference_efficiency = ttk.DoubleVar(self, 15, "reference_efficiency")

        self.reference_efficiency_unit = ttk.Label(self, text=f" 15%")
        self.reference_efficiency_unit.grid(
            row=6, column=2, padx=10, pady=5, sticky="ew"
        )

        def scalar_reference_efficiency(_):
            self.reference_efficiency_unit.config(
                text=f"{' ' * (int(self.reference_efficiency.get()) < 100)}"
                f"{' ' * (int(self.reference_efficiency.get()) < 10)}"
                f"{abs(round(self.reference_efficiency.get(), 2))}%"
            )

        self.reference_efficiency_entry = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_reference_efficiency,
            bootstyle=WARNING,
            variable=self.reference_efficiency,
            state=DISABLED,
        )
        self.reference_efficiency_entry.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew"
        )

        # Reference temperature
        self.reference_temperature_label = ttk.Label(self, text="Reference temperature")
        self.reference_temperature_label.grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )

        self.reference_temperature = tk.DoubleVar(value=25)
        self.reference_temperature_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.reference_temperature,
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

        self.thermal_coefficient = tk.DoubleVar(value=0.0056)
        self.thermal_coefficient_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.thermal_coefficient,
            state=DISABLED,
        )
        self.thermal_coefficient_entry.grid(
            row=8, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.thermal_coefficient_unit = ttk.Label(self, text="% / degree Celsius")
        self.thermal_coefficient_unit.grid(row=8, column=2, padx=10, pady=5, sticky="w")

    def populate_available_panels(self) -> None:
        """Populate the combo box with the set of avialable panels."""

        self.pv_panel_entry["values"] = ["m-Si"]


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

        self.columnconfigure(0, weight=2)  # First row has the header
        self.columnconfigure(1, weight=2)  # These rows have entries
        self.columnconfigure(2, weight=1)  # These rows have entries

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

        self.maximum_charge_unit = ttk.Label(self, text=f" 90%")
        self.maximum_charge_unit.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        def update_charge_labels():
            """Updates the maximum and minimum charge labels."""
            self.maximum_charge_unit.config(
                text=f"{' ' * (int(self.maximum_charge.get()) < 100)}"
                f"{' ' * (int(self.maximum_charge.get()) < 10)}"
                f"{abs(round(self.maximum_charge.get(), 2))}%"
            )
            self.minimum_charge_unit.config(
                text=f"{' ' * (int(self.minimum_charge.get()) < 100)}"
                f"{' ' * (int(self.minimum_charge.get()) < 10)}"
                f"{abs(round(self.minimum_charge.get(), 2))}%"
            )

        def scalar_maximum_charge(_):
            self.minimum_charge.set(
                min(self.minimum_charge.get(), self.maximum_charge.get())
            )
            update_charge_labels()

        self.maximum_charge_entry = ttk.Scale(
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
        self.maximum_charge_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Minimum charge
        self.minimum_charge_label = ttk.Label(self, text="Minimum charge")
        self.minimum_charge_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.minimum_charge = ttk.DoubleVar(self, 40, "minimum_charge")

        self.minimum_charge_unit = ttk.Label(self, text=f" 20%")
        self.minimum_charge_unit.grid(row=4, column=2, padx=10, pady=5, sticky="ew")

        def scalar_minimum_charge(_):
            self.maximum_charge.set(
                max(self.minimum_charge.get(), self.maximum_charge.get())
            )
            update_charge_labels()

        self.minimum_charge_entry = ttk.Scale(
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
        self.minimum_charge_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Leakage
        self.leakage_label = ttk.Label(self, text="Leakage")
        self.leakage_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.leakage = ttk.DoubleVar(self, 30, "leakage")
        self.leakage_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.leakage
        )
        self.leakage_entry.grid(
            row=5, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

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
            self, 95, "conversion_efficiency_in"
        )

        self.conversion_efficiency_in_unit = ttk.Label(self, text=f" 95%")
        self.conversion_efficiency_in_unit.grid(
            row=6, column=2, padx=10, pady=5, sticky="ew"
        )

        def scalar_conversion_efficiency_in(_):
            self.conversion_efficiency_in_unit.config(
                text=f"{' ' * (int(self.conversion_efficiency_in.get()) < 100)}"
                f"{' ' * (int(self.conversion_efficiency_in.get()) < 10)}"
                f"{abs(round(self.conversion_efficiency_in.get(), 2))}%"
            )

        self.conversion_efficiency_in_entry = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_conversion_efficiency_in,
            bootstyle=WARNING,
            variable=self.conversion_efficiency_in,
            # state=DISABLED
        )
        self.conversion_efficiency_in_entry.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew"
        )

        # Conversion efficiency out
        self.conversion_efficiency_out_label = ttk.Label(
            self, text="Conversion efficiency out"
        )
        self.conversion_efficiency_out_label.grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )

        self.conversion_efficiency_out = ttk.DoubleVar(
            self, 90, "conversion_efficiency_out"
        )

        self.conversion_efficiency_out_unit = ttk.Label(self, text=f" 90%")
        self.conversion_efficiency_out_unit.grid(
            row=7, column=2, padx=10, pady=5, sticky="ew"
        )

        def scalar_conversion_efficiency_out(_):
            self.conversion_efficiency_out_unit.config(
                text=f"{' ' * (int(self.conversion_efficiency_out.get()) < 100)}"
                f"{' ' * (int(self.conversion_efficiency_out.get()) < 10)}"
                f"{abs(round(self.conversion_efficiency_out.get(), 2))}%"
            )

        self.conversion_efficiency_out_entry = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=320,
            command=scalar_conversion_efficiency_out,
            bootstyle=WARNING,
            variable=self.conversion_efficiency_out,
            # state=DISABLED
        )
        self.conversion_efficiency_out_entry.grid(
            row=7, column=1, padx=10, pady=5, sticky="ew"
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

        self.lifetime_capacity_loss = ttk.DoubleVar(
            self, 0, "lifetime_capacity_loss"
        )

        self.lifetime_capacity_loss_unit = ttk.Label(self, text=f"  0%")
        self.lifetime_capacity_loss_unit.grid(
            row=9, column=2, padx=10, pady=5, sticky="ew"
        )

        def scalar_lifetime_capacity_loss(_):
            self.lifetime_capacity_loss_unit.config(
                text=f"{' ' * (int(self.lifetime_capacity_loss.get()) < 100)}"
                f"{' ' * (int(self.lifetime_capacity_loss.get()) < 10)}"
                f"{abs(round(self.lifetime_capacity_loss.get(), 2))}%"
            )

        self.lifetime_capacity_loss_entry = ttk.Scale(
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
        self.lifetime_capacity_loss_entry.grid(
            row=9, column=1, padx=10, pady=5, sticky="ew"
        )

        # C-rate discharging
        self.c_rate_discharging_label = ttk.Label(self, text="C-rate discharging")
        self.c_rate_discharging_label.grid(row=10, column=0, padx=10, pady=5, sticky="w")

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
        self.cost_entry = ttk.Entry(
            self, bootstyle=WARNING, textvariable=self.cost
        )
        self.cost_entry.grid(
            row=12, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

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
        self.annual_emissions_decrease_unit.grid(row=17, column=2, padx=10, pady=5, sticky="w")

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


class LoadFrame(ttk.Frame):
    """
    Represents the Load frame.

    Contains settings for load management.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Load frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class DieselFrame(ttk.Frame):
    """
    Represents the Diesel frame.

    Contains settings for diesel generators.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Diesel frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class GridFrame(ttk.Frame):
    """
    Represents the Grid frame.

    Contains settings for grid connection.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Grid frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class FinanceFrame(ttk.Frame):
    """
    Represents the Finance frame.

    Contains settings for financial analysis.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Finance frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class GHGFrame(ttk.Frame):
    """
    Represents the GHG frame.

    Contains settings for greenhouse gas emissions.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="GHGs frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class SystemFrame(ttk.Frame):
    """
    Represents the System frame.

    Contains settings for system configuration.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="System frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class DetailsWindow(tk.Toplevel):
    """
    Represents the details window.

    The details window contains tabs for inputting more precise information into the
    application.

    TODO: Update attributes.

    """

    def __init__(
        self,
    ) -> None:
        """
        Instantiate a :class:`DetailsWindow` instance.

        """

        super().__init__()

        self.title("CLOVER-GUI Details")

        self.geometry(DETAILS_GEOMETRY)

        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.details_label = ttk.Label(
            self, bootstyle=SECONDARY, text="Detailed settings", font="80"
        )
        self.details_label.grid(row=0, column=0, sticky="w", padx=60, pady=5)

        self.details_notebook = ttk.Notebook(self, bootstyle=f"{SECONDARY}")
        self.details_notebook.grid(
            row=1, column=0, sticky="nsew", padx=60, pady=5
        )  # Use grid

        style = ttk.Style()
        style.configure("TNotebook.Tab", width=int(self.winfo_screenwidth() / 8))

        self.solar_frame = SolarFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Solar", sticky="news")

        self.solar_frame = StorageFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Storage", sticky="news")

        self.solar_frame = LoadFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Load", sticky="news")

        self.solar_frame = DieselFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Diesel", sticky="news")

        self.solar_frame = GridFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Grid", sticky="news")

        self.solar_frame = FinanceFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Finance", sticky="news")

        self.solar_frame = GHGFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="GHGs", sticky="news")

        self.solar_frame = SystemFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="System", sticky="news")
