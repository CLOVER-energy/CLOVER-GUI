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

        self.columnconfigure(0, weight=2)  # First row has the header
        self.columnconfigure(1, weight=2)  # These rows have entries
        self.columnconfigure(2, weight=1)  # These rows have entries

        self.panel_name_variable = tk.StringVar(value="m-Si")

        self.pv_panel_entry = ttk.Combobox(
            self, bootstyle=WARNING, textvariable=self.panel_name_variable
        )
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

        # Reference efficiency
        self.reference_efficiency_label = ttk.Label(self, text="Reference efficiency")
        self.reference_efficiency_label.grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )

        self.reference_efficiency = ttk.DoubleVar(self, 15, "reference_efficiency")

        self.reference_efficiency_unit = ttk.Label(self, text=f" 15%")
        self.reference_efficiency_unit.grid(
            row=5, column=2, padx=10, pady=5, sticky="ew"
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
            row=5, column=1, padx=10, pady=5, sticky="ew"
        )

        # Reference temperature
        self.reference_temperature_label = ttk.Label(self, text="Reference temperature")
        self.reference_temperature_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        self.reference_temperature = tk.DoubleVar(value=25)
        self.reference_temperature_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.reference_temperature,
            state=DISABLED,
        )
        self.reference_temperature_entry.grid(
            row=6, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.reference_temperature_unit = ttk.Label(self, text="degrees Celsius")
        self.reference_temperature_unit.grid(
            row=6, column=2, padx=10, pady=5, sticky="w"
        )

        # Thermal coefficient
        self.thermal_coefficient_label = ttk.Label(self, text="Thermal coefficient")
        self.thermal_coefficient_label.grid(
            row=7, column=0, padx=10, pady=5, sticky="w"
        )

        self.thermal_coefficient = tk.DoubleVar(value=0.0056)
        self.thermal_coefficient_entry = ttk.Entry(
            self,
            bootstyle=WARNING,
            textvariable=self.thermal_coefficient,
            state=DISABLED,
        )
        self.thermal_coefficient_entry.grid(
            row=7, column=1, padx=10, pady=5, sticky="ew", ipadx=80
        )

        self.thermal_coefficient_unit = ttk.Label(self, text="% / degree Celsius")
        self.thermal_coefficient_unit.grid(row=7, column=2, padx=10, pady=5, sticky="w")

    def populate_available_panels(self) -> None:
        """Populate the combo box with the set of avialable panels."""

        self.pv_panel_entry["values"] = ["m-Si"]
