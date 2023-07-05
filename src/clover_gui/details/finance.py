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


__all__ = ("FinanceFrame",)


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

        # self.columnconfigure(0, weight=10)  # First row has the header
        # self.columnconfigure(1, weight=10)  # These rows have entries
        # self.columnconfigure(2, weight=1)  # These rows have entries
        # self.columnconfigure(3, weight=1)  # These rows have entries

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

        # Header
        self.header = ttk.Label(self, text="")
       
        # Discount Rate
        self.discount_rate_label = ttk.Label(self, text="Discount Rate")
        self.discount_rate_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.discount_rate = ttk.DoubleVar(self, "8.0")
        
        self.discount_rate_entry = ttk.Entry(
        self, bootstyle=DANGER, textvariable=self.discount_rate
        )
        self.discount_rate_entry.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        
        self.discount_rate_units_label = ttk.Label(self, text='%')
        self.discount_rate_units_label.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        
        # General O&M
        self.general_OM_label = ttk.Label(self, text="General O&M")
        self.general_OM_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.general_OM = ttk.DoubleVar(self, "0.0")
        
        self.general_OM_entry = ttk.Entry(
        self, bootstyle=DANGER, textvariable=self.general_OM
        )
        self.general_OM_entry.grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.general_OM_units_label = ttk.Label(self, text='$/year')
        self.general_OM_units_label.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # # Misc
        # self.misc_label = ttk.Label(self, text="Misc:")
        # self.misc_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        # Capacity Cost
        self.capacity_cost_label = ttk.Label(self, text="Misc Capacity Cost")
        self.capacity_cost_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.capacity_cost = ttk.DoubleVar(self, "0.0")

        self.capacity_cost_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.capacity_cost
        )
        self.capacity_cost_entry.grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.capacity_cost_units_label = ttk.Label(self, text='$/kWp')
        self.capacity_cost_units_label.grid(row=4, column=3, padx=10, pady=5, sticky="w")

        # Fixed Cost
        self.fixed_cost_label = ttk.Label(self, text="Misc Fixed Cost")
        self.fixed_cost_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.fixed_cost = ttk.DoubleVar(self, "0.0")

        self.fixed_cost_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.fixed_cost
        )
        self.fixed_cost_entry.grid(row=5, column=2, padx=10, pady=5, sticky="w")
        self.fixed_cost_units_label = ttk.Label(self, text='$')
        self.fixed_cost_units_label.grid(row=5, column=3, padx=10, pady=5, sticky="w")


        # BOS Cost
        self.bos_cost_label = ttk.Label(self, text="BOS Cost")
        self.bos_cost_label.grid(row=7, column=1, padx=10, pady=5, sticky="w")
        self.bos_cost = ttk.DoubleVar(self, "0.0")

        self.bos_cost_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.bos_cost
        )
        self.bos_cost_entry.grid(row=7, column=2, padx=10, pady=5, sticky="w")
        self.bos_cost_units_label = ttk.Label(self, text='$/kWp')
        self.bos_cost_units_label.grid(row=7, column=3, padx=10, pady=5, sticky="w")

        # BOS Cost Decrease
        self.bos_cost_decrease_label = ttk.Label(self, text="BOS Cost Decrease")
        self.bos_cost_decrease_label.grid(row=8, column=1, padx=10, pady=5, sticky="w")
        self.bos_cost_decrease = ttk.DoubleVar(self, "0.0")

        self.bos_cost_decrease_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.bos_cost_decrease
        )
        self.bos_cost_decrease_entry.grid(row=8, column=2, padx=10, pady=5, sticky="w")
        self.bos_cost_decrease_units_label = ttk.Label(self, text='%/year')
        self.bos_cost_decrease_units_label.grid(row=8, column=3, padx=10, pady=5, sticky="w")

        # # Diesel Fuel
        # self.diesel_fuel_label = ttk.Label(self, text="Diesel Fuel:")
        # self.diesel_fuel_label.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        # Diesel Fuel Cost
        self.diesel_fuel_cost_label = ttk.Label(self, text="Diesel Fuel Cost")
        self.diesel_fuel_cost_label.grid(row=10, column=1, padx=10, pady=5, sticky="w")
        self.diesel_fuel_cost = ttk.DoubleVar(self, "0.0")

        self.diesel_fuel_cost_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.diesel_fuel_cost
        )
        self.diesel_fuel_cost_entry.grid(row=10, column=2, padx=10, pady=5, sticky="w")
        self.diesel_fuel_cost_units_label = ttk.Label(self, text='$/litre')
        self.diesel_fuel_cost_units_label.grid(row=10, column=3, padx=10, pady=5, sticky="w")

        # Diesel Fuel Cost Decrease
        self.diesel_fuel_cost_decrease_label = ttk.Label(self, text="Diesel Fuel Cost Decrease")
        self.diesel_fuel_cost_decrease_label.grid(row=11, column=1, padx=10, pady=5, sticky="w")
        self.diesel_fuel_cost_decrease = ttk.DoubleVar(self, "0.0")

        self.diesel_fuel_cost_decrease_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.diesel_fuel_cost_decrease
        )
        self.diesel_fuel_cost_decrease_entry.grid(row=11, column=2, padx=10, pady=5, sticky="w")
        self.diesel_fuel_cost_decrease_units_label = ttk.Label(self, text='%/year')
        self.diesel_fuel_cost_decrease_units_label.grid(row=11, column=3, padx=10, pady=5, sticky="w")

        # # Grid
        # self.grid_label = ttk.Label(self, text="Grid:")
        # self.grid_label.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        # Grid Cost
        self.grid_cost_label = ttk.Label(self, text="Grid Cost")
        self.grid_cost_label.grid(row=13, column=1, padx=10, pady=5, sticky="w")
        self.grid_cost = ttk.DoubleVar(self, "0.0")

        self.grid_cost_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.grid_cost
        )
        self.grid_cost_entry.grid(row=13, column=2, padx=10, pady=5, sticky="w")
        self.grid_cost_units_label = ttk.Label(self, text='$/kWh')
        self.grid_cost_units_label.grid(row=13, column=3, padx=10, pady=5, sticky="w")
        
        # Distribution network
        self.distribution_network_infrastructure_cost_label = \
            ttk.Label(self, text="Distribution Network Infrastructure Cost")
        self.distribution_network_infrastructure_cost_label.grid(row=14, column=1, padx=10, pady=5, sticky="w")
        self.distribution_network_infrastructure_cost = ttk.DoubleVar(self, "0.0")

        self.distribution_network_infrastructure_cost_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.distribution_network_infrastructure_cost
        )
        self.distribution_network_infrastructure_cost_entry.grid(row=14, column=2, padx=10, pady=5, sticky="w")
        self.distribution_network_infrastructure_cost_units_label = ttk.Label(self, text='$')
        self.distribution_network_infrastructure_cost_units_label.grid(row=14, column=3, padx=10, pady=5, sticky="w")

        # Households
        # self.household_label = ttk.Label(self, text="Households")
        # self.household_label.grid(row=15, column=1, padx=10, pady=5, sticky="w")

        # Connection Cost
        self.connection_cost_label = ttk.Label(self, text="Connection Cost")
        self.connection_cost_label.grid(row=16, column=1, padx=10, pady=5, sticky="w")
        self.connection_cost = ttk.DoubleVar(self, "0.0")
        
        self.connection_cost_entry = ttk.Entry(
        self, bootstyle=DANGER, textvariable=self.connection_cost
        )
        self.connection_cost_entry.grid(row=16, column=2, padx=10, pady=5, sticky="w")
        self.connection_cost_units_label = ttk.Label(self, text='$/household')
        self.connection_cost_units_label.grid(row=16, column=3, padx=10, pady=5, sticky="w")

        # Inverter
        # self.inverter_label = ttk.Label(self, text="Inverter:")
        # self.inverter_label.grid(row=17, column=1, padx=10, pady=5, sticky="w")

        # Inverter Cost
        self.inverter_cost_label = ttk.Label(self, text="Inverter Cost")
        self.inverter_cost_label.grid(row=18, column=1, padx=10, pady=5, sticky="w")
        self.inverter_cost = ttk.DoubleVar(self, "0.0")

        self.inverter_cost_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.inverter_cost
        )
        self.inverter_cost_entry.grid(row=18, column=2, padx=10, pady=5, sticky="w")
        self.inverter_cost_units_label = ttk.Label(self, text='$/kW')
        self.inverter_cost_units_label.grid(row=18, column=3, padx=10, pady=5, sticky="w")

        # Inverter Cost Decrease
        self.inverter_cost_decrease_label = ttk.Label(self, text="Inverter Cost Decrease")
        self.inverter_cost_decrease_label.grid(row=19, column=1, padx=10, pady=5, sticky="w")
        self.inverter_cost_decrease = ttk.DoubleVar(self, "0.0")

        self.inverter_cost_decrease_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.inverter_cost_decrease
        )
        self.inverter_cost_decrease_entry.grid(row=19, column=2, padx=10, pady=5, sticky="w")
        self.inverter_cost_decrease_units_label = ttk.Label(self, text='%/year')
        self.inverter_cost_decrease_units_label.grid(row=19, column=3, padx=10, pady=5, sticky="w")

        # Inverter Lifetime
        self.inverter_lifetime_label = ttk.Label(self, text="Inverter Lifetime")
        self.inverter_lifetime_label.grid(row=20, column=1, padx=10, pady=5, sticky="w")
        self.inverter_lifetime = ttk.DoubleVar(self, "0.0")

        self.inverter_lifetime_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.inverter_lifetime
        )
        self.inverter_lifetime_entry.grid(row=20, column=2, padx=10, pady=5, sticky="w")
        self.inverter_lifetime_units_label = ttk.Label(self, text='years')
        self.inverter_lifetime_units_label.grid(row=20, column=3, padx=10, pady=5, sticky="w")

        # Inverter Size Increment
        self.inverter_size_increment_label = ttk.Label(self, text="Inverter Size Increment")
        self.inverter_size_increment_label.grid(row=21, column=1, padx=10, pady=5, sticky="w")
        self.inverter_size_increment = ttk.DoubleVar(self, "0.0")

        self.inverter_size_increment_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.inverter_size_increment
        )
        self.inverter_size_increment_entry.grid(row=21, column=2, padx=10, pady=5, sticky="w")
        self.inverter_size_increment_units_label = ttk.Label(self, text='kW')
        self.inverter_size_increment_units_label.grid(row=21, column=3, padx=10, pady=5, sticky="w")

        # Kerosene
        # self.kerosene_label = ttk.Label(self, text="Kerosene:")
        # self.kerosene_label.grid(row=20, column=1, padx=10, pady=5, sticky="w")

        # Kerosene Cost
        self.kerosene_cost_label = ttk.Label(self, text="Kerosene Cost")
        self.kerosene_cost_label.grid(row=22, column=1, padx=10, pady=5, sticky="w")
        self.kerosene_cost = ttk.DoubleVar(self, "0.0")
        
        self.kerosene_cost_entry = ttk.Entry(
            self, bootstyle=DANGER, textvariable=self.kerosene_cost
        )
        self.kerosene_cost_entry.grid(row=22, column=2, padx=10, pady=5, sticky="w")
        self.kerosene_cost_units_label = ttk.Label(self, text='$/hour')
        self.kerosene_cost_units_label.grid(row=22, column=3, padx=10, pady=5, sticky="w")

        

