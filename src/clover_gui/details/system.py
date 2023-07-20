#!/usr/bin/python3.10
########################################################################################
# system.py - The system module for CLOVER-GUI application.                            #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 11/07/2023                                                             #
# License: MIT, Open-source                                                            #
# For more Information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import ttkbootstrap as ttk

from clover.simulation.energy_system import Minigrid, Scenario
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


__all__ = ("SystemFrame",)


class SystemFrame(ttk.Frame):
    """
    Represents the System frame.

    Contains System inputs for the system.

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

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)
        self.columnconfigure(5, weight=1)

        # AC transmission efficiency
        self.ac_transmission_label = ttk.Label(self, text="AC transmission efficiency")
        self.ac_transmission_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.ac_transmission = ttk.DoubleVar(self, "92")

        def scalar_ac_transmission(_):
            self.ac_transmission.set(
                text=f"{' ' * (int(self.ac_transmission_slider.get()) < 100)}{self.ac_transmission_slider.get()} %"
            )

        self.ac_transmission_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_ac_transmission,
            bootstyle=WARNING,
            variable=self.ac_transmission,
        )
        self.ac_transmission_slider.grid(row=1, column=2, padx=10, pady=5, sticky="ew")

        def enter_ac_transmission(_):
            self.ac_transmission.set(self.ac_transmission_entry.get())
            self.ac_transmission_slider.set(self.ac_transmission.get())

        self.ac_transmission_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.ac_transmission,
        )

        self.ac_transmission_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        self.ac_transmission_entry.bind("<Return>", enter_ac_transmission)

        self.ac_transmission_unit = ttk.Label(self, text=f"%")
        self.ac_transmission_unit.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        # DC transmission efficiency
        self.dc_transmission_label = ttk.Label(self, text="DC transmission efficiency")
        self.dc_transmission_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.dc_transmission = ttk.DoubleVar(self, "96")

        def scalar_dc_transmission(_):
            self.dc_transmission.set(
                text=f"{' ' * (int(self.dc_transmission_slider.get()) < 100)}{self.dc_transmission_slider.get()} %"
            )

        self.dc_transmission_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_dc_transmission,
            bootstyle=WARNING,
            variable=self.dc_transmission,
        )

        self.dc_transmission_slider.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        def enter_dc_transmission(_):
            self.dc_transmission.set(self.dc_transmission_entry.get())
            self.dc_transmission_slider.set(self.dc_transmission.get())

        self.dc_transmission_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.dc_transmission,
        )

        self.dc_transmission_entry.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        self.dc_transmission_entry.bind("<Return>", enter_dc_transmission)

        self.dc_transmission_unit = ttk.Label(self, text=f"%")
        self.dc_transmission_unit.grid(row=2, column=4, padx=10, pady=5, sticky="ew")

        # # DC to AC conversion efficiency
        self.dc_to_ac_conversion_label = ttk.Label(
            self, text="DC to AC conversion efficiency"
        )
        self.dc_to_ac_conversion_label.grid(
            row=3, column=1, padx=10, pady=5, sticky="w"
        )

        self.dc_to_ac_conversion = ttk.DoubleVar(self, "97")

        def scalar_dc_to_ac_conversion(_):
            self.dc_to_ac_conversion.set(
                text=f"{' ' * (int(self.dc_to_ac_conversion_slider.get()) < 100)}{self.dc_to_ac_conversion_slider.get()} %"
            )

        self.dc_to_ac_conversion_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_dc_to_ac_conversion,
            bootstyle=WARNING,
            variable=self.dc_to_ac_conversion,
        )

        self.dc_to_ac_conversion_slider.grid(
            row=3, column=2, padx=10, pady=5, sticky="ew"
        )

        def enter_dc_to_ac_conversion(_):
            self.dc_to_ac_conversion.set(self.dc_to_ac_conversion_entry.get())
            self.dc_to_ac_conversion_slider.set(self.dc_to_ac_conversion.get())

        self.dc_to_ac_conversion_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.dc_to_ac_conversion,
        )

        self.dc_to_ac_conversion_entry.grid(
            row=3, column=3, padx=10, pady=5, sticky="ew"
        )
        self.dc_to_ac_conversion_entry.bind("<Return>", enter_dc_to_ac_conversion)

        self.dc_to_ac_conversion_unit = ttk.Label(self, text=f"%")
        self.dc_to_ac_conversion_unit.grid(
            row=3, column=4, padx=10, pady=5, sticky="ew"
        )

        # # DC to DC conversion efficiency
        self.dc_to_dc_conversion_label = ttk.Label(
            self, text="DC to DC conversion efficiency"
        )
        self.dc_to_dc_conversion_label.grid(
            row=4, column=1, padx=10, pady=5, sticky="w"
        )

        self.dc_to_dc_conversion = ttk.DoubleVar(self, "95")

        def scalar_dc_to_dc_conversion(_):
            self.dc_to_dc_conversion.set(
                text=f"{' ' * (int(self.dc_to_dc_conversion_slider.get()) < 100)}{self.dc_to_dc_conversion_slider.get()} %"
            )

        self.dc_to_dc_conversion_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_dc_to_dc_conversion,
            bootstyle=WARNING,
            variable=self.dc_to_dc_conversion,
        )

        self.dc_to_dc_conversion_slider.grid(
            row=4, column=2, padx=10, pady=5, sticky="ew"
        )

        def enter_dc_to_dc_conversion(_):
            self.dc_to_dc_conversion.set(self.dc_to_dc_conversion_entry.get())
            self.dc_to_dc_conversion_slider.set(self.dc_to_dc_conversion.get())

        self.dc_to_dc_conversion_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.dc_to_dc_conversion,
        )

        self.dc_to_dc_conversion_entry.grid(
            row=4, column=3, padx=10, pady=5, sticky="ew"
        )
        self.dc_to_dc_conversion_entry.bind("<Return>", enter_dc_to_dc_conversion)

        self.dc_to_dc_conversion_unit = ttk.Label(self, text=f"%")
        self.dc_to_dc_conversion_unit.grid(
            row=4, column=4, padx=10, pady=5, sticky="ew"
        )

        # # AC to DC conversion efficiency
        self.ac_to_dc_conversion_label = ttk.Label(
            self, text="AC to DC conversion efficiency"
        )
        self.ac_to_dc_conversion_label.grid(
            row=5, column=1, padx=10, pady=5, sticky="w"
        )

        self.ac_to_dc_conversion = ttk.DoubleVar(self, "90")

        def scalar_ac_to_dc_conversion(_):
            self.ac_to_dc_conversion.set(
                text=f"{' ' * (int(self.ac_to_dc_conversion_slider.get()) < 100)}{self.ac_to_dc_conversion_slider.get()} %"
            )

        self.ac_to_dc_conversion_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_ac_to_dc_conversion,
            bootstyle=WARNING,
            variable=self.ac_to_dc_conversion,
        )

        self.ac_to_dc_conversion_slider.grid(
            row=5, column=2, padx=10, pady=5, sticky="ew"
        )

        def enter_ac_to_dc_conversion(_):
            self.ac_to_dc_conversion.set(self.ac_to_dc_conversion_entry.get())
            self.ac_to_dc_conversion_slider.set(self.ac_to_dc_conversion.get())

        self.ac_to_dc_conversion_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.ac_to_dc_conversion,
        )

        self.ac_to_dc_conversion_entry.grid(
            row=5, column=3, padx=10, pady=5, sticky="ew"
        )
        self.ac_to_dc_conversion_entry.bind("<Return>", enter_ac_to_dc_conversion)

        self.ac_to_dc_conversion_unit = ttk.Label(self, text=f"%")

        self.ac_to_dc_conversion_unit.grid(
            row=5, column=4, padx=10, pady=5, sticky="ew"
        )

        # # AC to AC conversion efficiency
        self.ac_to_ac_conversion_label = ttk.Label(
            self, text="AC to AC conversion efficiency"
        )
        self.ac_to_ac_conversion_label.grid(
            row=6, column=1, padx=10, pady=5, sticky="w"
        )

        self.ac_to_ac_conversion = ttk.DoubleVar(self, "98")

        def scalar_ac_to_ac_conversion(_):
            self.ac_to_ac_conversion.set(
                text=f"{' ' * (int(self.ac_to_ac_conversion_slider.get()) < 100)}{self.ac_to_ac_conversion_slider.get()} %"
            )

        self.ac_to_ac_conversion_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_ac_to_ac_conversion,
            bootstyle=WARNING,
            variable=self.ac_to_ac_conversion,
        )

        self.ac_to_ac_conversion_slider.grid(
            row=6, column=2, padx=10, pady=5, sticky="ew"
        )

        def enter_ac_to_ac_conversion(_):
            self.ac_to_ac_conversion.set(self.ac_to_ac_conversion_entry.get())
            self.ac_to_ac_conversion_slider.set(self.ac_to_ac_conversion.get())

        self.ac_to_ac_conversion_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.ac_to_ac_conversion,
        )

        self.ac_to_ac_conversion_entry.grid(
            row=6, column=3, padx=10, pady=5, sticky="ew"
        )
        self.ac_to_ac_conversion_entry.bind("<Return>", enter_ac_to_ac_conversion)

        self.ac_to_ac_conversion_unit = ttk.Label(self, text=f"%")
        self.ac_to_ac_conversion_unit.grid(
            row=6, column=4, padx=10, pady=5, sticky="ew"
        )

        # Select battery
        self.battery_label = ttk.Label(self, text="Battery")
        self.battery_label.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        self.battery = ttk.Combobox(
            self,
            values=["default_battery"],
            state="readonly",
            bootstyle=WARNING,
        )
        self.battery.current(0)
        self.battery.grid(row=7, column=2, padx=10, pady=5, sticky="ew")

        # Select diesel generator
        self.diesel_generator_label = ttk.Label(self, text="Diesel generator")
        self.diesel_generator_label.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        self.diesel_generator = ttk.Combobox(
            self,
            values=["default_diesel"],
            state="readonly",
            bootstyle=WARNING,
        )
        self.diesel_generator.current(0)
        self.diesel_generator.grid(row=8, column=2, padx=10, pady=5, sticky="ew")

        # Select PV panel
        self.pv_panel_label = ttk.Label(self, text="PV panel")
        self.pv_panel_label.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        self.pv_panel = ttk.Combobox(
            self,
            values=["default_pv"],
            state="readonly",
            bootstyle=WARNING,
        )
        self.pv_panel.current(0)
        self.pv_panel.grid(row=9, column=2, padx=10, pady=5, sticky="ew")

        # Select AC heat exchanger
        self.ac_heat_exchanger_label = ttk.Label(self, text="AC heat exchanger")
        self.ac_heat_exchanger_label.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        self.ac_heat_exchanger = ttk.Combobox(
            self,
            values=["default_heat_exchanger"],
            state="readonly",
            bootstyle=WARNING,
        )
        self.ac_heat_exchanger.current(0)
        self.ac_heat_exchanger.grid(row=10, column=2, padx=10, pady=5, sticky="ew")

    def set_system(self, minigrid: Minigrid, scenarios: list[Scenario]) -> None:
        """
        Sets the scenarios on the system frame.

        """

        self.ac_transmission
