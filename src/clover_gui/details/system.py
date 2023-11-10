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
import tkinter as tk

from clover import Location, ProgrammerJudgementFault
from clover.generation.solar import PVPanel
from clover.impact.finance import ImpactingComponent
from clover.impact.__utils__ import LIFETIME, SIZE_INCREMENT
from clover.simulation.__utils__ import (
    AC_TO_AC,
    AC_TO_DC,
    CONVERSION,
    DC_TO_AC,
    DC_TO_DC,
)
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

        self.rowconfigure(0, weight=1)  # scrolled frame
        self.columnconfigure(0, weight=1)

        # Create the scrollable frame and rows
        self.scrollable_system_frame = ScrolledFrame(
            self,
        )
        self.scrollable_system_frame.grid(
            row=0,
            column=0,
            padx=10,
            pady=5,
            ipady=0,
            ipadx=0,
            sticky="news",
        )

        self.scrollable_system_frame.rowconfigure(0, weight=1)
        self.scrollable_system_frame.rowconfigure(1, weight=1)
        self.scrollable_system_frame.rowconfigure(2, weight=1)
        self.scrollable_system_frame.rowconfigure(3, weight=1)
        self.scrollable_system_frame.rowconfigure(4, weight=1)
        self.scrollable_system_frame.rowconfigure(5, weight=1)
        self.scrollable_system_frame.rowconfigure(6, weight=1)
        self.scrollable_system_frame.rowconfigure(7, weight=1)
        self.scrollable_system_frame.rowconfigure(8, weight=1)
        self.scrollable_system_frame.rowconfigure(9, weight=1)
        self.scrollable_system_frame.rowconfigure(10, weight=1)
        self.scrollable_system_frame.rowconfigure(11, weight=1)
        self.scrollable_system_frame.rowconfigure(12, weight=1)
        self.scrollable_system_frame.rowconfigure(13, weight=1)
        self.scrollable_system_frame.rowconfigure(14, weight=1)
        self.scrollable_system_frame.rowconfigure(15, weight=1)
        self.scrollable_system_frame.rowconfigure(16, weight=1)

        self.scrollable_system_frame.columnconfigure(0, weight=1)
        self.scrollable_system_frame.columnconfigure(1, weight=1)
        self.scrollable_system_frame.columnconfigure(2, weight=1)
        self.scrollable_system_frame.columnconfigure(3, weight=1)
        self.scrollable_system_frame.columnconfigure(4, weight=1)
        self.scrollable_system_frame.columnconfigure(5, weight=1)

        # Transmission and conversion efficiencies header
        # custom_font = tk.font.nametofont("TkDefaultFont")
        # custom_font_bold =custom_font.configure(weight="bold")

        bold_head = ttk.Style()
        bold_head.configure("Bold.TLabel", font=("TkDefaultFont", 12, "bold"))

        self.efficiencies_header = ttk.Label(
            self.scrollable_system_frame,
            text="Transmission and Conversion Efficiencies",
            style="Bold.TLabel",
        )
        self.efficiencies_header.grid(
            row=0, column=1, padx=10, columnspan=5, pady=5, sticky="w"
        )

        # AC transmission efficiency
        self.ac_transmission_label = ttk.Label(
            self.scrollable_system_frame, text="AC transmission efficiency"
        )
        self.ac_transmission_label.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.ac_transmission = ttk.DoubleVar(self, "92")

        def scalar_ac_transmission(_):
            self.ac_transmission.set(
                round(max(min(self.ac_transmission.get(), 100), 0), 1)
            )
            self.ac_transmission_entry.update()

        self.ac_transmission_slider = ttk.Scale(
            self.scrollable_system_frame,
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
            self.ac_transmission.set(round(self.ac_transmission_entry.get(), 2))
            self.ac_transmission_slider.set(round(self.ac_transmission.get(), 2))

        self.ac_transmission_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.ac_transmission,
        )

        self.ac_transmission_entry.grid(row=1, column=3, padx=10, pady=5, sticky="ew")
        self.ac_transmission_entry.bind("<Return>", enter_ac_transmission)

        self.ac_transmission_unit = ttk.Label(self.scrollable_system_frame, text=f"%")
        self.ac_transmission_unit.grid(row=1, column=4, padx=10, pady=5, sticky="ew")

        # DC transmission efficiency
        self.dc_transmission_label = ttk.Label(
            self.scrollable_system_frame, text="DC transmission efficiency"
        )
        self.dc_transmission_label.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.dc_transmission = ttk.DoubleVar(self, "96")

        def scalar_dc_transmission(_):
            self.dc_transmission.set(
                round(max(min(self.dc_transmission.get(), 100), 0), 1)
            )
            self.dc_transmission_entry.update()

        self.dc_transmission_slider = ttk.Scale(
            self.scrollable_system_frame,
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
            self.dc_transmission.set(round(self.dc_transmission_entry.get(), 2))
            self.dc_transmission_slider.set(round(self.dc_transmission.get()), 2)

        self.dc_transmission_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.dc_transmission,
        )

        self.dc_transmission_entry.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        self.dc_transmission_entry.bind("<Return>", enter_dc_transmission)

        self.dc_transmission_unit = ttk.Label(self.scrollable_system_frame, text=f"%")
        self.dc_transmission_unit.grid(row=2, column=4, padx=10, pady=5, sticky="ew")

        # # DC to AC conversion efficiency
        self.dc_to_ac_conversion_label = ttk.Label(
            self.scrollable_system_frame, text="DC to AC conversion efficiency"
        )
        self.dc_to_ac_conversion_label.grid(
            row=3, column=1, padx=10, pady=5, sticky="w"
        )

        self.dc_to_ac_conversion = ttk.DoubleVar(self, 97)

        def scalar_dc_to_ac_conversion(_):
            self.dc_to_ac_conversion.set(
                round(max(min(self.dc_to_ac_conversion.get(), 100), 0), 1)
            )
            self.dc_to_ac_conversion_entry.update()

        self.dc_to_ac_conversion_slider = ttk.Scale(
            self.scrollable_system_frame,
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
            self.dc_to_ac_conversion.set(round(self.dc_to_ac_conversion_entry.get(), 2))
            self.dc_to_ac_conversion_slider.set(
                round(self.dc_to_ac_conversion.get(), 2)
            )

        self.dc_to_ac_conversion_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.dc_to_ac_conversion,
        )

        self.dc_to_ac_conversion_entry.grid(
            row=3, column=3, padx=10, pady=5, sticky="ew"
        )
        self.dc_to_ac_conversion_entry.bind("<Return>", enter_dc_to_ac_conversion)

        self.dc_to_ac_conversion_unit = ttk.Label(
            self.scrollable_system_frame, text=f"%"
        )
        self.dc_to_ac_conversion_unit.grid(
            row=3, column=4, padx=10, pady=5, sticky="ew"
        )

        # # DC to DC conversion efficiency
        self.dc_to_dc_conversion_label = ttk.Label(
            self.scrollable_system_frame, text="DC to DC conversion efficiency"
        )
        self.dc_to_dc_conversion_label.grid(
            row=4, column=1, padx=10, pady=5, sticky="w"
        )

        self.dc_to_dc_conversion = ttk.DoubleVar(self, "95")

        def scalar_dc_to_dc_conversion(_):
            self.dc_to_dc_conversion.set(
                round(max(min(self.dc_to_dc_conversion.get(), 100), 0), 1)
            )
            self.dc_to_dc_conversion_entry.update()

        self.dc_to_dc_conversion_slider = ttk.Scale(
            self.scrollable_system_frame,
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
            self.dc_to_dc_conversion.set(round(self.dc_to_dc_conversion_entry.get(), 2))
            self.dc_to_dc_conversion_slider.set(
                round(self.dc_to_dc_conversion.get(), 2)
            )

        self.dc_to_dc_conversion_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.dc_to_dc_conversion,
        )

        self.dc_to_dc_conversion_entry.grid(
            row=4, column=3, padx=10, pady=5, sticky="ew"
        )
        self.dc_to_dc_conversion_entry.bind("<Return>", enter_dc_to_dc_conversion)

        self.dc_to_dc_conversion_unit = ttk.Label(
            self.scrollable_system_frame, text=f"%"
        )
        self.dc_to_dc_conversion_unit.grid(
            row=4, column=4, padx=10, pady=5, sticky="ew"
        )

        # # AC to DC conversion efficiency
        self.ac_to_dc_conversion_label = ttk.Label(
            self.scrollable_system_frame, text="AC to DC conversion efficiency"
        )
        self.ac_to_dc_conversion_label.grid(
            row=5, column=1, padx=10, pady=5, sticky="w"
        )

        self.ac_to_dc_conversion = ttk.DoubleVar(self, "90")

        def scalar_ac_to_dc_conversion(_):
            self.ac_to_dc_conversion.set(
                round(max(min(self.ac_to_dc_conversion.get(), 100), 0), 1)
            )
            self.ac_to_dc_conversion_entry.update()

        self.ac_to_dc_conversion_slider = ttk.Scale(
            self.scrollable_system_frame,
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
            self.ac_to_dc_conversion.set(round(self.ac_to_dc_conversion_entry.get(), 2))
            self.ac_to_dc_conversion_slider.set(
                round(self.ac_to_dc_conversion.get(), 2)
            )

        self.ac_to_dc_conversion_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.ac_to_dc_conversion,
        )

        self.ac_to_dc_conversion_entry.grid(
            row=5, column=3, padx=10, pady=5, sticky="ew"
        )
        self.ac_to_dc_conversion_entry.bind("<Return>", enter_ac_to_dc_conversion)

        self.ac_to_dc_conversion_unit = ttk.Label(
            self.scrollable_system_frame, text=f"%"
        )

        self.ac_to_dc_conversion_unit.grid(
            row=5, column=4, padx=10, pady=5, sticky="ew"
        )

        # # AC to AC conversion efficiency
        self.ac_to_ac_conversion_label = ttk.Label(
            self.scrollable_system_frame, text="AC to AC conversion efficiency"
        )
        self.ac_to_ac_conversion_label.grid(
            row=6, column=1, padx=10, pady=5, sticky="w"
        )

        self.ac_to_ac_conversion = ttk.DoubleVar(self.scrollable_system_frame, "98")

        def scalar_ac_to_ac_conversion(_):
            self.ac_to_ac_conversion.set(
                round(max(min(self.ac_to_ac_conversion.get(), 100), 0), 1)
            )
            self.ac_to_ac_conversion_entry.update()

        self.ac_to_ac_conversion_slider = ttk.Scale(
            self.scrollable_system_frame,
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
            self.ac_to_ac_conversion.set(round(self.ac_to_ac_conversion_entry.get(), 2))
            self.ac_to_ac_conversion_slider.set(
                round(self.ac_to_ac_conversion.get(), 2)
            )

        self.ac_to_ac_conversion_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.ac_to_ac_conversion,
        )

        self.ac_to_ac_conversion_entry.grid(
            row=6, column=3, padx=10, pady=5, sticky="ew"
        )
        self.ac_to_ac_conversion_entry.bind("<Return>", enter_ac_to_ac_conversion)

        self.ac_to_ac_conversion_unit = ttk.Label(
            self.scrollable_system_frame, text=f"%"
        )
        self.ac_to_ac_conversion_unit.grid(
            row=6, column=4, padx=10, pady=5, sticky="ew"
        )

        # Empty row
        self.empty_row = ttk.Label(self.scrollable_system_frame, text="")
        self.empty_row.grid(row=7, column=1, padx=10, pady=5, sticky="w")

        # Line separator
        self.horizontal_divider = ttk.Separator(
            self.scrollable_system_frame, orient=ttk.HORIZONTAL
        )
        self.horizontal_divider.grid(
            row=8, column=1, columnspan=7, padx=10, pady=5, sticky="ew"
        )

        # Inverter settings header
        self.inverter_header = ttk.Label(
            self.scrollable_system_frame, text="Inverter Settings", style="Bold.TLabel"
        )
        self.inverter_header.grid(
            row=9, column=1, columnspan=4, padx=10, pady=5, sticky="w"
        )

        # Inverter lifetime
        self.inverter_lifetime_label = ttk.Label(
            self.scrollable_system_frame, text="Inverter lifetime"
        )
        self.inverter_lifetime_label.grid(row=10, column=1, padx=10, pady=5, sticky="w")

        self.inverter_lifetime = ttk.IntVar(self, "10")

        def _round_inverter_lifetime(_) -> None:
            """Round the inverter lifetime to the nearest integer."""

            self.inverter_lifetime.set(int(self.inverter_lifetime.get()))
            self.inverter_lifetime_entry.update()

        self.inverter_lifetime_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.inverter_lifetime,
        )
        self.inverter_lifetime_entry.bind("<Return>", _round_inverter_lifetime)

        self.inverter_lifetime_entry.grid(
            row=10, column=2, padx=10, pady=5, sticky="ew"
        )

        self.inverter_lifetime_unit = ttk.Label(
            self.scrollable_system_frame, text=f"years"
        )
        self.inverter_lifetime_unit.grid(row=10, column=3, padx=10, pady=5, sticky="ew")

        # Inverter step size
        self.inverter_step_size_label = ttk.Label(
            self.scrollable_system_frame, text="Inverter step size"
        )
        self.inverter_step_size_label.grid(
            row=11, column=1, padx=10, pady=5, sticky="w"
        )

        self.inverter_step_size = ttk.IntVar(self, "1")
        self.inverter_step_size_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.inverter_step_size,
        )

        self.inverter_step_size_entry.grid(
            row=11, column=2, padx=10, pady=5, sticky="ew"
        )

        self.inverter_step_size_unit = ttk.Label(
            self.scrollable_system_frame, text=f"kW"
        )
        self.inverter_step_size_unit.grid(
            row=11, column=3, padx=10, pady=5, sticky="ew"
        )

        # Empty row
        self.empty_row = ttk.Label(self.scrollable_system_frame, text="")
        self.empty_row.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        # Line separator
        self.horizontal_divider = ttk.Separator(
            self.scrollable_system_frame, orient=ttk.HORIZONTAL
        )
        self.horizontal_divider.grid(
            row=13, column=1, columnspan=7, padx=10, pady=5, sticky="ew"
        )

        # Households settings header
        self.households_header = ttk.Label(
            self.scrollable_system_frame, text="Households/community Settings", style="Bold.TLabel"
        )
        self.households_header.grid(
            row=14, column=1, columnspan=4, padx=10, pady=5, sticky="w"
        )

        # Household size and community growth rate
        self.community_size_label = ttk.Label(
            self.scrollable_system_frame, text="Community size"
        )
        self.community_size_label.grid(row=15, column=1, padx=10, pady=5, sticky="w")

        self.community_size = ttk.IntVar(self, 100)

        def _round_community_size(_) -> None:
            """Round the community size lifetime to the nearest integer."""

            self.community_size.set(int(self.community_size.get()))
            self.community_size_entry.update()

        self.community_size_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.community_size,
        )
        self.community_size_entry.bind("<Return>", _round_community_size)

        self.community_size_entry.grid(
            row=15, column=2, padx=10, pady=5, sticky="ew"
        )

        self.community_size_unit = ttk.Label(
            self.scrollable_system_frame, text=f"households"
        )
        self.community_size_unit.grid(row=15, column=3, padx=10, pady=5, sticky="ew")

        # Commnuity growth rate
        self.community_growth_rate_label = ttk.Label(
            self.scrollable_system_frame, text="Community growth rate"
        )
        self.community_growth_rate_label.grid(
            row=16, column=1, padx=10, pady=5, sticky="w"
        )

        self.community_growth_rate = ttk.DoubleVar(self, 1)
        self.community_growth_rate_entry = ttk.Entry(
            self.scrollable_system_frame,
            bootstyle=WARNING,
            textvariable=self.community_growth_rate,
        )

        self.community_growth_rate_entry.grid(
            row=16, column=2, padx=10, pady=5, sticky="ew"
        )

        self.community_growth_rate_unit = ttk.Label(
            self.scrollable_system_frame, text=f"% growth per year"
        )
        self.community_growth_rate_unit.grid(
            row=16, column=3, padx=10, pady=5, sticky="ew"
        )



        # # Empty line
        # self.empty_row = ttk.Label(self.scrollable_system_frame, text="")
        # self.empty_row.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        # # Line separator
        # self.horizontal_divider = ttk.Separator(
        #     self.scrollable_system_frame, orient=ttk.HORIZONTAL
        # )
        # # Line divider
        # self.horizontal_divider.grid(
        #     row=13, column=1, columnspan=7, padx=10, pady=5, sticky="ew"
        # )

        # # System set-up header
        # self.system_header = ttk.Label(
        #     self.scrollable_system_frame, text="System Setup", style="Bold.TLabel"
        # )
        # self.system_header.grid(
        #     row=14, column=1, padx=10, columnspan=4, pady=5, sticky="w"
        # )

        # # Select battery
        # self.battery_label = ttk.Label(self.scrollable_system_frame, text="Battery")
        # self.battery_label.grid(row=15, column=1, padx=10, pady=5, sticky="w")

        # self.battery = ttk.StringVar(self, "")
        # self.battery_combobox = ttk.Combobox(
        #     self.scrollable_system_frame,
        #     values=[],
        #     state=READONLY,
        #     bootstyle=WARNING,
        #     textvariable=self.battery,
        # )
        # self.battery_combobox.grid(row=15, column=2, padx=10, pady=5, sticky="ew")

        # # Select diesel generator
        # self.diesel_generator_label = ttk.Label(
        #     self.scrollable_system_frame, text="Diesel generator"
        # )
        # self.diesel_generator_label.grid(row=16, column=1, padx=10, pady=5, sticky="w")

        # self.diesel_generator = ttk.StringVar(self, "")
        # self.diesel_generator_combobox = ttk.Combobox(
        #     self.scrollable_system_frame,
        #     values=[],
        #     state=READONLY,
        #     bootstyle=WARNING,
        #     textvariable=self.diesel_generator,
        # )
        # self.diesel_generator_combobox.grid(
        #     row=16, column=2, padx=10, pady=5, sticky="ew"
        # )

        # # Select PV panel
        # self.pv_panel_label = ttk.Label(self.scrollable_system_frame, text="PV panel")
        # self.pv_panel_label.grid(row=17, column=1, padx=10, pady=5, sticky="w")

        # self.pv_panel = ttk.StringVar(self, "")
        # self.pv_panel_combobox = ttk.Combobox(
        #     self.scrollable_system_frame,
        #     values=[],
        #     state=READONLY,
        #     bootstyle=WARNING,
        #     textvariable=self.pv_panel,
        # )
        # self.pv_panel_combobox.grid(row=17, column=2, padx=10, pady=5, sticky="ew")

        # # Select heat exchanger
        # self.heat_exchanger_label = ttk.Label(
        #     self.scrollable_system_frame, text="AC heat exchanger"
        # )
        # # self.heat_exchanger_label.grid(row=12, column=1, padx=10, pady=5, sticky="w")

        # self.heat_exchanger = ttk.StringVar(self, "")
        # self.heat_exchanger_combobox = ttk.Combobox(
        #     self.scrollable_system_frame,
        #     values=[],
        #     state=DISABLED,
        #     bootstyle=WARNING,
        # )
        # # self.heat_exchanger_combobox.grid(
        # #     row=12, column=2, padx=10, pady=5, sticky="ew"
        # # )

        # # Select the grid profile
        # self.grid_profile_label = ttk.Label(
        #     self.scrollable_system_frame, text="Grid profile"
        # )
        # self.grid_profile_label.grid(row=18, column=1, padx=10, pady=5, sticky="w")

        # self.grid_profile = ttk.StringVar(self, "")
        # self.grid_profile_combobox = ttk.Combobox(
        #     self.scrollable_system_frame,
        #     values=[],
        #     state=READONLY,
        #     bootstyle=WARNING,
        #     textvariable=self.grid_profile,
        # )
        # self.grid_profile_combobox.grid(row=18, column=2, padx=10, pady=5, sticky="ew")

        # # Empty row
        # self.empty_row = ttk.Label(self.scrollable_system_frame, text="")
        # self.empty_row.grid(row=19, column=1, padx=10, pady=5, sticky="w")

    def set_system(
        self,
        location: Location,
        minigrid: Minigrid,
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

        # # Update the battery name
        # if minigrid.battery is not None:
        #     self.battery.set(minigrid.battery.name)
        # else:
        #     self.battery_combobox.configure(state=DISABLED)

        # # Update the combobox
        # self.battery_combobox["values"] = [entry.name for entry in batteries]
        # self.battery_combobox.set(self.battery.get())

        # # Update the PV-panel name
        # try:
        #     if minigrid.pv_panel is not None:
        #         self.pv_panel.set(minigrid.pv_panel.name)
        #     else:
        #         self.pv_panel_combobox.configure(state=DISABLED)
        # except ProgrammerJudgementFault:
        #     self.pv_panel.set(minigrid.pv_panels[0].name)

        # # Update the combobox
        # self.pv_panel_combobox["values"] = [entry.name for entry in pv_panels]
        # self.pv_panel_combobox.set(self.pv_panel.get())

        # # Update the diesel-generator name
        # if minigrid.diesel_generator is not None:
        #     self.diesel_generator.set(minigrid.diesel_generator.name)
        # else:
        #     self.diesel_generator_combobox.configure(state=DISABLED)

        # # Update the combobox
        # self.diesel_generator_combobox["values"] = [
        #     entry.name for entry in diesel_generators
        # ]
        # self.diesel_generator_combobox.set(self.diesel_generator.get())

        # # Update the heat-exchanger name
        # if minigrid.heat_exchanger is not None:
        #     self.heat_exchanger.set(minigrid.heat_exchanger.name)
        #     self.heat_exchanger_combobox.configure(state=READONLY)
        # else:
        #     self.heat_exchanger_combobox.configure(state=DISABLED)
        # self.heat_exchanger_combobox.set(self.heat_exchanger.get())

        # # Update the grid profile name
        # self.grid_profile_combobox.set(grid_profile_name)

        # Update the inverter information.
        self.inverter_lifetime.set(minigrid.inverter.lifetime)
        self.inverter_lifetime_entry.update()

        self.inverter_step_size.set(minigrid.inverter.size_increment)
        self.inverter_step_size_entry.update()

        # Update the community information
        self.community_size.set(location.community_size)
        self.community_size_entry.update()

        self.community_growth_rate.set(100 * location.community_growth_rate)
        self.community_growth_rate_entry.update()

    @property
    def minigrid_dict(self) -> dict[str, dict[str, float] | float | str]:
        """
        Return the energy-system information as a `dict`.

        :returns:
            The information as a `dict` ready for saving.

        """

        return {
            "ac_transmission_efficiency": self.ac_transmission.get() / 100,
            "dc_transmission_efficiency": self.dc_transmission.get() / 100,
            # BATTERY: self.battery_combobox.get(),
            CONVERSION: {
                AC_TO_AC: self.ac_to_ac_conversion.get() / 100,
                AC_TO_DC: self.ac_to_dc_conversion.get() / 100,
                DC_TO_AC: self.dc_to_ac_conversion.get() / 100,
                DC_TO_DC: self.dc_to_dc_conversion.get() / 100,
            },
            # DIESEL_GENERATOR: self.diesel_generator_combobox.get(),
            # "pv_panel": self.pv_panel_combobox.get(),
            ImpactingComponent.INVERTER.value: {
                LIFETIME: int(self.inverter_lifetime.get()),
                SIZE_INCREMENT: self.inverter_step_size.get(),
            },
        }

    @property
    def location_dict(self) -> dict[str, dict[str, float] | float | str]:
        """
        Return the location information as a `dict`.

        :returns:
            The information as a `dict` ready for saving.

        """

        return {
            "community_size": self.community_size.get(),
            "community_growth_rate": 0.01 * self.community_growth_rate.get(),
        }
