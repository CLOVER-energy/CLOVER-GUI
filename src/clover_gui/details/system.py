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

from clover.generation.solar import PVPanel
from clover.simulation.diesel import DieselGenerator
from clover.simulation.energy_system import Minigrid
from clover.simulation.storage_utils import Battery
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
            self.ac_transmission.set(max(min(self.ac_transmission.get(), 100), 0))
            self.ac_transmission_entry.update()

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
            self.dc_transmission.set(max(min(self.dc_transmission.get(), 100), 0))
            self.dc_transmission_entry.update()

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

        self.dc_to_ac_conversion = ttk.DoubleVar(self, 97)

        def scalar_dc_to_ac_conversion(_):
            self.dc_to_ac_conversion.set(
                max(min(self.dc_to_ac_conversion.get(), 100), 0)
            )
            self.dc_to_ac_conversion_entry.update()

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
                max(min(self.dc_to_dc_conversion.get(), 100), 0)
            )
            self.dc_to_dc_conversion_entry.update()

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
                max(min(self.ac_to_dc_conversion.get(), 100), 0)
            )
            self.ac_to_dc_conversion_entry.update()

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
                max(min(self.ac_to_ac_conversion.get(), 100), 0)
            )
            self.ac_to_ac_conversion_entry.update()

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

        self.battery = ttk.StringVar(self, "")
        self.battery_combobox = ttk.Combobox(
            self,
            values=[],
            state=READONLY,
            bootstyle=WARNING,
            textvariable=self.battery,
        )
        self.battery_combobox.grid(row=7, column=2, padx=10, pady=5, sticky="ew")

        # Select diesel generator
        self.diesel_generator_label = ttk.Label(self, text="Diesel generator")
        self.diesel_generator_label.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        self.diesel_generator = ttk.StringVar(self, "")
        self.diesel_generator_combobox = ttk.Combobox(
            self,
            values=[],
            state=READONLY,
            bootstyle=WARNING,
            textvariable=self.diesel_generator,
        )
        self.diesel_generator_combobox.grid(
            row=8, column=2, padx=10, pady=5, sticky="ew"
        )

        # Select PV panel
        self.pv_panel_label = ttk.Label(self, text="PV panel")
        self.pv_panel_label.grid(row=9, column=1, padx=10, pady=5, sticky="w")

        self.pv_panel = ttk.StringVar(self, "")
        self.pv_panel_combobox = ttk.Combobox(
            self,
            values=[],
            state=READONLY,
            bootstyle=WARNING,
            textvariable=self.pv_panel,
        )
        self.pv_panel_combobox.grid(row=9, column=2, padx=10, pady=5, sticky="ew")

        # Select heat exchanger
        self.heat_exchanger_label = ttk.Label(self, text="AC heat exchanger")
        self.heat_exchanger_label.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        self.heat_exchanger = ttk.StringVar(self, "")
        self.heat_exchanger_combobox = ttk.Combobox(
            self,
            values=[],
            state=DISABLED,
            bootstyle=WARNING,
        )
        self.heat_exchanger_combobox.grid(
            row=10, column=2, padx=10, pady=5, sticky="ew"
        )

    def set_system(
        self,
        batteries: list[Battery],
        diesel_generators: list[DieselGenerator],
        minigrid: Minigrid,
        pv_panels: list[PVPanel],
    ) -> None:
        """
        Sets the scenarios on the system frame.

        """

        # Update the AC transmission efficiency
        self.ac_transmission.set(float(100 * minigrid.ac_transmission_efficiency))
        self.ac_transmission_entry.update()
        self.ac_transmission_slider.set(self.ac_transmission.get())

        # Update the DC transmission efficiency
        self.dc_transmission.set(float(100 * minigrid.dc_transmission_efficiency))
        self.dc_transmission_entry.update()
        self.dc_transmission_slider.set(self.dc_transmission.get())

        # Update the conversion efficincies
        self.ac_to_ac_conversion.set(
            float(100 * minigrid.ac_to_ac_conversion_efficiency)
        )
        self.ac_to_ac_conversion_entry.update()
        self.ac_to_ac_conversion_slider.set(self.ac_to_ac_conversion.get())

        self.ac_to_dc_conversion.set(
            float(100 * minigrid.ac_to_dc_conversion_efficiency)
        )
        self.ac_to_dc_conversion_entry.update()
        self.ac_to_dc_conversion_slider.set(self.ac_to_dc_conversion.get())

        self.dc_to_ac_conversion.set(
            float(100 * minigrid.dc_to_ac_conversion_efficiency)
        )
        self.dc_to_ac_conversion_entry.update()
        self.dc_to_ac_conversion_slider.set(self.dc_to_ac_conversion.get())

        self.dc_to_dc_conversion.set(
            float(100 * minigrid.dc_to_dc_conversion_efficiency)
        )
        self.dc_to_dc_conversion_entry.update()
        self.dc_to_dc_conversion_slider.set(self.dc_to_dc_conversion.get())

        # Update the battery name
        if minigrid.battery is not None:
            self.battery.set(minigrid.battery.name)
        else:
            self.battery_combobox.configure(state=DISABLED)

        # Update the combobox
        self.battery_combobox["values"] = [entry.name for entry in batteries]
        self.battery_combobox.set(self.battery.get())

        # Update the PV-panel name
        if minigrid.pv_panel is not None:
            self.pv_panel.set(minigrid.pv_panel.name)
        else:
            self.pv_panel_combobox.configure(state=DISABLED)

        # Update the combobox
        self.pv_panel_combobox["values"] = [entry.name for entry in pv_panels]
        self.pv_panel_combobox.set(self.pv_panel.get())

        # Update the diesel-generator name
        if minigrid.diesel_generator is not None:
            self.diesel_generator.set(minigrid.diesel_generator.name)
        else:
            self.diesel_generator_combobox.configure(state=DISABLED)

        # Update the combobox
        self.diesel_generator_combobox["values"] = [
            entry.name for entry in diesel_generators
        ]
        self.diesel_generator_combobox.set(self.diesel_generator.get())

        # Update the heat-exchanger name
        if minigrid.heat_exchanger is not None:
            self.heat_exchanger.set(minigrid.heat_exchanger.name)
            self.heat_exchanger_combobox.configure(state=READONLY)
        else:
            self.heat_exchanger_combobox.configure(state=DISABLED)
        self.heat_exchanger_combobox.set(self.heat_exchanger.get())
