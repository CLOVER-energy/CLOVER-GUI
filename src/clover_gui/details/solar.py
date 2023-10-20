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

import os
import tkinter as tk

from typing import Callable

import ttkbootstrap as ttk

from clover.generation.solar import PVPanel, Tracking
from clover.impact.finance import (
    COST,
    COST_DECREASE,
    INSTALLATION_COST,
    INSTALLATION_COST_DECREASE,
    OM,
)
from clover.impact.ghgs import (
    GHGS,
    GHG_DECREASE,
    INSTALLATION_GHGS,
    INSTALLATION_GHGS_DECREASE,
    OM_GHGS,
)
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.tooltip import ToolTip

from ..__utils__ import COSTS, EMISSIONS, PANELS

# Images directory name:
#   The name of the images directory.
_IMAGES_DIRECTORY: str = "images"


__all__ = ("SolarFrame",)


class PVFrame(ttk.Frame):
    """
    Represents the Solar PV frame.

    Contains settings for PV collectors.

    TODO: Update attributes.

    """

    def __init__(
        self, parent, data_directory: str, renewables_ninja_token: ttk.StringVar
    ):
        """
        Instantiate a :class:`PVFrame` instance.

        :param: parent
            The parent frame.

        :param: renewables_ninja_token
            The renewables.ninja API token for the user.


        """
        super().__init__(parent)

        self.add_panel_to_scenario_frame: Callable | None = None
        self.set_panels_on_system_frame: Callable | None = None

        self.renewables_ninja_token = renewables_ninja_token

        self.help_image = ttk.PhotoImage(
            file=os.path.join(
                data_directory,
                _IMAGES_DIRECTORY,
                "QMark_unhovered.png",
            )
        )

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.scrolled_frame = ScrolledFrame(
            self,
            # bootstyle=f"{WARNING}-inverted"
        )
        self.scrolled_frame.grid(row=0, column=0, padx=10, pady=5, sticky="news")

        self.scrolled_frame.rowconfigure(0, weight=1)
        self.scrolled_frame.rowconfigure(1, weight=1)
        self.scrolled_frame.rowconfigure(2, weight=1)
        self.scrolled_frame.rowconfigure(3, weight=1)
        self.scrolled_frame.rowconfigure(4, weight=1)
        self.scrolled_frame.rowconfigure(5, weight=1)
        self.scrolled_frame.rowconfigure(6, weight=1)
        self.scrolled_frame.rowconfigure(7, weight=1)
        self.scrolled_frame.rowconfigure(8, weight=1)
        self.scrolled_frame.rowconfigure(9, weight=1)
        self.scrolled_frame.rowconfigure(10, weight=1)
        self.scrolled_frame.rowconfigure(11, weight=1)
        self.scrolled_frame.rowconfigure(12, weight=1)
        self.scrolled_frame.rowconfigure(13, weight=1)
        self.scrolled_frame.rowconfigure(14, weight=1)

        self.scrolled_frame.columnconfigure(0, weight=5)
        self.scrolled_frame.columnconfigure(1, weight=4)
        self.scrolled_frame.columnconfigure(2, weight=3)
        self.scrolled_frame.columnconfigure(3, weight=3)
        self.scrolled_frame.columnconfigure(4, weight=3)
        self.scrolled_frame.columnconfigure(5, weight=1)
        self.scrolled_frame.columnconfigure(6, weight=1)

        self.renewables_ninja_token_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=f"{WARNING}-inverted",
            state=DISABLED,
            textvariable=self.renewables_ninja_token,
        )
        self.renewables_ninja_token_entry.grid(
            row=0, column=2, columnspan=4, padx=10, pady=5, sticky="ew", ipadx=60
        )

        # Panel selected
        self.panel_selected = ttk.StringVar(value="m-Si")
        self.panel_name_values = {
            "m-Si": self.panel_selected,
            (panel_name := "p-Si"): ttk.StringVar(self, panel_name),
            (panel_name := "CdTe"): ttk.StringVar(self, panel_name),
        }

        self.pv_panel_label = ttk.Label(self.scrolled_frame, text="Panel to configure")
        self.pv_panel_label.grid(
            row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.pv_panel_combobox = ttk.Combobox(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.panel_selected,
            state=READONLY,
        )
        self.pv_panel_combobox.grid(
            row=1, column=2, columnspan=3, padx=10, pady=5, sticky="w", ipadx=60
        )
        self.pv_panel_combobox.bind("<<ComboboxSelected>>", self.select_pv_panel)
        self.populate_available_panels()

        # New panel
        self.new_panel_button = ttk.Button(
            self.scrolled_frame,
            bootstyle=f"{WARNING}-{OUTLINE}",
            command=self.add_panel,
            text="New Panel",
        )
        self.new_panel_button.grid(row=1, column=5, padx=10, pady=5, ipadx=40)

        # Panel name
        self.panel_name_label = ttk.Label(self.scrolled_frame, text="Panel name")
        self.panel_name_label.grid(
            row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.panel_name_entry = ttk.Entry(
            self.scrolled_frame, bootstyle=WARNING, textvariable=self.panel_selected
        )
        self.panel_name_entry.grid(
            row=2, column=2, columnspan=2, padx=10, pady=5, sticky="ew", ipadx=50
        )
        self.panel_name_entry.bind("<Return>", self.enter_panel_name)

        # Save panel name button
        self.save_panel_name_button = ttk.Button(
            self.scrolled_frame,
            bootstyle=f"{WARNING}-{TOOLBUTTON}",
            text="Save",
            command=self.enter_panel_name,
        )
        self.save_panel_name_button.grid(row=2, column=4, padx=10, pady=5, sticky="ew")

        # Nominal power
        self.nominal_power_label = ttk.Label(self.scrolled_frame, text="Nominal power")
        self.nominal_power_label.grid(
            row=3, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.nominal_power: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 1, f"{panel_name}_nominal_power")
            for panel_name in self.panel_name_values
        }
        self.nominal_power_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.nominal_power[self.panel_selected.get()],
        )
        self.nominal_power_entry.grid(
            row=3,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.nominal_power_unit = ttk.Label(self.scrolled_frame, text="kWp")
        self.nominal_power_unit.grid(row=3, column=5, padx=10, pady=5, sticky="w")

        # Lifetime
        self.lifetime_label = ttk.Label(self.scrolled_frame, text="Lifetime")
        self.lifetime_label.grid(
            row=4, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.panel_lifetimes: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 20, f"{panel_name}_lifetime")
            for panel_name in self.panel_name_values
        }

        def scalar_lifetime(_):
            self.panel_lifetimes[self.panel_selected.get()].set(
                int(self.lifetime_slider.get())
            )
            self.lifetime_entry.update()

        self.lifetime_slider = ttk.Scale(
            self.scrolled_frame,
            from_=0,
            to=30,
            orient=tk.HORIZONTAL,
            # length=320,
            command=scalar_lifetime,
            bootstyle=WARNING,
            variable=self.panel_lifetimes[self.panel_selected.get()],
        )
        self.lifetime_slider.grid(
            row=4, column=2, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        def enter_lifetime(_):
            self.panel_lifetimes[self.panel_selected.get()].set(
                int(self.lifetime_entry.get())
            )
            self.lifetime_slider.set(
                self.panel_lifetimes[self.panel_selected.get()].get()
            )

        self.lifetime_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.panel_lifetimes[self.panel_selected.get()],
        )
        self.lifetime_entry.grid(row=4, column=5, padx=10, pady=5, sticky="ew")
        self.lifetime_entry.bind("<Return>", enter_lifetime)

        self.lifetime_unit = ttk.Label(self.scrolled_frame, text="years")
        self.lifetime_unit.grid(row=4, column=6, padx=15, pady=5, sticky="w")

        # Tracking
        self.tracking_label = ttk.Label(self.scrolled_frame, text="Tracking")
        self.tracking_label.grid(
            row=5, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.tracking: dict[str, ttk.IntVar] = {
            panel_name: ttk.IntVar(self, 0, f"{panel_name}_tracking")
            for panel_name in self.panel_name_values
        }
        self.fixed_tracking: ttk.BooleanVar = ttk.BooleanVar(self, True)
        self.single_axis_tracking: ttk.BooleanVar = ttk.BooleanVar(self, False)
        self.dual_axis_tracking: ttk.BooleanVar = ttk.BooleanVar(self, False)

        self.fixed_tracking_button = ttk.Checkbutton(
            self.scrolled_frame,
            variable=self.fixed_tracking,
            command=self._fixed_axis_callback,
            bootstyle=f"{WARNING}-{TOOLBUTTON}",
            text="Fixed",
        )
        self.fixed_tracking_button.grid(
            row=5, column=2, padx=10, pady=5, ipadx=5, sticky="ew"
        )

        self.single_axis_tracking_button = ttk.Checkbutton(
            self.scrolled_frame,
            variable=self.single_axis_tracking,
            command=self._single_axis_callback,
            bootstyle=f"{WARNING}-{TOOLBUTTON}",
            text="Single-axis",
        )
        self.single_axis_tracking_button.grid(
            row=5, column=3, padx=10, pady=5, ipadx=5, sticky="ew"
        )

        self.dual_axis_tracking_button = ttk.Checkbutton(
            self.scrolled_frame,
            variable=self.dual_axis_tracking,
            command=self._dual_axis_callback,
            bootstyle=f"{WARNING}-{TOOLBUTTON}",
            text="Dual-axis",
        )
        self.dual_axis_tracking_button.grid(
            row=5, column=4, padx=10, pady=5, ipadx=5, sticky="ew"
        )

        # Tilt
        self.tilt_label = ttk.Label(self.scrolled_frame, text="Tilt")
        self.tilt_label.grid(row=6, column=0, columnspan=2, padx=10, pady=5, sticky="w")

        self.panel_tilt: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.IntVar(self, 22, f"{panel_name}_tilt")
            for panel_name in self.panel_name_values
        }

        def scalar_tilt(_):
            self.panel_tilt[self.panel_selected.get()].set(
                round(self.tilt_slider.get(), 0)
            )
            self.tilt_entry.update()

        self.tilt_slider = ttk.Scale(
            self.scrolled_frame,
            from_=0,
            to=90,
            orient=tk.HORIZONTAL,
            # length=320,
            command=scalar_tilt,
            bootstyle=WARNING,
            variable=self.panel_tilt[self.panel_selected.get()],
        )
        self.tilt_slider.grid(
            row=6, column=2, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        def enter_tilt(_):
            self.panel_tilt[self.panel_selected.get()].set(
                round(float(self.tilt_entry.get()), 2)
            )
            self.tilt_slider.set(
                round(self.panel_tilt[self.panel_selected.get()].get(), 2)
            )

        self.tilt_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.panel_tilt[self.panel_selected.get()],
        )
        self.tilt_entry.grid(row=6, column=5, padx=10, pady=5, sticky="ew")
        self.tilt_entry.bind("<Return>", enter_tilt)

        self.tilt_unit = ttk.Label(self.scrolled_frame, text="degrees")
        self.tilt_unit.grid(row=6, column=6, padx=15, pady=5, sticky="w")

        # Azimuthal orientation
        self.azimuthal_orientation_label = ttk.Label(
            self.scrolled_frame, text="Azimuthal orientation"
        )
        self.azimuthal_orientation_label.grid(
            row=8, column=0, padx=10, pady=5, sticky="w"
        )

        self.azimuthal_orientation_help = ttk.Label(
            self.scrolled_frame,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )
        self.azimuthal_orientation_help.grid(
            row=8, column=1, padx=10, pady=5, sticky="ew"
        )
        self.azimuthal_orientation_help_tooltip = ToolTip(
            self.azimuthal_orientation_help,
            bootstyle=f"{INFO}-{INVERSE}",
            text="The azimuthal orientation is defined as the degrees orientation of "
            "the panel from the equator. I.E., in the northern hemisphere, 180 degrees "
            "corresponds to due-South orientation, and, in the southern hemisphere, it "
            "corresponds to due-North orientation. For more information, consult the "
            "documentation.",
        )

        self.panel_orientation: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.IntVar(self, 180, f"{panel_name}_azimuthal_orientation")
            for panel_name in self.panel_name_values
        }

        def scalar_azimuthal_orientation(_):
            self.panel_orientation[self.panel_selected.get()].set(
                round(self.azimuthal_orientation_slider.get(), 0)
            )
            self.azimuthal_orientation_entry.update()

        self.azimuthal_orientation_slider = ttk.Scale(
            self.scrolled_frame,
            from_=0,
            to=360,
            orient=tk.HORIZONTAL,
            # length=320,
            command=scalar_azimuthal_orientation,
            bootstyle=WARNING,
            variable=self.panel_orientation[self.panel_selected.get()],
        )
        self.azimuthal_orientation_slider.grid(
            row=8, column=2, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        def enter_azimuthal_orientation(_):
            self.panel_orientation[self.panel_selected.get()].set(
                round(float(self.azimuthal_orientation_entry.get()), 2)
            )
            self.azimuthal_orientation_slider.set(
                round(self.panel_orientation[self.panel_selected.get()].get(), 2)
            )

        self.azimuthal_orientation_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.panel_orientation[self.panel_selected.get()],
        )
        self.azimuthal_orientation_entry.grid(
            row=8, column=5, padx=10, pady=5, sticky="ew"
        )
        self.azimuthal_orientation_entry.bind("<Return>", enter_azimuthal_orientation)

        self.azimuthal_orientation_unit = ttk.Label(self.scrolled_frame, text="degrees")
        self.azimuthal_orientation_unit.grid(
            row=8, column=6, padx=(15, 20), pady=5, sticky="w"
        )

        # Reference efficiency
        self.reference_efficiency_label = ttk.Label(
            self.scrolled_frame, text="Reference efficiency"
        )
        self.reference_efficiency_label.grid(
            row=9, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.reference_efficiencies: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 15, f"{panel_name}_reference_efficiency")
            for panel_name in self.panel_name_values
        }

        def scalar_reference_efficiency(_):
            self.reference_efficiencies[self.panel_selected.get()].set(
                self.reference_efficiency_slider.get()
            )
            self.reference_efficiency_entry.update()

        self.reference_efficiency_slider = ttk.Scale(
            self.scrolled_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            # length=320,
            command=scalar_reference_efficiency,
            bootstyle=f"{WARNING}-inverted",
            state=DISABLED,
            variable=self.reference_efficiencies[self.panel_selected.get()],
        )
        self.reference_efficiency_slider.grid(
            row=9, column=2, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        def enter_reference_efficiency(_):
            self.reference_efficiencies[self.panel_selected.get()].set(
                self.reference_efficiency_entry.get()
            )
            self.reference_efficiency_slider.set(
                self.reference_efficiencies[self.panel_selected.get()].get()
            )

        self.reference_efficiency_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=f"{WARNING}-inverted",
            state=DISABLED,
            textvariable=self.reference_efficiencies[self.panel_selected.get()],
        )
        self.reference_efficiency_entry.grid(
            row=9, column=5, padx=10, pady=5, sticky="ew"
        )
        self.reference_efficiency_entry.bind("<Return>", enter_reference_efficiency)

        self.reference_efficiency_unit = ttk.Label(self.scrolled_frame, text=f"%")
        self.reference_efficiency_unit.grid(
            row=9, column=6, padx=15, pady=5, sticky="w"
        )

        # Reference temperature
        self.reference_temperature_label = ttk.Label(
            self.scrolled_frame, text="Reference temperature"
        )
        self.reference_temperature_label.grid(
            row=10, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.reference_temperature: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 25, f"{panel_name}_reference_temperature")
            for panel_name in self.panel_name_values
        }
        self.reference_temperature_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.reference_temperature[self.panel_selected.get()],
            state=DISABLED,
        )
        self.reference_temperature_entry.grid(
            row=10,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.reference_temperature_unit = ttk.Label(
            self.scrolled_frame, text="degrees Celsius"
        )
        self.reference_temperature_unit.grid(
            row=10, column=5, padx=10, pady=5, sticky="w"
        )

        # Thermal coefficient
        self.thermal_coefficient_label = ttk.Label(
            self.scrolled_frame, text="Thermal coefficient"
        )
        self.thermal_coefficient_label.grid(
            row=11, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.thermal_coefficient: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0.56, f"{panel_name}_thermal_coefficient")
            for panel_name in self.panel_name_values
        }
        self.thermal_coefficient_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.thermal_coefficient[self.panel_selected.get()],
            state=DISABLED,
        )
        self.thermal_coefficient_entry.grid(
            row=11,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.thermal_coefficient_unit = ttk.Label(
            self.scrolled_frame, text="% / degree Celsius"
        )
        self.thermal_coefficient_unit.grid(
            row=11, column=5, padx=10, pady=5, sticky="w"
        )

        # Cost
        self.cost_label = ttk.Label(self.scrolled_frame, text="PV cost")
        self.cost_label.grid(
            row=12, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.costs: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_cost")
            for panel_name in self.panel_name_values
        }
        self.cost_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.costs[self.panel_selected.get()],
        )
        self.cost_entry.grid(
            row=12, column=2, columnspan=3, padx=10, pady=5, sticky="ew"
        )

        self.cost_unit = ttk.Label(self.scrolled_frame, text="$ / kWp")
        self.cost_unit.grid(row=12, column=5, padx=10, pady=5, sticky="w")

        # Cost decrease
        self.cost_decrease_label = ttk.Label(self.scrolled_frame, text="PV cost change")
        self.cost_decrease_label.grid(
            row=13, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.cost_decrease: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_cost_decrease")
            for panel_name in self.panel_name_values
        }
        self.cost_decrease_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.cost_decrease[self.panel_selected.get()],
        )
        self.cost_decrease_entry.grid(
            row=13,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.cost_decrease_unit = ttk.Label(self.scrolled_frame, text="%  / year")
        self.cost_decrease_unit.grid(row=13, column=5, padx=10, pady=5, sticky="w")

        # Installation cost
        self.installation_cost_label = ttk.Label(
            self.scrolled_frame, text="Installation cost"
        )
        self.installation_cost_label.grid(
            row=14, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.installation_costs: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_installation_cost")
            for panel_name in self.panel_name_values
        }
        self.installation_cost_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.installation_costs[self.panel_selected.get()],
        )
        self.installation_cost_entry.grid(
            row=14,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.installation_cost_unit = ttk.Label(
            self.scrolled_frame, text="$ / kWp installed"
        )
        self.installation_cost_unit.grid(row=14, column=5, padx=10, pady=5, sticky="w")

        # Installation cost decrease
        self.installation_cost_decrease_label = ttk.Label(
            self.scrolled_frame, text="Installation cost change"
        )
        self.installation_cost_decrease_label.grid(
            row=15, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.installation_cost_decrease: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(
                self, 0, f"{panel_name}_installation_cost_decrease"
            )
            for panel_name in self.panel_name_values
        }
        self.installation_cost_decrease_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.installation_cost_decrease[self.panel_selected.get()],
        )
        self.installation_cost_decrease_entry.grid(
            row=15,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.installation_cost_decrease_unit = ttk.Label(
            self.scrolled_frame, text="%  / year"
        )
        self.installation_cost_decrease_unit.grid(
            row=15, column=5, padx=10, pady=5, sticky="w"
        )

        # OPEX costs
        self.opex_costs_label = ttk.Label(self.scrolled_frame, text="OPEX (O&M) costs")
        self.opex_costs_label.grid(
            row=16, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.o_and_m_costs: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_o_and_m_costs")
            for panel_name in self.panel_name_values
        }
        self.o_and_m_costs_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.o_and_m_costs[self.panel_selected.get()],
        )
        self.o_and_m_costs_entry.grid(
            row=16,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.o_and_m_costs_unit = ttk.Label(self.scrolled_frame, text="$ / kWp / year")
        self.o_and_m_costs_unit.grid(row=16, column=5, padx=10, pady=5, sticky="w")

        # Embedded emissions
        self.embedded_emissions_label = ttk.Label(
            self.scrolled_frame, text="PV embedded emissions"
        )
        self.embedded_emissions_label.grid(
            row=17, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.embedded_emissions: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_ghgs")
            for panel_name in self.panel_name_values
        }
        self.embedded_emissions_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.embedded_emissions[self.panel_selected.get()],
        )
        self.embedded_emissions_entry.grid(
            row=17,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.embedded_emissions_unit = ttk.Label(
            self.scrolled_frame, text="kgCO2eq / kWp"
        )
        self.embedded_emissions_unit.grid(row=17, column=5, padx=10, pady=5, sticky="w")

        # Annual emissions decrease
        self.annual_emissions_decrease_label = ttk.Label(
            self.scrolled_frame, text="PV emissions change"
        )
        self.annual_emissions_decrease_label.grid(
            row=18, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.annual_emissions_decrease: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_ghgs_decrease")
            for panel_name in self.panel_name_values
        }
        self.annual_emissions_decrease_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.annual_emissions_decrease[self.panel_selected.get()],
        )
        self.annual_emissions_decrease_entry.grid(
            row=18,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.annual_emissions_decrease_unit = ttk.Label(
            self.scrolled_frame, text="% / year"
        )
        self.annual_emissions_decrease_unit.grid(
            row=18, column=5, padx=10, pady=5, sticky="w"
        )

        # Embedded installation emissions
        self.installation_emissions_label = ttk.Label(
            self.scrolled_frame, text="Installation emissions"
        )
        self.installation_emissions_label.grid(
            row=19, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.installation_emissions: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_installation_ghgs")
            for panel_name in self.panel_name_values
        }
        self.installation_emissions_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.installation_emissions[self.panel_selected.get()],
        )
        self.installation_emissions_entry.grid(
            row=19,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.installation_emissions_unit = ttk.Label(
            self.scrolled_frame, text="kgCO2eq / kWp"
        )
        self.installation_emissions_unit.grid(
            row=19, column=5, padx=10, pady=5, sticky="w"
        )

        # Annual installation emissions decrease
        self.installation_emissions_decrease_label = ttk.Label(
            self.scrolled_frame, text="Installation emissions change"
        )
        self.installation_emissions_decrease_label.grid(
            row=20, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.installation_emissions_decrease: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(
                self, 0, f"{panel_name}_installation_ghgs_decrease"
            )
            for panel_name in self.panel_name_values
        }
        self.installation_emissions_decrease_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.installation_emissions_decrease[
                self.panel_selected.get()
            ],
        )
        self.installation_emissions_decrease_entry.grid(
            row=20,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.installation_emissions_decrease_unit = ttk.Label(
            self.scrolled_frame, text="% / year"
        )
        self.installation_emissions_decrease_unit.grid(
            row=20, column=5, padx=10, pady=5, sticky="w"
        )

        # O&M emissions
        self.om_emissions_label = ttk.Label(self.scrolled_frame, text="O&M emissions")
        self.om_emissions_label.grid(
            row=21, column=0, columnspan=2, padx=10, pady=5, sticky="w"
        )

        self.om_emissions: dict[str, ttk.DoubleVar] = {
            panel_name: ttk.DoubleVar(self, 0, f"{panel_name}_o_and_m_ghgs")
            for panel_name in self.panel_name_values
        }
        self.om_emissions_entry = ttk.Entry(
            self.scrolled_frame,
            bootstyle=WARNING,
            textvariable=self.om_emissions[self.panel_selected.get()],
        )
        self.om_emissions_entry.grid(
            row=21,
            column=2,
            columnspan=3,
            padx=10,
            pady=5,
            sticky="ew",
        )

        self.om_emissions_unit = ttk.Label(
            self.scrolled_frame, text="kgCO2eq / kWp / year"
        )
        self.om_emissions_unit.grid(row=21, column=5, padx=10, pady=5, sticky="w")

    def _fixed_axis_callback(self) -> None:
        """Callback when the fixed-tracking button is depressed."""

        self.tracking[self.panel_selected.get()].set(Tracking.FIXED.value)
        self.fixed_tracking.set(True)
        self.single_axis_tracking.set(False)
        self.dual_axis_tracking.set(False)

        self.tilt_entry.configure(state=(_enabled := "enabled"))
        self.tilt_slider.configure(state=_enabled)
        self.azimuthal_orientation_entry.configure(state=_enabled)
        self.azimuthal_orientation_slider.configure(state=_enabled)

    def _single_axis_callback(self) -> None:
        """Callback when the single-axis-tracking button is depressed."""

        self.tracking[self.panel_selected.get()].set(Tracking.SINGLE_AXIS.value)
        self.fixed_tracking.set(False)
        self.single_axis_tracking.set(True)
        self.dual_axis_tracking.set(False)

        self.tilt_entry.configure(state=(_enabled := "enabled"))
        self.tilt_slider.configure(state=_enabled)
        self.azimuthal_orientation_entry.configure(state=DISABLED)
        self.azimuthal_orientation_slider.configure(state=DISABLED)

    def _dual_axis_callback(self) -> None:
        """Callback when the dual-axis-tracking button is depressed."""

        self.tracking[self.panel_selected.get()].set(Tracking.DUAL_AXIS.value)
        self.fixed_tracking.set(False)
        self.single_axis_tracking.set(False)
        self.dual_axis_tracking.set(True)

        self.tilt_entry.configure(state=DISABLED)
        self.tilt_slider.configure(state=DISABLED)
        self.azimuthal_orientation_entry.configure(state=DISABLED)
        self.azimuthal_orientation_slider.configure(state=DISABLED)

    def _tracking_callback(self) -> None:
        """Deals with tracking callback."""

        if (
            _tracking := self.tracking[self.panel_selected.get()].get()
        ) == Tracking.FIXED.value:
            self._fixed_axis_callback()
        elif _tracking == Tracking.SINGLE_AXIS.value:
            self._single_axis_callback()
        else:
            self._dual_axis_callback()

    def add_panel(self) -> None:
        """Called when a user presses the new-panel button."""

        # Determine the new name
        new_name = "New panel {suffix}"
        index = 0
        suffix = ""
        while new_name.format(suffix=suffix) in self.panel_name_values:
            index += 1
            suffix = f"({index})"

        new_name = new_name.format(suffix=suffix)

        self.panel_name_values[new_name] = ttk.StringVar(self, new_name)
        self.populate_available_panels()

        # Update all the mappings stored
        self.nominal_power[new_name] = ttk.DoubleVar(self, 1)
        self.panel_lifetimes[new_name] = ttk.DoubleVar(self, 15)
        self.panel_tilt[new_name] = ttk.DoubleVar(self, 0)
        self.panel_orientation[new_name] = ttk.DoubleVar(self, 180)
        self.reference_efficiencies[new_name] = ttk.DoubleVar(self, 0.015)
        self.reference_temperature[new_name] = ttk.DoubleVar(self, 25)
        self.thermal_coefficient[new_name] = ttk.DoubleVar(self, 0.56)
        self.costs[new_name] = ttk.DoubleVar(self, 0)
        self.cost_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.installation_costs[new_name] = ttk.DoubleVar(self, 0)
        self.installation_cost_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.o_and_m_costs[new_name] = ttk.DoubleVar(self, 0)
        self.embedded_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.om_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.annual_emissions_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.installation_emissions[new_name] = ttk.DoubleVar(self, 0)
        self.installation_emissions_decrease[new_name] = ttk.DoubleVar(self, 0)
        self.tracking[new_name] = ttk.IntVar(self, 0)

        # Select the new panel and update the screen
        self.panel_selected = self.panel_name_values[new_name]
        self.pv_panel_combobox.configure(textvariable=self.panel_selected)
        self.panel_name_entry.configure(textvariable=self.panel_selected)
        self.update_panel_frame()

        # Add the panel to the system frame's list of panels.
        self.add_panel_to_scenario_frame(new_name)

    def enter_panel_name(self, _=None) -> None:
        """Called when someone enters a new panel name."""

        self.populate_available_panels()

        # Update all the mappings stored
        self.nominal_power = {
            self.panel_name_values[key].get(): value
            for key, value in self.nominal_power.items()
        }
        self.panel_lifetimes = {
            self.panel_name_values[key].get(): value
            for key, value in self.panel_lifetimes.items()
        }
        self.panel_tilt = {
            self.panel_name_values[key].get(): value
            for key, value in self.panel_tilt.items()
        }
        self.panel_orientation = {
            self.panel_name_values[key].get(): value
            for key, value in self.panel_orientation.items()
        }
        self.reference_efficiencies = {
            self.panel_name_values[key].get(): value
            for key, value in self.reference_efficiencies.items()
        }
        self.reference_temperature = {
            self.panel_name_values[key].get(): value
            for key, value in self.reference_temperature.items()
        }
        self.thermal_coefficient = {
            self.panel_name_values[key].get(): value
            for key, value in self.thermal_coefficient.items()
        }
        self.costs = {
            self.panel_name_values[key].get(): value
            for key, value in self.costs.items()
        }
        self.cost_decrease = {
            self.panel_name_values[key].get(): value
            for key, value in self.cost_decrease.items()
        }
        self.installation_costs = {
            self.panel_name_values[key].get(): value
            for key, value in self.installation_costs.items()
        }
        self.installation_cost_decrease = {
            self.panel_name_values[key].get(): value
            for key, value in self.installation_cost_decrease.items()
        }
        self.o_and_m_costs = {
            self.panel_name_values[key].get(): value
            for key, value in self.o_and_m_costs.items()
        }
        self.embedded_emissions = {
            self.panel_name_values[key].get(): value
            for key, value in self.embedded_emissions.items()
        }
        self.annual_emissions_decrease = {
            self.panel_name_values[key].get(): value
            for key, value in self.annual_emissions_decrease.items()
        }
        self.installation_emissions = {
            self.panel_name_values[key].get(): value
            for key, value in self.installation_emissions.items()
        }
        self.installation_emissions_decrease = {
            self.panel_name_values[key].get(): value
            for key, value in self.installation_emissions_decrease.items()
        }
        self.om_emissions = {
            self.panel_name_values[key].get(): value
            for key, value in self.om_emissions.items()
        }
        self.tracking = {
            self.panel_name_values[key].get(): value
            for key, value in self.tracking.items()
        }

        # Update the panel-name values.
        self.panel_name_values = {
            entry.get(): entry for entry in self.panel_name_values.values()
        }

        # Update the panel name values in the system frame.
        self.set_panels_on_system_frame(list(self.panel_name_values.keys()))

    def populate_available_panels(self) -> None:
        """Populate the combo box with the set of avialable panels."""

        self.pv_panel_combobox["values"] = [
            entry.get() for entry in self.panel_name_values.values()
        ]

    def select_pv_panel(self, _) -> None:
        """Select the PV panel."""

        # Determine the panel name pre- and post-selection
        previous_panel_name: str = {
            (entry == self.panel_selected): key
            for key, entry in self.panel_name_values.items()
        }[True]
        selected_panel_name: str = self.pv_panel_combobox.get()

        # Reset the value of the old variable
        self.panel_name_values[previous_panel_name].set(previous_panel_name)

        # Set the variable to be the new selected variable
        self.panel_selected = self.panel_name_values[selected_panel_name]
        self.pv_panel_combobox.configure(textvariable=self.panel_selected)
        self.panel_name_entry.configure(textvariable=self.panel_selected)

        # Update the tracking
        self._tracking_callback()

        # Update the variables being displayed.
        self.update_panel_frame()

    def set_solar(
        self,
        pv_panels: list[PVPanel],
        pv_panel_costs: dict[str, dict[str, float]],
        pv_panel_emissions: dict[str, dict[str, float]],
    ) -> None:
        """
        Set the solar panel information for the frame based on the inputs provided.

        :param: pv_panels
            The `list` of :class:`solar.PVPanel` instances defined;

        :param: pv_panel_costs
            The pv-panel cost information

        :param: pv_panel_emissions
            The pv-panel emissions information;

        """

        self.panel_name_values: dict[str, ttk.StringVar] = {}

        # Clean existing maps
        self.panel_lifetimes = {}
        self.panel_tilt = {}
        self.panel_orientation = {}
        self.tracking = {}
        self.nominal_power = {}
        self.reference_efficiencies = {}
        self.reference_temperature = {}
        self.thermal_coefficient = {}
        self.costs = {}
        self.cost_decrease = {}
        self.installation_costs = {}
        self.installation_cost_decrease = {}
        self.o_and_m_costs = {}
        self.embedded_emissions = {}
        self.annual_emissions_decrease = {}
        self.installation_emissions = {}
        self.installation_emissions_decrease = {}
        self.om_emissions = {}

        for pv_panel in pv_panels:
            self.panel_name_values[pv_panel.name] = ttk.StringVar(self, pv_panel.name)
            self.panel_lifetimes[pv_panel.name] = ttk.IntVar(
                self, int(pv_panel.lifetime)
            )

            # Panel orientation
            self.panel_tilt[pv_panel.name] = ttk.IntVar(
                self, int(pv_panel.tilt) if pv_panel.tilt is not None else 0
            )

            self.panel_orientation[pv_panel.name] = ttk.IntVar(
                self,
                int(pv_panel.azimuthal_orientation)
                if pv_panel.azimuthal_orientation is not None
                else 0,
            )

            # Tracking
            self.tracking[pv_panel.name] = ttk.IntVar(self, pv_panel.tracking.value)

            self.nominal_power[pv_panel.name] = ttk.DoubleVar(
                self,
                pv_panel.pv_unit,
            )
            self.nominal_power_entry.update()

            # Performance characteristics
            self.reference_efficiencies[pv_panel.name] = ttk.DoubleVar(
                self,
                100
                * (
                    pv_panel.reference_efficiency
                    if pv_panel.reference_efficiency is not None
                    else 15
                ),
            )
            self.reference_temperature[pv_panel.name] = ttk.DoubleVar(
                self,
                (
                    pv_panel.reference_temperature
                    if pv_panel.reference_temperature is not None
                    else 25
                ),
            )
            self.thermal_coefficient[pv_panel.name] = ttk.DoubleVar(
                self,
                (
                    pv_panel.thermal_coefficient
                    if pv_panel.thermal_coefficient is not None
                    else 0.5
                ),
            )

            # Costs
            self.costs[pv_panel.name] = ttk.DoubleVar(
                self,
                (this_pv_panel_costs := pv_panel_costs[pv_panel.name]).get(COST, 0),
            )
            self.cost_decrease[pv_panel.name] = ttk.DoubleVar(
                self, -(this_pv_panel_costs.get(COST_DECREASE, 0))
            )
            self.installation_costs[pv_panel.name] = ttk.DoubleVar(
                self, this_pv_panel_costs.get(INSTALLATION_COST, 0)
            )
            self.installation_cost_decrease[pv_panel.name] = ttk.DoubleVar(
                self, -(this_pv_panel_costs.get(INSTALLATION_COST_DECREASE, 0))
            )
            self.o_and_m_costs[pv_panel.name] = ttk.DoubleVar(
                self, this_pv_panel_costs.get(OM, 0)
            )

            # Emissions
            self.embedded_emissions[pv_panel.name] = ttk.DoubleVar(
                self,
                (this_pv_panel_emissions := pv_panel_emissions[pv_panel.name]).get(
                    GHGS, 0
                ),
            )
            self.annual_emissions_decrease[pv_panel.name] = ttk.DoubleVar(
                self, -(this_pv_panel_emissions.get(GHG_DECREASE, 0))
            )
            self.installation_emissions[pv_panel.name] = ttk.DoubleVar(
                self, this_pv_panel_emissions.get(INSTALLATION_GHGS, 0)
            )
            self.installation_emissions_decrease[pv_panel.name] = ttk.DoubleVar(
                self, -(this_pv_panel_emissions.get(INSTALLATION_GHGS_DECREASE, 0))
            )
            self.om_emissions[pv_panel.name] = ttk.DoubleVar(
                self, this_pv_panel_emissions.get(OM_GHGS, 0)
            )

        self.panel_selected = self.panel_name_values[
            (_selected_panel := pv_panels[0]).name
        ]

        # Sort out tracking-related inputs.
        self._tracking_callback()

        self.pv_panel_combobox["values"] = [panel.name for panel in pv_panels]
        self.pv_panel_combobox.set(self.panel_selected.get())
        self.select_pv_panel(self.panel_selected.get())

    def update_panel_frame(self) -> None:
        """
        Updates the entries so that the correct variables are displayed on the screen.

        """

        self.nominal_power_entry.configure(
            textvariable=self.nominal_power[self.panel_selected.get()]
        )
        self.lifetime_entry.configure(
            textvariable=self.panel_lifetimes[self.panel_selected.get()]
        )
        self.lifetime_slider.configure(
            variable=self.panel_lifetimes[self.panel_selected.get()]
        )
        self.tilt_entry.configure(
            textvariable=self.panel_tilt[self.panel_selected.get()]
        )
        self.tilt_slider.configure(variable=self.panel_tilt[self.panel_selected.get()])
        self.azimuthal_orientation_entry.configure(
            textvariable=self.panel_orientation[self.panel_selected.get()]
        )
        self.azimuthal_orientation_slider.configure(
            variable=self.panel_orientation[self.panel_selected.get()]
        )
        self.reference_efficiency_entry.configure(
            textvariable=self.reference_efficiencies[self.panel_selected.get()]
        )
        self.reference_efficiency_slider.configure(
            variable=self.reference_efficiencies[self.panel_selected.get()]
        )
        self.reference_temperature_entry.configure(
            textvariable=self.reference_temperature[self.panel_selected.get()]
        )
        self.thermal_coefficient_entry.configure(
            textvariable=self.thermal_coefficient[self.panel_selected.get()]
        )
        self.cost_entry.configure(textvariable=self.costs[self.panel_selected.get()])
        self.cost_decrease_entry.configure(
            textvariable=self.cost_decrease[self.panel_selected.get()]
        )
        self.installation_cost_entry.configure(
            textvariable=self.installation_costs[self.panel_selected.get()]
        )
        self.installation_cost_decrease_entry.configure(
            textvariable=self.installation_cost_decrease[self.panel_selected.get()]
        )
        self.o_and_m_costs_entry.configure(
            textvariable=self.o_and_m_costs[self.panel_selected.get()]
        )
        self.embedded_emissions_entry.configure(
            textvariable=self.embedded_emissions[self.panel_selected.get()]
        )
        self.annual_emissions_decrease_entry.configure(
            textvariable=self.annual_emissions_decrease[self.panel_selected.get()]
        )
        self.installation_emissions_entry.configure(
            textvariable=self.installation_emissions[self.panel_selected.get()]
        )
        self.installation_emissions_decrease_entry.configure(
            textvariable=self.installation_emissions_decrease[self.panel_selected.get()]
        )
        self.om_emissions_entry.configure(
            textvariable=self.om_emissions[self.panel_selected.get()]
        )

        # Update the entries
        self.lifetime_entry.update()
        self.lifetime_slider.update()
        self.tilt_entry.update()
        self.tilt_slider.update()
        self.azimuthal_orientation_entry.update()
        self.azimuthal_orientation_slider.update()
        self.reference_efficiency_entry.update()
        self.reference_efficiency_slider.update()
        self.reference_temperature_entry.update()
        self.thermal_coefficient_entry.update()
        self.cost_entry.update()
        self.cost_decrease_entry.update()
        self.o_and_m_costs_entry.update()
        self.embedded_emissions_entry.update()
        self.annual_emissions_decrease_entry.update()
        self.installation_emissions_entry.update()
        self.installation_emissions_decrease_entry.update()
        self.om_emissions_entry.update()


class PVTFrame(ttk.Frame):
    """
    Represents the PV-T frame.

    Contains settings for the PV-T units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="PV-T frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class SolarThermalFrame(ttk.Frame):
    """
    Represents the solar-thermal frame.

    Contains settings for the solar-thermal units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Solar-thermal frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class SolarFrame(ttk.Frame):
    """
    Represents the Solar frame.

    Contains settings for solar units.

    TODO: Update attributes.

    """

    def __init__(
        self, parent, data_directory: str, renewables_ninja_token: ttk.StringVar
    ):
        """
        Instantiate a :class:`PVFrame` instance.

        :param: parent
            The parent frame.

        :param: data_directory
            The name of the data directory being used.

        :param: renewables_ninja_token
            The renewables.ninja API token for the user.


        """

        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.solar_notebook = ttk.Notebook(self, bootstyle=WARNING)
        self.solar_notebook.grid(row=0, column=0, padx=20, pady=10, sticky="news")

        self.pv_frame = PVFrame(self, data_directory, renewables_ninja_token)
        self.solar_notebook.add(self.pv_frame, text="PV panels", sticky="news")

        self.pv_t_frame = PVTFrame(self)
        # self.solar_notebook.add(
        #     self.pv_t_frame, text="PV-T collectors", sticky="news", state=DISABLED
        # )

        self.solar_thermal_frame = SolarThermalFrame(self)
        # self.solar_notebook.add(
        #     self.solar_thermal_frame,
        #     text="Solar-thermal collectors",
        #     sticky="news",
        #     state=DISABLED,
        # )

        # TODO: Add configuration frame widgets and layout

    @property
    def pv_panels(self) -> list[dict[str, float | dict[str, float]]]:
        """
        Return a list of solar panels based on the information provided in the frame.

        :return:
            The solar panels based on the frame's information.


        """

        pv_panels: dict[list[dict[str, float | dict[str, float]]]] = {PANELS: []}

        for panel_name in self.pv_frame.panel_name_values:
            panel_dict = PVPanel(
                int(self.pv_frame.panel_orientation[panel_name].get()),
                self.pv_frame.panel_lifetimes[panel_name].get(),
                panel_name,
                self.pv_frame.nominal_power[panel_name].get(),
                True,
                self.pv_frame.reference_efficiencies[panel_name].get() / 100,
                self.pv_frame.reference_temperature[panel_name].get(),
                self.pv_frame.thermal_coefficient[panel_name].get(),
                int(self.pv_frame.panel_tilt[panel_name].get()),
                Tracking(int(self.pv_frame.tracking[panel_name].get())),
            ).as_dict

            # Append cost and emissions information
            panel_dict[COSTS] = {
                COST: self.pv_frame.costs[panel_name].get(),
                COST_DECREASE: -(self.pv_frame.cost_decrease[panel_name].get()),
                INSTALLATION_COST: self.pv_frame.installation_costs[panel_name].get(),
                INSTALLATION_COST_DECREASE: -(
                    self.pv_frame.installation_cost_decrease[panel_name].get()
                ),
                OM: self.pv_frame.o_and_m_costs[panel_name].get(),
            }

            panel_dict[EMISSIONS] = {
                GHGS: self.pv_frame.embedded_emissions[panel_name].get(),
                GHG_DECREASE: -(
                    self.pv_frame.annual_emissions_decrease[panel_name].get()
                ),
                INSTALLATION_GHGS: self.pv_frame.installation_emissions[
                    panel_name
                ].get(),
                INSTALLATION_GHGS_DECREASE: -(
                    self.pv_frame.installation_emissions_decrease[panel_name].get()
                ),
                OM_GHGS: self.pv_frame.om_emissions[panel_name].get(),
            }

            pv_panels[PANELS].append(panel_dict)

        return pv_panels

    def set_solar(
        self,
        pv_panels: list[PVPanel],
        pv_panel_costs: dict[str, dict[str, float]],
        pv_panel_emissions: dict[str, dict[str, float]],
    ) -> None:
        """
        Set the solar panel information for the frame based on the inputs provided.

        :param: pv_panels
            The `list` of :class:`solar.PVPanel` instances defined;

        :param: pv_panel_costs
            The pv-panel cost information

        :param: pv_panel_emissions
            The pv-panel emissions information;

        """

        self.pv_frame.set_solar(pv_panels, pv_panel_costs, pv_panel_emissions)
