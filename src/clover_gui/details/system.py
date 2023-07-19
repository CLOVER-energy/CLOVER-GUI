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
        self.AC_transmission_label = ttk.Label(self, text="AC transmission efficiency")
        self.AC_transmission_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.AC_transmission = ttk.DoubleVar(self, "92")

        def scalar_AC_transmission(_):
            self.AC_transmission.set(
                text=f"{' ' * (int(self.AC_transmission_slider.get()) < 100)}{self.AC_transmission_slider.get()} %"
            )

        self.AC_transmission_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_AC_transmission,
            bootstyle=WARNING,
            variable=self.AC_transmission
        )
        self.AC_transmission_slider.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        
        def enter_AC_transmission(_):
            self.AC_transmission.set(self.AC_transmission_entry.get())
            self.AC_transmission_slider.set(self.AC_transmission.get())

        self.AC_transmission_entry = ttk.Entry(
            self, 
            bootstyle=WARNING,
            textvariable=self.AC_transmission,
            )
        
        self.AC_transmission_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        self.AC_transmission_entry.bind("<Return>", enter_AC_transmission)

        self.AC_transmission_unit = ttk.Label(self, 
            text=f"%"
            )
        self.AC_transmission_unit.grid(
            row=1, column=4, padx=10, pady=5, sticky="ew"
        )        
        
        # DC transmission efficiency
        self.DC_transmission_label = ttk.Label(self, text="DC transmission efficiency")
        self.DC_transmission_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.DC_transmission = ttk.DoubleVar(self, "96")

        def scalar_DC_transmission(_):
            self.DC_transmission.set(
                text=f"{' ' * (int(self.DC_transmission_slider.get()) < 100)}{self.DC_transmission_slider.get()} %"
            )

        self.DC_transmission_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_DC_transmission,
            bootstyle=WARNING,
            variable=self.DC_transmission
        )

        self.DC_transmission_slider.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        def enter_DC_transmission(_):
            self.DC_transmission.set(self.DC_transmission_entry.get())
            self.DC_transmission_slider.set(self.DC_transmission.get())

        self.DC_transmission_entry = ttk.Entry(
            self, 
            bootstyle=WARNING,
            textvariable=self.DC_transmission,
            )

        self.DC_transmission_entry.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        self.DC_transmission_entry.bind("<Return>", enter_DC_transmission)

        self.DC_transmission_unit = ttk.Label(self,
            text=f"%"
            )
        self.DC_transmission_unit.grid(
            row=2, column=4, padx=10, pady=5, sticky="ew"
        )
        
        # # DC to AC conversion efficiency
        self.DC_to_AC_conversion_label = ttk.Label(self, text="DC to AC conversion efficiency")
        self.DC_to_AC_conversion_label.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.DC_to_AC_conversion = ttk.DoubleVar(self, "97")
        
        def scalar_DC_to_AC_conversion(_):
            self.DC_to_AC_conversion.set(
                text=f"{' ' * (int(self.DC_to_AC_conversion_slider.get()) < 100)}{self.DC_to_AC_conversion_slider.get()} %"
            )
        
        self.DC_to_AC_conversion_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_DC_to_AC_conversion,
            bootstyle=WARNING,
            variable=self.DC_to_AC_conversion
        )

        self.DC_to_AC_conversion_slider.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        def enter_DC_to_AC_conversion(_):
            self.DC_to_AC_conversion.set(self.DC_to_AC_conversion_entry.get())
            self.DC_to_AC_conversion_slider.set(self.DC_to_AC_conversion.get())

        self.DC_to_AC_conversion_entry = ttk.Entry(
            self, 
            bootstyle=WARNING,
            textvariable=self.DC_to_AC_conversion,
            )
        
        self.DC_to_AC_conversion_entry.grid(row=3, column=3, padx=10, pady=5, sticky="ew")
        self.DC_to_AC_conversion_entry.bind("<Return>", enter_DC_to_AC_conversion)

        self.DC_to_AC_conversion_unit = ttk.Label(self,
            text=f"%"
            )
        self.DC_to_AC_conversion_unit.grid(
            row=3, column=4, padx=10, pady=5, sticky="ew"
        )

        # # DC to DC conversion efficiency
        self.DC_to_DC_conversion_label = ttk.Label(self, text="DC to DC conversion efficiency")
        self.DC_to_DC_conversion_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.DC_to_DC_conversion = ttk.DoubleVar(self, "95")

        def scalar_DC_to_DC_conversion(_):
            self.DC_to_DC_conversion.set(
                text=f"{' ' * (int(self.DC_to_DC_conversion_slider.get()) < 100)}{self.DC_to_DC_conversion_slider.get()} %"
            )

        self.DC_to_DC_conversion_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_DC_to_DC_conversion,
            bootstyle=WARNING,
            variable=self.DC_to_DC_conversion
        )

        self.DC_to_DC_conversion_slider.grid(row=4, column=2, padx=10, pady=5, sticky="ew")

        def enter_DC_to_DC_conversion(_):
            self.DC_to_DC_conversion.set(self.DC_to_DC_conversion_entry.get())
            self.DC_to_DC_conversion_slider.set(self.DC_to_DC_conversion.get())

        self.DC_to_DC_conversion_entry = ttk.Entry(
            self, 
            bootstyle=WARNING,
            textvariable=self.DC_to_DC_conversion,
            )
        
        self.DC_to_DC_conversion_entry.grid(row=4, column=3, padx=10, pady=5, sticky="ew")
        self.DC_to_DC_conversion_entry.bind("<Return>", enter_DC_to_DC_conversion)

        self.DC_to_DC_conversion_unit = ttk.Label(self,
            text=f"%"
            )
        self.DC_to_DC_conversion_unit.grid(
            row=4, column=4, padx=10, pady=5, sticky="ew"
        )

        # # AC to DC conversion efficiency
        self.AC_to_DC_conversion_label = ttk.Label(self, text="AC to DC conversion efficiency")
        self.AC_to_DC_conversion_label.grid(row=5, column=1, padx=10, pady=5, sticky="w")

        self.AC_to_DC_conversion = ttk.DoubleVar(self, "90")

        def scalar_AC_to_DC_conversion(_):
            self.AC_to_DC_conversion.set(
                text=f"{' ' * (int(self.AC_to_DC_conversion_slider.get()) < 100)}{self.AC_to_DC_conversion_slider.get()} %"
            )

        self.AC_to_DC_conversion_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_AC_to_DC_conversion,
            bootstyle=WARNING,
            variable=self.AC_to_DC_conversion
        )

        self.AC_to_DC_conversion_slider.grid(row=5, column=2, padx=10, pady=5, sticky="ew")

        def enter_AC_to_DC_conversion(_):
            self.AC_to_DC_conversion.set(self.AC_to_DC_conversion_entry.get())
            self.AC_to_DC_conversion_slider.set(self.AC_to_DC_conversion.get())
        
        self.AC_to_DC_conversion_entry = ttk.Entry(
            self, 
            bootstyle=WARNING,
            textvariable=self.AC_to_DC_conversion,
            )
        
        self.AC_to_DC_conversion_entry.grid(row=5, column=3, padx=10, pady=5, sticky="ew")
        self.AC_to_DC_conversion_entry.bind("<Return>", enter_AC_to_DC_conversion)

        self.AC_to_DC_conversion_unit = ttk.Label(self,
            text=f"%"
            )
        
        self.AC_to_DC_conversion_unit.grid(
            row=5, column=4, padx=10, pady=5, sticky="ew"
        )

        # # AC to AC conversion efficiency
        self.AC_to_AC_conversion_label = ttk.Label(self, text="AC to AC conversion efficiency")
        self.AC_to_AC_conversion_label.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        self.AC_to_AC_conversion = ttk.DoubleVar(self, "98")

        def scalar_AC_to_AC_conversion(_):
            self.AC_to_AC_conversion.set(
                text=f"{' ' * (int(self.AC_to_AC_conversion_slider.get()) < 100)}{self.AC_to_AC_conversion_slider.get()} %"
            )

        self.AC_to_AC_conversion_slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient=ttk.HORIZONTAL,
            length=320,
            command=scalar_AC_to_AC_conversion,
            bootstyle=WARNING,
            variable=self.AC_to_AC_conversion
        )

        self.AC_to_AC_conversion_slider.grid(row=6, column=2, padx=10, pady=5, sticky="ew")

        def enter_AC_to_AC_conversion(_):
            self.AC_to_AC_conversion.set(self.AC_to_AC_conversion_entry.get())
            self.AC_to_AC_conversion_slider.set(self.AC_to_AC_conversion.get())

        self.AC_to_AC_conversion_entry = ttk.Entry(
            self, 
            bootstyle=WARNING,
            textvariable=self.AC_to_AC_conversion,
            )
        
        self.AC_to_AC_conversion_entry.grid(row=6, column=3, padx=10, pady=5, sticky="ew")
        self.AC_to_AC_conversion_entry.bind("<Return>", enter_AC_to_AC_conversion)

        self.AC_to_AC_conversion_unit = ttk.Label(self,
            text=f"%"
            )
        self.AC_to_AC_conversion_unit.grid(
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
        self.PV_panel_label = ttk.Label(self, text="PV panel")
        self.PV_panel_label.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        self.PV_panel = ttk.Combobox(
            self,
            values=["default_pv"],
            state="readonly",
            bootstyle=WARNING,
        )
        self.PV_panel.current(0)
        self.PV_panel.grid(row=9, column=2, padx=10, pady=5, sticky="ew")

        # Select AC heat exchanger
        self.AC_heat_exchanger_label = ttk.Label(self, text="AC heat exchanger")
        self.AC_heat_exchanger_label.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        self.AC_heat_exchanger = ttk.Combobox(
            self,
            values=["default_heat_exchanger"],
            state="readonly",
            bootstyle=WARNING,
        )
        self.AC_heat_exchanger.current(0)
        self.AC_heat_exchanger.grid(row=10, column=2, padx=10, pady=5, sticky="ew")


    def set_system(self, minigrid: Minigrid, scenarios: list[Scenario]) -> None:
        """
        Sets the scenarios on the system frame.

        """

        pass
        



