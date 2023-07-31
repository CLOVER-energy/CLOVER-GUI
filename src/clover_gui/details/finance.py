#!/usr/bin/python3.10
########################################################################################
# finance.py - The finance module for CLOVER-GUI application.                          #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################


import tkinter as tk

import ttkbootstrap as ttk

from clover.impact.finance import *
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


__all__ = ("FinanceFrame",)

# Infrastructure costs:
#   Keyword for the infrastructure costs.
_INFRASTRUCTURE_COSTS: str = "infrastructure_costs"


class FinanceFrame(ttk.Frame):
    """
    Represents the Finance frame.

    Contains financial inputs for the system.

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
        self.rowconfigure(17, weight=1)
        self.rowconfigure(18, weight=1)
        self.rowconfigure(19, weight=1)
        self.rowconfigure(20, weight=1)
        self.rowconfigure(21, weight=1)
        self.rowconfigure(22, weight=1)
        self.rowconfigure(23, weight=1)

        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=2)
        # self.columnconfigure(3, weight=2)
        # self.columnconfigure(4, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        # Header
        self.header = ttk.Label(self, text="")

        # Discount Rate
        self.discount_rate_label = ttk.Label(self, text="Discount Rate")
        self.discount_rate_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.discount_rate = ttk.DoubleVar(self, "8.0")

        def scalar_discount_rate(_):
            self.discount_rate.set(max(min(self.discount_rate.get(), 100), 0))
            self.discount_rate_entry.update()

        self.discount_rate_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_discount_rate,
            # bootstyle=WARNING,
            variable=self.discount_rate,
        )
        self.discount_rate_slider.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        def enter_discount_rate(_):
            self.discount_rate.set(self.discount_rate_entry.get())
            self.discount_rate_slider.set(self.discount_rate.get())

        self.discount_rate_entry = ttk.Entry(
            self,
            # bootstyle=WARNING,
            textvariable=self.discount_rate,
        )

        self.discount_rate_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        self.discount_rate_entry.bind("<Return>", enter_discount_rate)

        self.discount_rate_unit = ttk.Label(self, text=f"%")
        self.discount_rate_unit.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        # General O&M
        self.general_om_label = ttk.Label(self, text="General O&M")
        self.general_om_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.general_om = ttk.DoubleVar(self, "0.0")

        self.general_om_entry = ttk.Entry(
            self,
            # bootstyle=DANGER,
            textvariable=self.general_om,
        )
        self.general_om_entry.grid(
            row=2, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.general_om_units_label = ttk.Label(self, text="$/year")
        self.general_om_units_label.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # # Misc
        # self.misc_frame = ttk.Labelframe(self, text="Misc. Costs", bootstyle=PRIMARY)
        # self.misc_frame.grid(
        #     row=3, column=1, columnspan=3, padx=10, pady=5, sticky="ew"
        # )
        # self.misc_frame.columnconfigure(0, weight=1)
        # self.misc_frame.columnconfigure(1, weight=2)
        # self.misc_frame.columnconfigure(2, weight=2, pad=20)

        # Capacity Cost
        self.capacity_cost_label = ttk.Label(self, text="Misc. Capacity Cost")
        self.capacity_cost_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.capacity_cost = ttk.DoubleVar(self, "0.0")

        self.capacity_cost_entry = ttk.Entry(
            self,
            textvariable=self.capacity_cost,
        )
        self.capacity_cost_entry.grid(
            row=3, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )

        self.capacity_cost_units_label = ttk.Label(self, text="$/kWp")
        self.capacity_cost_units_label.grid(
            row=3, column=3, padx=10, pady=5, sticky="w"
        )

        # Fixed Cost
        self.fixed_cost_label = ttk.Label(self, text="Misc. Fixed Cost")
        self.fixed_cost_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.fixed_cost = ttk.DoubleVar(self, "0.0")

        self.fixed_cost_entry = ttk.Entry(
            self,
            # bootstyle=PRIMARY,
            textvariable=self.fixed_cost,
        )

        self.fixed_cost_entry.grid(
            row=4, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.fixed_cost_units_label = ttk.Label(self, text="$")
        self.fixed_cost_units_label.grid(row=4, column=3, padx=10, pady=5, sticky="w")

        # BOS Cost
        self.bos_cost_label = ttk.Label(self, text="BOS Cost")
        self.bos_cost_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.bos_cost = ttk.DoubleVar(self, "0.0")

        self.bos_cost_entry = ttk.Entry(
            self,
            # bootstyle=DANGER,
            textvariable=self.bos_cost,
        )
        self.bos_cost_entry.grid(
            row=5, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.bos_cost_units_label = ttk.Label(self, text="$/kWp")
        self.bos_cost_units_label.grid(row=5, column=3, padx=10, pady=5, sticky="w")

        # BOS Cost Decrease
        self.bos_cost_decrease_label = ttk.Label(self, text="BOS Cost Decrease")
        self.bos_cost_decrease_label.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.bos_cost_decrease = ttk.DoubleVar(self, "0.0")

        self.bos_cost_decrease_entry = ttk.Entry(
            self,
            # bootstyle=DANGER,
            textvariable=self.bos_cost_decrease,
        )
        self.bos_cost_decrease_entry.grid(
            row=6, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.bos_cost_decrease_units_label = ttk.Label(self, text="%/year")
        self.bos_cost_decrease_units_label.grid(
            row=6, column=3, padx=10, pady=5, sticky="w"
        )

        # # Diesel Fuel
        # self = ttk.Labelframe(
        #     self, text="Diesel Fuel", bootstyle=DANGER
        # )
        # self.grid(
        #     row=6, column=1, columnspan=3, padx=10, pady=5, sticky="ew"
        # )

        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=2)
        # self.columnconfigure(2, weight=2, pad=30)

        # Diesel Fuel Cost
        self.diesel_fuel_cost_label = ttk.Label(self, text="Diesel Fuel Cost")
        self.diesel_fuel_cost_label.grid(row=7, column=1, padx=10, pady=5, sticky="w")
        self.diesel_fuel_cost = ttk.DoubleVar(self, "0.0")

        self.diesel_fuel_cost_entry = ttk.Entry(
            self,
            # bootstyle=DANGER,
            textvariable=self.diesel_fuel_cost,
        )
        self.diesel_fuel_cost_entry.grid(
            row=7, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.diesel_fuel_cost_units_label = ttk.Label(self, text="$/litre")
        self.diesel_fuel_cost_units_label.grid(
            row=7, column=3, padx=10, pady=5, sticky="w"
        )

        # Diesel Fuel Cost Decrease
        self.diesel_fuel_cost_decrease_label = ttk.Label(
            self, text="Diesel Fuel Cost Decrease"
        )
        self.diesel_fuel_cost_decrease_label.grid(
            row=8, column=1, padx=10, pady=5, sticky="w"
        )
        self.diesel_fuel_cost_decrease = ttk.DoubleVar(self, "0.0")

        self.diesel_fuel_cost_decrease_entry = ttk.Entry(
            self,
            # bootstyle=DANGER,
            textvariable=self.diesel_fuel_cost_decrease,
        )
        self.diesel_fuel_cost_decrease_entry.grid(
            row=8, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.diesel_fuel_cost_decrease_units_label = ttk.Label(self, text="%/year")
        self.diesel_fuel_cost_decrease_units_label.grid(
            row=8, column=3, padx=10, pady=5, sticky="w"
        )

        # # Grid
        # self = ttk.Labelframe(self, text="Grid", bootstyle=SUCCESS)
        # self.grid(
        #     row=7, column=1, columnspan=3, padx=10, pady=5, sticky="ew"
        # )

        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=3)
        # self.columnconfigure(2, weight=3, pad=110)

        # Grid Cost
        self.grid_cost_label = ttk.Label(self, text="Grid Cost")
        self.grid_cost_label.grid(row=9, column=1, padx=10, pady=5, sticky="w")
        self.grid_cost = ttk.DoubleVar(self, "0.0")

        self.grid_cost_entry = ttk.Entry(self, textvariable=self.grid_cost)
        self.grid_cost_entry.grid(
            row=9, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.grid_cost_units_label = ttk.Label(self, text="$/kWh")
        self.grid_cost_units_label.grid(row=8, column=3, padx=10, pady=5, sticky="w")

        # Distribution network
        self.distribution_network_infrastructure_cost_label = ttk.Label(
            self, text="Distribution Network Infrastructure Cost"
        )
        self.distribution_network_infrastructure_cost_label.grid(
            row=10, column=1, padx=10, pady=5, sticky="w"
        )
        self.distribution_network_infrastructure_cost = ttk.DoubleVar(self, "0.0")

        self.distribution_network_infrastructure_cost_entry = ttk.Entry(
            self,
            # bootstyle=SUCCESS,
            textvariable=self.distribution_network_infrastructure_cost,
            state=DISABLED,
        )
        self.distribution_network_infrastructure_cost_entry.grid(
            row=10, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.distribution_network_infrastructure_cost_units_label = ttk.Label(
            self, text="$"
        )
        self.distribution_network_infrastructure_cost_units_label.grid(
            row=10, column=3, padx=10, pady=5, sticky="w"
        )

        # # Households
        # self = ttk.Labelframe(
        #     self, text="Households", bootstyle=PRIMARY
        # )
        # self.grid(
        #     row=8, column=1, columnspan=3, padx=10, pady=5, sticky="ew"
        # )

        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=3)
        # self.columnconfigure(2, weight=2, pad=5)

        # Connection Cost
        self.connection_cost_label = ttk.Label(self, text="Connection Cost")
        self.connection_cost_label.grid(row=11, column=1, padx=10, pady=5, sticky="w")
        self.connection_cost = ttk.DoubleVar(self, "0.0")

        self.connection_cost_entry = ttk.Entry(
            self,
            # bootstyle=PRIMARY,
            textvariable=self.connection_cost,
        )
        self.connection_cost_entry.grid(
            row=11, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.connection_cost_units_label = ttk.Label(self, text="$/household")
        self.connection_cost_units_label.grid(
            row=11, column=3, padx=10, pady=5, sticky="w"
        )

        # # Inverter
        # self = ttk.Labelframe(
        #     self, text="Inverter", bootstyle=WARNING
        # )
        # self.grid(
        #     row=9, column=1, columnspan=3, padx=10, pady=5, sticky="ew"
        # )

        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=2)
        # self.columnconfigure(2, weight=2, pad=30)

        # Inverter Cost
        self.inverter_cost_label = ttk.Label(self, text="Inverter Cost")
        self.inverter_cost_label.grid(row=12, column=1, padx=10, pady=5, sticky="w")
        self.inverter_cost = ttk.DoubleVar(self, "0.0")

        self.inverter_cost_entry = ttk.Entry(
            self,
            # bootstyle=WARNING,
            textvariable=self.inverter_cost,
        )
        self.inverter_cost_entry.grid(
            row=12, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.inverter_cost_units_label = ttk.Label(self, text="$/kW")
        self.inverter_cost_units_label.grid(
            row=12, column=3, padx=10, pady=5, sticky="w"
        )

        # Inverter Cost Decrease
        self.inverter_cost_decrease_label = ttk.Label(
            self, text="Inverter Cost Decrease"
        )
        self.inverter_cost_decrease_label.grid(
            row=13, column=1, padx=10, pady=5, sticky="w"
        )
        self.inverter_cost_decrease = ttk.DoubleVar(self, "0.0")

        self.inverter_cost_decrease_entry = ttk.Entry(
            self,
            # bootstyle=WARNING,
            textvariable=self.inverter_cost_decrease,
        )
        self.inverter_cost_decrease_entry.grid(
            row=13, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )
        self.inverter_cost_decrease_units_label = ttk.Label(self, text="%/year")
        self.inverter_cost_decrease_units_label.grid(
            row=13, column=3, padx=10, pady=5, sticky="w"
        )

        # # Inverter Lifetime
        # self.inverter_lifetime_label = ttk.Label(self, text="Inverter Lifetime")
        # self.inverter_lifetime_label.grid(row=20, column=1, padx=10, pady=5, sticky="w")
        # self.inverter_lifetime = ttk.DoubleVar(self, "0.0")

        # self.inverter_lifetime_entry = ttk.Entry(
        #     self, bootstyle=DANGER, textvariable=self.inverter_lifetime
        # )
        # self.inverter_lifetime_entry.grid(row=20, column=2, padx=10, pady=5, sticky="ew")
        # self.inverter_lifetime_units_label = ttk.Label(self, text="years")
        # self.inverter_lifetime_units_label.grid(
        #     row=20, column=3, padx=10, pady=5, sticky="w"
        # )

        # # Inverter Size Increment
        # self.inverter_size_increment_label = ttk.Label(
        #     self, text="Inverter Size Increment"
        # )
        # self.inverter_size_increment_label.grid(
        #     row=21, column=1, padx=10, pady=5, sticky="w"
        # )
        # self.inverter_size_increment = ttk.DoubleVar(self, "0.0")

        # self.inverter_size_increment_entry = ttk.Entry(
        #     self, bootstyle=DANGER, textvariable=self.inverter_size_increment
        # )
        # self.inverter_size_increment_entry.grid(
        #     row=21, column=2, padx=10, pady=5, sticky="ew"
        # )
        # self.inverter_size_increment_units_label = ttk.Label(self, text="kW")
        # self.inverter_size_increment_units_label.grid(
        #     row=21, column=3, padx=10, pady=5, sticky="w"
        # )

        # # Kerosene
        # self = ttk.Labelframe(
        #     self, text="Kerosene", bootstyle=DANGER
        # )
        # self.grid(
        #     row=10, column=1, columnspan=3, padx=10, pady=5, sticky="ew"
        # )

        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=2)
        # self.columnconfigure(2, weight=1, pad=82)

        # Kerosene Cost
        self.kerosene_cost_label = ttk.Label(self, text="Kerosene Cost")
        self.kerosene_cost_label.grid(row=14, column=1, padx=10, pady=5, sticky="w")
        self.kerosene_cost = ttk.DoubleVar(self, "0.0")

        self.kerosene_cost_entry = ttk.Entry(self, textvariable=self.kerosene_cost)
        self.kerosene_cost_entry.grid(
            row=14, column=2, padx=10, pady=5, ipadx=80, sticky="ew"
        )

        self.kerosene_cost_units_label = ttk.Label(self, text="$/hour")
        self.kerosene_cost_units_label.grid(
            row=14, column=3, padx=10, pady=5, sticky="w"
        )

    def set_finance_inputs(
        self, finance_inputs: dict[str, float | dict[str, float]], logger: Logger
    ) -> None:
        """
        Sets the finance inputs.

        :param: finance_inputs
            The finance inputs information.

        """

        self.discount_rate.set(finance_inputs[DISCOUNT_RATE])
        self.discount_rate_entry.update()

        self.general_om.set(finance_inputs[OM][COST])
        self.general_om_entry.update()

        # Misc.
        try:
            self.capacity_cost.set(
                finance_inputs[ImpactingComponent.MISC.value][CAPACITY_COST]
            )
        except KeyError:
            logger.error(
                "Using misc cost without capacity or fixed keywords will be deprecated."
            )
            self.capacity_cost.set(
                finance_inputs[ImpactingComponent.MISC.value].get(COST, 0)
            )

        self.capacity_cost_entry.update()

        try:
            self.fixed_cost.set(
                finance_inputs[ImpactingComponent.MISC.value][FIXED_COST]
            )
        except KeyError:
            logger.error(
                "Using misc cost without capacity or fixed keywords will be deprecated."
            )
            self.fixed_cost.set(
                finance_inputs[ImpactingComponent.MISC.value].get(COST, 0)
            )

        self.fixed_cost_entry.update()

        # BOS
        self.bos_cost.set(finance_inputs[ImpactingComponent.BOS.value][COST])
        self.bos_cost_entry.update()

        self.bos_cost_decrease.set(
            finance_inputs[ImpactingComponent.BOS.value][COST_DECREASE]
        )
        self.bos_cost_decrease_entry.update()

        # Diesel
        self.diesel_fuel_cost.set(
            finance_inputs[ImpactingComponent.DIESEL_FUEL.value][COST]
        )
        self.diesel_fuel_cost_entry.update()

        self.diesel_fuel_cost_decrease.set(
            finance_inputs[ImpactingComponent.DIESEL_FUEL.value][COST_DECREASE]
        )
        self.diesel_fuel_cost_decrease_entry.update()

        # Grid
        self.grid_cost.set(finance_inputs[ImpactingComponent.GRID.value][COST])
        self.grid_cost_entry.update()

        self.distribution_network_infrastructure_cost.set(
            finance_inputs[ImpactingComponent.GRID.value].get(_INFRASTRUCTURE_COSTS, 0)
        )
        self.distribution_network_infrastructure_cost_entry.update()

        # Household
        self.connection_cost.set(
            finance_inputs[ImpactingComponent.HOUSEHOLDS.value][CONNECTION_COST]
        )
        self.connection_cost_entry.update()

        # Inverter
        self.inverter_cost.set(finance_inputs[ImpactingComponent.INVERTER.value][COST])
        self.inverter_cost_entry.update()

        self.inverter_cost_decrease.set(
            finance_inputs[ImpactingComponent.INVERTER.value][COST_DECREASE]
        )
        self.inverter_cost_decrease_entry.update()

        # Kerosene
        self.kerosene_cost.set(finance_inputs[ImpactingComponent.KEROSENE.value][COST])
        self.kerosene_cost_entry.update()
