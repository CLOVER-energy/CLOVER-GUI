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

import functools
import os
import tkinter as tk

from typing import Callable

import customtkinter as ctk
import ttkbootstrap as ttk

from clover import (
    DEFAULT_SCENARIO,
    DemandType,
    DieselMode,
    ProgrammerJudgementFault,
    ResourceType,
    Scenario,
)
from clover.__utils__ import DistributionNetwork, ELECTRIC_POWER
from clover.fileparser import BATTERY, DIESEL_GENERATOR, DieselMode, NAME, SCENARIOS
from clover.generation.solar import PVPanel
from clover.impact.finance import ImpactingComponent
from clover.simulation.diesel import DieselGenerator
from clover.simulation.energy_system import Minigrid
from clover.simulation.storage_utils import Battery
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.tooltip import ToolTip


__all__ = ("ConfigurationFrame",)


# Images directory name:
#   The name of the images directory.
_IMAGES_DIRECTORY: str = "images"


class ConfigurationFrame(ttk.Frame):
    """
    Represents the configuration frame.

    The configure frame contains toggles for configuration top-level settings for each
    run.

    TODO: Update attributes.

    """

    def __init__(
        self,
        parent,
        data_directory: str,
        help_image: ttk.PhotoImage,
        open_details_window: Callable,
        pv_icon_configuration_callback: Callable,
        storage_button_configuration_callback: Callable,
    ):
        super().__init__(parent)

        self.help_image = help_image
        self.open_details_window = open_details_window
        self.pv_icon_configuration_callback = pv_icon_configuration_callback
        self.storage_button_configuration_callback = (
            storage_button_configuration_callback
        )

        self.columnconfigure(0, weight=4)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=8, minsize=300)
        # self.pack(fill="both", expand=True)

        self.columnconfigure(0, weight=1, minsize=250)
        self.columnconfigure(1, weight=4)

        self.scrollable_scenario_frame = ScrolledFrame(self)
        self.scrollable_scenario_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=10,
            pady=5,
            ipady=0,
            ipadx=0,
            sticky="news",
        )

        self.scrollable_scenario_frame.columnconfigure(0, weight=1)
        self.scrollable_scenario_frame.columnconfigure(1, weight=1)
        self.scrollable_scenario_frame.columnconfigure(2, weight=1)
        self.scrollable_scenario_frame.columnconfigure(3, weight=1)
        self.scrollable_scenario_frame.columnconfigure(4, weight=1)

        self.scrollable_scenario_frame.rowconfigure(0, weight=1)
        self.scrollable_scenario_frame.rowconfigure(1, weight=1)
        self.scrollable_scenario_frame.rowconfigure(2, weight=1)
        self.scrollable_scenario_frame.rowconfigure(3, weight=1)
        self.scrollable_scenario_frame.rowconfigure(4, weight=1)
        self.scrollable_scenario_frame.rowconfigure(5, weight=1)
        self.scrollable_scenario_frame.rowconfigure(6, weight=1)
        self.scrollable_scenario_frame.rowconfigure(7, weight=1)
        self.scrollable_scenario_frame.rowconfigure(8, weight=1)
        self.scrollable_scenario_frame.rowconfigure(9, weight=1)
        self.scrollable_scenario_frame.rowconfigure(10, weight=1)
        self.scrollable_scenario_frame.rowconfigure(11, weight=1)
        self.scrollable_scenario_frame.rowconfigure(12, weight=1)
        self.scrollable_scenario_frame.rowconfigure(13, weight=1)
        self.scrollable_scenario_frame.rowconfigure(14, weight=1)
        self.scrollable_scenario_frame.rowconfigure(15, weight=1)
        self.scrollable_scenario_frame.rowconfigure(16, weight=1)
        self.scrollable_scenario_frame.rowconfigure(17, weight=1)

        # Style
        bold_head = ttk.Style()
        bold_head.configure("Bold.TLabel", font=("TkDefaultFont", 12, "bold"))

        # Scenario information helper
        self.scenario_label = ttk.Label(
            self, text="Configure your CLOVER scenario", style="Bold.TLabel"
        )
        self.scenario_label.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.scenario_information_icon = ttk.Label(
            self,
            bootstyle=INFO,
            image=self.help_image,
            text="",
        )
        self.scenario_information_icon.grid(
            row=0, column=0, padx=20, pady=20, sticky="e"
        )

        # self.scenario_information_text = ttk.Label(
        #     self,
        #     text="The secnario configures your CLOVER run. Here, you can toggle on "
        #     "and off various power-generation sources \nand sources of demand. You "
        #     "should check all the information on this screen before continuing to "
        #     "ensure \nthat your system is correctly represented.",
        # )
        self.scenario_information_tooltip = ToolTip(
            self.scenario_information_icon,
            text="The configure tab sets up your CLOVER run. Here, you can toggle on "
            "and off various power-generation sources and sources of demand. You "
            "should check all the information on this screen before continuing to "
            "ensure that your system is correctly represented.",
            bootstyle=f"{INFO}-{INVERSE}",
        )
        # self.scenario_information_text.grid(
        #     row=0, column=1, padx=20, pady=10, sticky="ew"
        # )

        # Horizontal separator
        # self.separator = ttk.Separator(
        #     self, orient="horizontal"
        # )
        # self.separator.grid(row=1, column=0, columnspan=2, pady=5, padx=10, sticky="")

        self.separator = ttk.Separator(self)
        self.separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(20, 20))

        # Selecting system components
        self.power_generation_label = ttk.Label(
            self.scrollable_scenario_frame, text="Power sources", style="Bold.TLabel"
        )
        self.power_generation_label.grid(
            row=0, column=0, columnspan=5, padx=10, pady=5, sticky="w"
        )

        # Component labels
        self.solar_label = ttk.Label(self.scrollable_scenario_frame, text="PV")
        self.solar_label.grid(row=0, column=1, rowspan=2, sticky="", pady=5)

        self.battery_label = ttk.Label(self.scrollable_scenario_frame, text="Battery")
        self.battery_label.grid(row=0, column=2, rowspan=2, sticky="", pady=5)

        self.diesel_label = ttk.Label(self.scrollable_scenario_frame, text="Diesel")
        self.diesel_label.grid(row=0, column=3, rowspan=2, sticky="", pady=5)

        self.grid_label = ttk.Label(self.scrollable_scenario_frame, text="Grid")
        self.grid_label.grid(row=0, column=4, rowspan=2, sticky="", pady=5)

        # Explainer label
        self.explainer_power_generation_label = ttk.Label(
            self.scrollable_scenario_frame,
            text="Select power sources \n" "and adjust settings\n" "and components. \n"
            # "Detailed settings can be \n"
            # "adjusted by clicking the\n"
            # "buttons below the \n"
            # "coloured icons.",
        )
        self.explainer_power_generation_label.grid(
            row=2, column=0, padx=10, pady=5, sticky="nsw"
        )
        self.power_source_used_label = ttk.Label(
            self.scrollable_scenario_frame, text="Toggle power sources\n" " on or off"
        )
        self.power_source_used_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.power_source_settings_label = ttk.Label(
            self.scrollable_scenario_frame,
            text="Open advanced settings \n" "for each power source"
            # "adjusted by clicking\n"
            # "respective settings buttons\n"
        )
        self.power_source_settings_label.grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )

        self.component_selection_label = ttk.Label(
            self.scrollable_scenario_frame, text="Component selection"
        )
        self.component_selection_label.grid(
            row=5, column=0, padx=10, pady=5, sticky="w"
        )

        self.solar_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory,
                    _IMAGES_DIRECTORY,
                    "solar_gui_selected.png",
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY, "solar_gui_disabled.png"
                )
            ),
        }
        self.solar_pv_selected: ttk.BooleanVar = ttk.BooleanVar(self, value=False)

        self.pv_icon = ttk.Label(
            master=self.scrollable_scenario_frame,
            image=self.solar_images[self.solar_pv_selected.get()],
        )
        self.pv_icon.grid(row=1, column=1, rowspan=2, padx=10)

        # self.pv_label = ttk.Label(
        #     self.scrollable_scenario_frame,
        #     text="PV",
        #     bootstyle=INFO,
        # )
        # self.pv_label.grid(row=0, column=1, rowspan=2, sticky="w")

        # # PV On/Off buttons
        # self.PV_true_button = ttk.Checkbutton(
        #     self.scrollable_scenario_frame,
        #     variable=self.solar_pv_selected,
        #     command=self.pv_button_callback,
        #     bootstyle=f"{INFO}-{TOOLBUTTON}",
        #     text="ON",
        # )
        # self.PV_true_button.grid(
        #     row=2, column=1, padx=60, pady=10, sticky="w"
        # )
        # self.PV_false_button = ttk.Checkbutton(
        #     self.scrollable_scenario_frame,
        #     variable=self.solar_pv_selected,
        #     command=self.pv_button_callback,
        #     bootstyle=f"{INFO}-{TOOLBUTTON}",
        #     text="OFF",
        # )
        # self.PV_false_button.grid(
        #     row=2, column=1, padx=60, pady=10, sticky="e"
        # )
        # Battery on off button
        self.pv_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            command=self.pv_button_callback,
            text="On / Off",
            variable=self.solar_pv_selected,
        )
        self.pv_switch.grid(row=3, column=1, pady=10, sticky="")

        self.pv_tooltip = ToolTip(
            self.pv_switch,
            text="Toggle whether PV collectors are present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

        # PV panel selection
        self.pv_panel = ttk.StringVar(self, "")
        self.pv_panel_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
            values=[],
            state=READONLY,
            bootstyle=INFO,
            textvariable=self.pv_panel,
            width=5,
        )
        self.pv_panel_combobox.grid(row=5, column=1, padx=20, pady=5, sticky="ew")

        self.pv_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="PV settings",
            bootstyle=INFO,
            command=self.open_pv_settings,
        )
        self.pv_settings_button.grid(row=4, column=1, padx=50, sticky="ew")

        self.pv_settings_tooltip = ToolTip(
            self.pv_settings_button,
            text="Opens the detailed settings for configuring PV collectors",
        )

        self.battery_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY, "battery_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY, "battery_gui_disabled.png"
                )
            ),
        }
        self.battery_selected: ttk.BooleanVar = ttk.BooleanVar(self, value=False)
        self.battery_icon = ttk.Label(
            master=self.scrollable_scenario_frame,
            image=self.battery_images[self.battery_selected.get()],
        )
        self.battery_icon.grid(row=1, column=2, rowspan=2, pady=5, padx=10, sticky="")

        # Battery On/Off buttons
        # self.battery_true_button = ttk.Checkbutton(
        #     self.scrollable_scenario_frame,
        #     variable=self.solar_pv_selected,
        #     command=self.pv_button_callback,
        #     bootstyle=f"{INFO}-{TOOLBUTTON}",
        #     text="ON",
        # )
        # self.battery_true_button.grid(
        #     row=2, column=2, padx=70, pady=10, sticky="w"
        # )
        # self.battery_false_button = ttk.Checkbutton(
        #     self.scrollable_scenario_frame,
        #     variable=self.solar_pv_selected,
        #     command=self.pv_button_callback,
        #     bootstyle=f"{INFO}-{TOOLBUTTON}",
        #     text="OFF",
        # )
        # self.battery_false_button.grid(
        #     row=2, column=2, padx=70, pady=10, sticky="e"
        # )
        # On off radio button
        self.battery_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            command=self.battery_button_callback,
            text="On / Off",
            variable=self.battery_selected,
        )
        self.battery_switch.grid(row=3, column=2, pady=10, sticky="")

        self.battery_tooltip = ToolTip(
            self.battery_switch,
            text="Toggle whether electric batteries are present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

        self.battery_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Battery settings",
            bootstyle=INFO,
            command=self.open_battery_settings,
        )
        self.battery_settings_button.grid(row=4, column=2, padx=20)

        self.battery_settings_tooltip = ToolTip(
            self.battery_settings_button,
            text="Opens the detailed settings for configuring batteries",
        )
        # Battery selection
        self.battery = ttk.StringVar(self, "")
        self.battery_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
            values=[],
            state=READONLY,
            bootstyle=INFO,
            textvariable=self.battery,
            width=5,
        )
        self.battery_combobox.grid(row=5, column=2, pady=5, padx=30, sticky="ew")

        self.diesel_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY, "diesel_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY, "diesel_gui_disabled.png"
                )
            ),
        }
        self.diesel_selected: ttk.BooleanVar = ttk.BooleanVar(self, value=False)
        self.diesel_button = ttk.Label(
            master=self.scrollable_scenario_frame,
            image=self.diesel_images[self.diesel_selected.get()],
        )
        self.diesel_button.grid(row=1, column=3, rowspan=2, pady=5, padx=10)

        self.diesel_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            command=self.diesel_button_callback,
            text="On / Off",
            variable=self.diesel_selected,
        )
        self.diesel_switch.grid(row=3, column=3, pady=10, sticky="")

        self.diesel_tooltip = ToolTip(
            self.diesel_switch,
            text="Toggle whether backup diesel power is present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

        self.diesel_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Diesel settings",
            bootstyle=INFO,
            command=self.open_diesel_settings,
        )
        self.diesel_settings_button.grid(row=4, column=3, padx=20)
        self.diesel_settings_tooltip = ToolTip(
            self.diesel_settings_button,
            text="Opens the detailed settings for configuring diesel generators",
        )
        # Diesel selection
        self.diesel_generator = ttk.StringVar(self, "")
        self.diesel_generator_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
            values=[],
            state=READONLY,
            bootstyle=INFO,
            textvariable=self.diesel_generator,
            width=5,
        )
        self.diesel_generator_combobox.grid(
            row=5, column=3, pady=5, padx=30, sticky="ew"
        )

        self.grid_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY, "grid_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY, "grid_gui_disabled.png"
                )
            ),
        }
        self.grid_selected: ttk.BooleanVar = ttk.BooleanVar(self, value=False)
        self.grid_icon = ttk.Label(
            master=self.scrollable_scenario_frame,
            image=self.grid_images[self.grid_selected.get()],
        )
        self.grid_icon.grid(row=1, column=4, rowspan=2, pady=5, padx=10)

        self.grid_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            command=self.grid_button_callback,
            text="On / Off",
            variable=self.grid_selected,
        )
        self.grid_switch.grid(row=3, column=4, pady=10, sticky="")

        self.grid_tooltip = ToolTip(
            self.grid_switch,
            text="Toggle whether backup a grid connection is present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

        # Grid selection
        self.grid_profile_name = ttk.StringVar(self, "")
        self.grid_profile_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
            values=[],
            state=READONLY,
            bootstyle=INFO,
            textvariable=self.grid_profile_name,
            width=5,
        )
        self.grid_profile_combobox.grid(row=5, column=4, pady=5, padx=30, sticky="ew")

        self.grid_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Grid settings",
            bootstyle=INFO,
            command=self.open_grid_settings,
        )
        self.grid_settings_button.grid(row=4, column=4, padx=20)

        self.grid_settings_tooltip = ToolTip(
            self.grid_settings_button,
            text="Opens the detailed settings for configuring the probability of the "
            "grid being available.",
        )
        # Empty line
        self.empty_line = ttk.Label(self.scrollable_scenario_frame, text="")
        self.empty_line.grid(row=6, column=0, columnspan=5, pady=5, padx=10)

        # Horizontal separator
        self.separator = ttk.Separator(
            self.scrollable_scenario_frame, orient="horizontal"
        )
        self.separator.grid(row=7, column=0, columnspan=5, pady=5, padx=10, sticky="ew")

        # Resource types selection
        self.resource_images: dict[ResourceType, dict[bool, ttk.PhotoImage]] = {
            ResourceType.ELECTRIC: {
                True: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory,
                        _IMAGES_DIRECTORY,
                        "electric_gui_selected_filled.png",
                    )
                ),
                False: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory,
                        _IMAGES_DIRECTORY,
                        "electric_gui_selected_outline.png",
                    )
                ),
            },
            ResourceType.HOT_CLEAN_WATER: {
                True: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory,
                        _IMAGES_DIRECTORY,
                        "hot_water_gui_selected_filled.png",
                    )
                ),
                False: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory,
                        _IMAGES_DIRECTORY,
                        "hot_water_gui_selected_outline.png",
                    )
                ),
            },
            ResourceType.CLEAN_WATER: {
                True: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory, "images", "clean_water_gui_selected_filled.png"
                    )
                ),
                False: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory, "images", "clean_water_gui_selected_outline.png"
                    )
                ),
            },
        }

        self.resource_selected: dict[ResourceType : ttk.BooleanVar] = {
            ResourceType.ELECTRIC: ttk.BooleanVar(self, value=True),
            ResourceType.HOT_CLEAN_WATER: ttk.BooleanVar(self, value=False),
            ResourceType.CLEAN_WATER: ttk.BooleanVar(self, value=False),
        }

        self.electric_power_label: ttk.Label = ttk.Label(
            self.scrollable_scenario_frame,
            text="Electricity demand",
            style="Bold.TLabel",
        )
        self.electric_power_label.grid(
            row=8, column=0, columnspan=5, padx=10, pady=5, sticky="w"
        )

        # Demand type headings
        self.domestic_demand_header = ttk.Label(
            self.scrollable_scenario_frame,
            text="Domestic",
        )
        self.domestic_demand_header.grid(row=8, column=1, padx=10, pady=5, sticky="")

        self.commercial_demand_header = ttk.Label(
            self.scrollable_scenario_frame, text="Commercial"
        )
        self.commercial_demand_header.grid(row=8, column=2, padx=10, pady=5, sticky="")

        self.public_demand_header = ttk.Label(
            self.scrollable_scenario_frame, text="Public"
        )
        self.public_demand_header.grid(row=8, column=3, padx=10, pady=5, sticky="")

        self.electric_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.resource_button_callback, ResourceType.ELECTRIC
            ),
            fg_color="transparent",
            image=self.resource_images[ResourceType.ELECTRIC][
                self.resource_selected[ResourceType.ELECTRIC].get()
            ],
            hover_color=NONE,
            text="",
            state=DISABLED,
        )

        # Demand explainer
        self.demand_explainer = ttk.Label(
            self.scrollable_scenario_frame,
            text="Select electricity demand\n"
            "types used. Select\n"
            "'Demand settings' for,\n"
            "further options",
        )
        self.demand_explainer.grid(row=9, column=0, pady=5, padx=10, sticky="nsw")

        self.demand_toggle_explainer = ttk.Label(
            self.scrollable_scenario_frame, text="Toggle demand types\n" " on or off"
        )
        self.demand_toggle_explainer.grid(
            row=10, column=0, pady=5, rowspan=2, padx=10, sticky="w"
        )
        # self.electric_button.grid(row=8, column=1, pady=5, padx=10, sticky="")
        # self.electric_button_tooltip = ToolTip(
        #     self.electric_button,
        #     text="Toggles whether electric power demands are included when generating "
        #     "stochastic demand profiles.",
        #     bootstyle=f"{WARNING}-{INVERSE}",
        # )

        self.hot_water_power_label: ttk.Label = ttk.Label(
            self.scrollable_scenario_frame, text="Hot-water demand"
        )
        # self.hot_water_power_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.hot_water_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.resource_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.resource_images[ResourceType.HOT_CLEAN_WATER][
                self.resource_selected[ResourceType.HOT_CLEAN_WATER].get()
            ],
            text="",
        )
        # self.hot_water_button.grid(row=4, column=1, pady=5, padx=10, sticky="")
        # self.hot_water_button_tooltip = ToolTip(
        #     self.hot_water_button,
        #     text="Toggles whether hot-water demands are included when generating "
        #     "stochastic demand profiles.",
        #     bootstyle=f"{DANGER}-{INVERSE}",
        # )

        self.clean_water_power_label: ttk.Label = ttk.Label(
            self.scrollable_scenario_frame, text="Clean-water demand"
        )
        # self.clean_water_power_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.clean_water_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.resource_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.resource_images[ResourceType.CLEAN_WATER][
                self.resource_selected[ResourceType.CLEAN_WATER].get()
            ],
            text="",
        )
        # self.clean_water_button.grid(row=5, column=1, pady=5, padx=10, sticky="")
        # self.clean_water_button_tooltip = ToolTip(
        #     self.clean_water_button,
        #     text="Toggles whether clean-water demands are included when generating "
        #     "stochastic demand profiles.",
        #     bootstyle=f"{PRIMARY}-{INVERSE}",
        # )

        self.resource_buttons: dict[ResourceType, ctk.CTkButton] = {
            ResourceType.ELECTRIC: self.electric_button,
            ResourceType.HOT_CLEAN_WATER: self.hot_water_button,
            ResourceType.CLEAN_WATER: self.clean_water_button,
        }

        self.domestic_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY, "domestic_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory,
                    _IMAGES_DIRECTORY,
                    "domestic_gui_disabled.png",
                )
            ),
        }
        self.domestic_button_disabled_image: ttk.PhotoImage = ttk.PhotoImage(
            file=os.path.join(data_directory, "images", "domestic_gui_disabled.png")
        )

        self.commercial_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, "images", "commercial_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, "images", "commercial_gui_disabled.png"
                )
            ),
        }
        self.commercial_button_disabled_image: ttk.PhotoImage = ttk.PhotoImage(
            file=os.path.join(data_directory, "images", "commercial_gui_disabled.png")
        )

        self.public_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(data_directory, "images", "public_gui_selected.png")
            ),
            False: ttk.PhotoImage(
                file=os.path.join(data_directory, "images", "public_gui_disabled.png")
            ),
        }
        self.public_button_disabled_image: ttk.PhotoImage = ttk.PhotoImage(
            file=os.path.join(data_directory, "images", "public_gui_disabled.png")
        )

        # Domestic buttons
        self.domestic_selected: dict[ResourceType, ttk.BooleanVar] = {
            ResourceType.ELECTRIC: ttk.BooleanVar(self, value=False),
            ResourceType.HOT_CLEAN_WATER: ttk.BooleanVar(self, value=False),
            ResourceType.CLEAN_WATER: ttk.BooleanVar(self, value=False),
        }
        self.electric_domestic_label = ttk.Label(
            master=self.scrollable_scenario_frame,
            image=self.domestic_images[
                self.domestic_selected[ResourceType.ELECTRIC].get()
            ],
        )
        self.electric_domestic_label.grid(row=9, column=1, pady=5, padx=10, sticky="")
        self.electric_domestic_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            command=functools.partial(
                self.domestic_button_callback, ResourceType.ELECTRIC
            ),
            text="On / Off",
            variable=self.domestic_selected[ResourceType.ELECTRIC],
        )
        self.electric_domestic_switch.grid(row=10, column=1, pady=10, sticky="")
        self.electric_domestic_button_tooltip = ToolTip(
            self.electric_domestic_switch,
            text="Toggles whether domestic electric demands are included when "
            "generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )

        self.hot_water_domestic_label = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.domestic_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.domestic_button_disabled_image,
            text="",
        )
        # self.hot_water_domestic_label.grid(row=4, column=2, pady=5, padx=10, sticky="")
        # self.hot_water_domestic_label_tooltip = ToolTip(
        #     self.hot_water_domestic_label,
        #     text="Toggles whether domestic hot-water demands are included when "
        #     "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{DANGER}",
        # )

        self.clean_water_domestic_label = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.domestic_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.domestic_button_disabled_image,
            text="",
        )
        # self.clean_water_domestic_label.grid(
        #     row=5, column=2, pady=5, padx=10, sticky=""
        # )
        # self.clean_water_domestic_label_tooltip = ToolTip(
        #     self.clean_water_domestic_label,
        #     text="Toggles whether domestic clean-water demands are included when "
        #     generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{PRIMARY}",
        # )

        self.domestic_labels: dict[ResourceType, ctk.CTkButton] = {
            ResourceType.ELECTRIC: self.electric_domestic_label,
            ResourceType.HOT_CLEAN_WATER: self.hot_water_domestic_label,
            ResourceType.CLEAN_WATER: self.clean_water_domestic_label,
        }

        # Commercial buttons
        self.commercial_selected: dict[ResourceType, ttk.BooleanVar] = {
            ResourceType.ELECTRIC: ttk.BooleanVar(self, value=False),
            ResourceType.HOT_CLEAN_WATER: ttk.BooleanVar(self, value=False),
            ResourceType.CLEAN_WATER: ttk.BooleanVar(self, value=False),
        }

        self.electric_commercial_label = ttk.Label(
            master=self.scrollable_scenario_frame,
            image=self.commercial_images[
                self.commercial_selected[ResourceType.ELECTRIC].get()
            ],
        )
        self.electric_commercial_label.grid(row=9, column=2, pady=5, padx=10)
        self.electric_commercial_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            command=functools.partial(
                self.commercial_button_callback, ResourceType.ELECTRIC
            ),
            text="On / Off",
            variable=self.commercial_selected[ResourceType.ELECTRIC],
        )
        self.electric_commercial_switch.grid(row=10, column=2, pady=10, sticky="")
        self.electric_commercial_button_tooltip = ToolTip(
            self.electric_commercial_switch,
            text="Toggles whether commercial electricity demands are included when "
            "generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )

        self.hot_water_commercial_label = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.commercial_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.commercial_button_disabled_image,
            text="",
        )
        # self.hot_water_commercial_label.grid(row=4, column=3, pady=5, padx=10)
        # self.hot_water_commercial_label_tooltip = ToolTip(
        #     self.hot_water_commercial_label,
        #     text="Toggles whether commercial hot-water demands are included when "
        #     "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{DANGER}",
        # )

        self.clean_water_commercial_label = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.commercial_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.commercial_button_disabled_image,
            text="",
        )
        # self.clean_water_commercial_label.grid(row=5, column=3, pady=5, padx=10)
        # self.clean_water_commercial_label_tooltip = ToolTip(
        #     self.clean_water_commercial_label,
        #     text="Toggles whether commercial clean-water demands are included when "
        #     "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{PRIMARY}",
        # )

        self.commercial_labels: dict[ResourceType, ctk.CTkButton] = {
            ResourceType.ELECTRIC: self.electric_commercial_label,
            ResourceType.HOT_CLEAN_WATER: self.hot_water_commercial_label,
            ResourceType.CLEAN_WATER: self.clean_water_commercial_label,
        }

        # Public buttons
        self.public_selected: dict[ResourceType, ttk.BooleanVar] = {
            ResourceType.ELECTRIC: ttk.BooleanVar(self, value=False),
            ResourceType.HOT_CLEAN_WATER: ttk.BooleanVar(self, value=False),
            ResourceType.CLEAN_WATER: ttk.BooleanVar(self, value=False),
        }

        self.electric_public_label = ttk.Label(
            master=self.scrollable_scenario_frame,
            image=self.public_images[self.public_selected[ResourceType.ELECTRIC].get()],
        )
        self.electric_public_label.grid(row=9, column=3, pady=5, padx=10)
        self.electric_public_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            command=functools.partial(
                self.public_button_callback, ResourceType.ELECTRIC
            ),
            text="On / Off",
            variable=self.public_selected[ResourceType.ELECTRIC],
        )
        self.electric_public_switch.grid(row=10, column=3, pady=10, sticky="")
        self.electric_public_button_tooltip = ToolTip(
            self.electric_public_switch,
            text="Toggles whether public electricity demands are included when "
            "generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )

        self.hot_water_public_label = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.public_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.public_button_disabled_image,
            text="",
        )
        # self.hot_water_public_label.grid(row=4, column=4, pady=5, padx=10)
        # self.hot_water_public_label_tooltip = ToolTip(
        #     self.hot_water_public_label,
        #     text="Toggles whether public hot-water demands are included when "
        #     "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{DANGER}",
        # )

        self.clean_water_public_label = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.public_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.public_button_disabled_image,
            text="",
        )
        # self.clean_water_public_label.grid(row=5, column=4, pady=5, padx=10)
        # self.clean_water_public_label_tooltip = ToolTip(
        #     self.clean_water_public_label,
        #     text="Toggles whether public clean-water demands are included when "
        #    "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{PRIMARY}",
        # )

        self.public_labels: dict[ResourceType, ctk.CTkButton] = {
            ResourceType.ELECTRIC: self.electric_public_label,
            ResourceType.HOT_CLEAN_WATER: self.hot_water_public_label,
            ResourceType.CLEAN_WATER: self.clean_water_public_label,
        }

        self.demand_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Demand settings",
            bootstyle=INFO,
            command=self.open_load_settings,
        )
        self.demand_settings_button.grid(row=9, column=4, padx=20)

        # Row with a horizontal separator
        self.separator = ttk.Separator(
            self.scrollable_scenario_frame, orient="horizontal"
        )
        self.separator.grid(
            row=12, column=0, pady=5, padx=10, columnspan=5, sticky="news"
        )

        # Empty row
        self.empty_row = ttk.Frame(self.scrollable_scenario_frame)
        self.empty_row.grid(
            row=11, column=0, pady=5, padx=10, columnspan=5, sticky="news"
        )

        # Diesel scenario information
        # self.diesel_label_frame = ttk.Labelframe(
        #     self.scrollable_scenario_frame, bootstyle=DANGER, text="Diesel"
        # )
        # self.diesel_label_frame.grid(
        #     row=6, column=0, padx=10, pady=5, columnspan=5, sticky="news"
        # )

        # self.diesel_label_frame.columnconfigure(0, weight=1)
        # self.diesel_label_frame.columnconfigure(1, weight=1)
        # self.diesel_label_frame.columnconfigure(2, weight=1)
        # self.diesel_label_frame.columnconfigure(3, weight=1)

        # Other scenario settings header
        self.other_settings_label = ttk.Label(
            self.scrollable_scenario_frame,
            text="Other Scenario Settings",
            style="Bold.TLabel",
        )
        self.other_settings_label.grid(
            row=13, column=0, padx=10, pady=5, columnspan=5, sticky="w"
        )

        self.other_settings_explainer = ttk.Label(
            self.scrollable_scenario_frame,
            text="Miscellaneous settings\n"
            "for scenarios including\n"
            "grid-prioritisation and\n"
            "diesel-generator settings.",
        )
        self.other_settings_explainer.grid(
            row=14, column=0, pady=5, rowspan=3, padx=10, sticky="nsw"
        )

        # Diesel mode
        # self.diesel_mode_label = ttk.Label(
        #     self.scrollable_scenario_frame, text="Diesel mode"
        # )
        # # self.diesel_mode_label.grid(row=8, column=0, padx=10, pady=5, sticky="w")

        # self.diesel_mode_combobox = ttk.Combobox(
        #     self.scrollable_scenario_frame, state=DISABLED, width=10
        # )
        # # self.diesel_mode_combobox.grid(row=8, column=1, padx=10, pady=5, sticky="ew")
        # self.diesel_mode_combobox["values"] = [e.value for e in DieselMode]
        # self.diesel_mode_combobox.set(DieselMode.BACKUP.value)

        # Backup threshold
        self.diesel_backup_threshold_label = ttk.Label(
            self.scrollable_scenario_frame, text="Diesel threshold"
        )
        self.diesel_backup_threshold_label.grid(
            row=14, column=1, padx=10, pady=5, sticky="w"
        )

        self.diesel_backup_threshold: ttk.IntVar = ttk.DoubleVar(self, 0)

        def scalar_threshold(_):
            self.diesel_backup_threshold.set(
                round(self.diesel_backup_threshold.get(), 1)
            )
            self.diesel_backup_entry.update()

        self.diesel_backup_slider = ttk.Scale(
            self.scrollable_scenario_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            # length=320,
            command=scalar_threshold,
            variable=self.diesel_backup_threshold,
        )
        self.diesel_backup_slider.grid(row=14, column=2, padx=10, pady=5, sticky="ew")

        def enter_threshold(_):
            self.diesel_backup_threshold.set(
                round(min(max(float(self.diesel_backup_entry.get()), 0), 100), 2)
            )
            self.diesel_backup_slider.set(self.diesel_backup_entry.get())
            self.diesel_backup_entry.update()

        self.diesel_backup_entry = ttk.Entry(
            self.scrollable_scenario_frame,
            textvariable=self.diesel_backup_threshold,
        )
        self.diesel_backup_entry.grid(row=14, column=3, padx=10, pady=5, sticky="ew")
        self.diesel_backup_entry.bind("<Return>", enter_threshold)

        self.diesel_backup_threshold_unit = ttk.Label(
            self.scrollable_scenario_frame, text=f"% of hours"
        )
        self.diesel_backup_threshold_unit.grid(
            row=14, column=4, padx=10, pady=5, sticky="w"
        )

        # Distribution network
        # self.generation_and_distribution_label_frame = ttk.Labelframe(
        #     self.scrollable_scenario_frame,
        #     bootstyle=SUCCESS,
        #     text="Generation and distribution",
        # )
        # self.generation_and_distribution_label_frame.grid(
        #     row=8, column=0, padx=10, pady=5, sticky="news", columnspan=5
        # )

        # self.generation_and_distribution_label_frame.columnconfigure(0, weight=1)
        # self.generation_and_distribution_label_frame.columnconfigure(1, weight=1)
        # self.generation_and_distribution_label_frame.columnconfigure(2, weight=1)
        # self.generation_and_distribution_label_frame.columnconfigure(3, weight=1)

        self.distribution_network_label = ttk.Label(
            self.scrollable_scenario_frame, text="Distribution network"
        )
        self.distribution_network_label.grid(
            row=15, column=1, padx=10, pady=5, sticky="w"
        )

        self.distribution_network_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
        )
        self.distribution_network_combobox.grid(
            row=15, column=2, padx=10, pady=5, sticky="w"
        )
        self.distribution_network_combobox["values"] = [
            e.value for e in DistributionNetwork
        ]
        self.distribution_network_combobox.set(DistributionNetwork.DC.value)

        # Self generation
        self.prioritise_self_generation_label = ttk.Label(
            self.scrollable_scenario_frame,
            text="Prioritise self\n" "generation",
        )
        self.prioritise_self_generation_label.grid(
            row=16, column=1, padx=10, pady=5, sticky="w"
        )

        self.prioritise_self_generation_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
        )
        self.prioritise_self_generation_combobox.grid(
            row=16, column=2, padx=10, pady=5, sticky="w"
        )
        self.prioritise_self_generation_combobox["values"] = ["True", "False"]
        self.prioritise_self_generation_combobox.set("True")

    @property
    def energy_system_dict(
        self,
    ) -> dict[str, list[dict[str, bool | dict[str, float] | list[str] | str]]]:
        """
        Outputs the energy-system-related scenario information in `dict` ready to save.

        """

        return {
            BATTERY: self.battery_combobox.get(),
            DIESEL_GENERATOR: self.diesel_generator_combobox.get(),
            "pv_panel": self.pv_panel_combobox.get(),
        }

    @property
    def scenarios_dict(
        self,
    ) -> dict[str, list[dict[str, bool | dict[str, float] | list[str] | str]]]:
        """
        Outputs the scenario information in a `dict` ready for saving.

        :returns:
            The scenario information as a `dict` ready for saving.

        """

        # Determine the available resource types.
        resource_types: list[str] = []
        for resource in ResourceType:
            if self.resource_selected.get(resource, ttk.BooleanVar(self, False)).get():
                if resource != ResourceType.ELECTRIC:
                    resource_types.append(resource.value)
                else:
                    resource_types.append(ELECTRIC_POWER)

        return {
            SCENARIOS: [
                {
                    NAME: DEFAULT_SCENARIO,
                    BATTERY: self.battery_selected.get(),
                    "demands": {
                        DemandType.DOMESTIC.value: self.domestic_selected[
                            ResourceType.ELECTRIC
                        ].get(),
                        DemandType.COMMERCIAL.value: self.commercial_selected[
                            ResourceType.ELECTRIC
                        ].get(),
                        DemandType.PUBLIC.value: self.public_selected[
                            ResourceType.ELECTRIC
                        ].get(),
                    },
                    "diesel": {
                        # "mode": self.diesel_mode_combobox.get()
                        "mode": DieselMode.BACKUP.value
                        if self.diesel_selected.get()
                        else DieselMode.DISABLED.value,
                        DieselMode.BACKUP.value: {
                            "threshold": float(self.diesel_backup_threshold.get()) / 100
                        },
                    },
                    "distribution_network": self.distribution_network_combobox.get(),
                    ImpactingComponent.GRID.value: self.grid_selected.get(),
                    "grid_type": self.grid_profile_combobox.get(),
                    # FIXME: Implement a fixed inverter size.
                    "fixed_inverter_size": False,
                    "prioritise_self_generation": self.prioritise_self_generation_combobox.get(),
                    ImpactingComponent.PV.value: self.solar_pv_selected.get(),
                    "resource_types": resource_types,
                }
            ]
        }

    def add_battery(self, battery_name: str) -> None:
        """
        Add a battery to the list of selectable options.

        :param: battery_name
            The name of the battery to add.

        """

        self.battery_combobox["values"] = self.battery_combobox["values"] + (
            battery_name,
        )

    def add_diesel_generator(self, diesel_generator_name: str) -> None:
        """
        Add a diesel generator to the list of selectable options.

        :param: diesel_generator_name
            The name of the diesel generator to add.

        """

        self.diesel_generator_combobox["values"] = self.diesel_generator_combobox[
            "values"
        ] + (diesel_generator_name,)

    def add_pv_panel(self, pv_panel_name: str) -> None:
        """
        Add a solar panel to the list of selectable options.

        :param: pv_panel_name
            The name of the PV panel to add.

        """

        self.pv_panel_combobox["values"] = self.pv_panel_combobox["values"] + (
            pv_panel_name,
        )

    def add_grid_profile(self, grid_profile_name: str) -> None:
        """
        Add a grid profile to the list of selectable options.

        :param: grid_profile_name
            The name of the grid profile to add.

        """

        if not isinstance(self.grid_profile_combobox["values"], tuple):
            self.grid_profile_combobox["values"] = (grid_profile_name,)
            return

        self.grid_profile_combobox["values"] = self.grid_profile_combobox["values"] + (
            grid_profile_name,
        )

    def set_batteries(self, battery_names: list[str]) -> None:
        """
        Set the names of the batteries in the combobox.

        :param: battery_names
            The `list` of battery names to set.

        """

        self.battery_combobox["values"] = battery_names
        if self.battery_combobox.get() not in battery_names:
            self.battery_combobox.set(battery_names[0])

    def set_diesel_generators(self, generator_names: list[str]) -> None:
        """
        Set the names of the generators in the combobox.

        :param: generator_names
            The `list` of diesel generator names to set.

        """

        self.diesel_generator_combobox["values"] = generator_names
        if self.diesel_generator_combobox.get() not in generator_names:
            self.diesel_generator_combobox.set(generator_names[0])

    def set_pv_panels(self, panel_names: list[str]) -> None:
        """
        Set the names of the panel in the combobox.

        :param: panel_names
            The `list` of panel names to set.

        """

        self.pv_panel_combobox["values"] = panel_names
        if self.pv_panel_combobox.get() not in panel_names:
            self.pv_panel_combobox.set(panel_names[0])

    def set_grid_profiles(self, grid_profile_names: list[str]) -> None:
        """
        Set the names of the grid profiles in the combobox.

        :param: grid_profile_names
            The `list` of grid-profile names to set.

        """

        self.grid_profile_combobox[(_values := "values")] = grid_profile_names
        if self.grid_profile_combobox.get() not in grid_profile_names:
            self.grid_profile_combobox.set(grid_profile_names[0])

    def update_diesel_settings(self) -> None:
        """Updates the diesel settings sliders."""

        # Update the backup threshold accordingly
        if self.diesel_selected.get():
            self.diesel_backup_entry.configure(state="enabled")
            self.diesel_backup_slider.configure(state="enabled")
        else:
            self.diesel_backup_entry.configure(state=DISABLED)
            self.diesel_backup_slider.configure(state=DISABLED)

    def pv_button_callback(self):
        """Function called when the PV toggle is pressed"""
        # Update the icon
        self.pv_icon.configure(image=self.solar_images[self.solar_pv_selected.get()])
        self.pv_icon_configuration_callback(self.solar_pv_selected.get())

    def battery_button_callback(self):
        """Function called when the battery toggle is pressed"""
        # Update the icon
        self.battery_icon.configure(
            image=self.battery_images[self.battery_selected.get()]
        )
        self.storage_button_configuration_callback(self.battery_selected.get())

    def diesel_button_callback(self):
        """Function called when the diesel toggle is pressed"""
        # Update the icon
        self.diesel_button.configure(
            image=self.diesel_images[self.diesel_selected.get()]
        )

        # Update the scenario diesel settings pane
        self.update_diesel_settings()

    def grid_button_callback(self):
        """Function called when the grid toggle is pressed"""
        # Update the icon
        self.grid_icon.configure(image=self.grid_images[self.grid_selected.get()])

    def resource_button_callback(self, resource_type: ResourceType):
        """
        Callback for when a resource type is toggled on or off.

        :param: resource_type
            The resource being toggled.

        """

        self.resource_selected[resource_type].set(
            not self.resource_selected[resource_type].get()
        )
        self.resource_buttons[resource_type].configure(
            image=self.resource_images[resource_type][
                self.resource_selected[resource_type].get()
            ]
        )

        # If loads are enabled, colour these buttons in
        if self.resource_selected[resource_type].get():
            self.domestic_labels[resource_type].configure(
                image=self.domestic_images[self.domestic_selected[resource_type].get()]
            )
            self.commercial_labels[resource_type].configure(
                image=self.commercial_images[
                    self.commercial_selected[resource_type].get()
                ]
            )
            self.public_labels[resource_type].configure(
                image=self.public_images[self.public_selected[resource_type].get()]
            )
        else:
            self.domestic_labels[resource_type].configure(
                image=self.domestic_button_disabled_image
            )
            self.commercial_labels[resource_type].configure(
                image=self.commercial_button_disabled_image
            )
            self.public_labels[resource_type].configure(
                image=self.public_button_disabled_image
            )

    def domestic_button_callback(self, resource_type: ResourceType) -> None:
        """
        Callback function for when a domestic-load toggle is switched.

        :param: resource_type
            The resource type to switch the load for.

        """
        if not self.resource_selected[resource_type].get():
            return

        self.domestic_labels[resource_type].configure(
            image=self.domestic_images[self.domestic_selected[resource_type].get()]
        )

    def commercial_button_callback(self, resource_type: ResourceType) -> None:
        """
        Callback function for when a commercial-load toggle is switched.

        :param: resource_type
            The resource type to switch the load for.

        """

        if not self.resource_selected[resource_type].get():
            return

        self.commercial_labels[resource_type].configure(
            image=self.commercial_images[self.commercial_selected[resource_type].get()]
        )

    def public_button_callback(self, resource_type: ResourceType) -> None:
        """
        Callback function for when a public-load toggle is switched.

        :param: resource_type
            The resource type to switch the load for.

        """

        # Return if electric loads are not selected
        if not self.resource_selected[resource_type].get():
            return

        self.public_labels[resource_type].configure(
            image=self.public_images[self.public_selected[resource_type].get()]
        )

    def open_pv_settings(self) -> None:
        self.open_details_window(0)

    def open_diesel_settings(self) -> None:
        self.open_details_window(3)

    def open_battery_settings(self) -> None:
        self.open_details_window(1)

    def open_grid_settings(self) -> None:
        self.open_details_window(4)

    def open_load_settings(self) -> None:
        self.open_details_window(2)

    def set_scenarios(self, scenarios: list[Scenario]) -> None:
        """
        Sets the scenarios on the configuration frame.

        """

        # FIXME: Decide on multiple scenarios approach
        scenario: Scenario = scenarios[0]

        # Power-generation sources
        self.solar_pv_selected.set(scenario.pv)
        self.pv_icon.configure(image=self.solar_images[self.solar_pv_selected.get()])

        self.battery_selected.set(scenario.battery)
        self.battery_icon.configure(
            image=self.battery_images[self.battery_selected.get()]
        )

        self.diesel_selected.set(scenario.diesel_scenario.mode != DieselMode.DISABLED)
        self.update_diesel_settings()
        self.diesel_button.configure(
            image=self.diesel_images[self.diesel_selected.get()]
        )

        self.grid_selected.set(scenario.grid)
        self.grid_icon.configure(image=self.grid_images[self.grid_selected.get()])

        # Resource types
        self.resource_selected[ResourceType.ELECTRIC].set(
            ResourceType.ELECTRIC in scenario.resource_types
        )
        self.electric_button.configure(
            image=self.resource_images[ResourceType.ELECTRIC][
                self.resource_selected[ResourceType.ELECTRIC].get()
            ]
        )

        self.resource_selected[ResourceType.HOT_CLEAN_WATER].set(
            ResourceType.HOT_CLEAN_WATER in scenario.resource_types
        )
        self.hot_water_button.configure(
            image=self.resource_images[ResourceType.HOT_CLEAN_WATER][
                self.resource_selected[ResourceType.HOT_CLEAN_WATER].get()
            ]
        )

        self.resource_selected[ResourceType.CLEAN_WATER].set(
            ResourceType.CLEAN_WATER in scenario.resource_types
        )
        self.clean_water_button.configure(
            image=self.resource_images[ResourceType.CLEAN_WATER][
                self.resource_selected[ResourceType.CLEAN_WATER].get()
            ]
        )

        # Demands
        for domestic_selected_variable in self.domestic_selected.values():
            domestic_selected_variable.set(scenario.demands.domestic)

        for commercial_selected_variable in self.commercial_selected.values():
            commercial_selected_variable.set(scenario.demands.commercial)

        for public_selected_variable in self.public_selected.values():
            public_selected_variable.set(scenario.demands.public)

        # Set the buttons
        self.electric_domestic_label.configure(
            image=(
                self.domestic_images[
                    self.domestic_selected[ResourceType.ELECTRIC].get()
                ]
                if self.resource_selected[ResourceType.ELECTRIC].get()
                else self.domestic_button_disabled_image
            ),
        )
        self.electric_commercial_label.configure(
            image=(
                self.commercial_images[
                    self.commercial_selected[ResourceType.ELECTRIC].get()
                ]
                if self.resource_selected[ResourceType.ELECTRIC].get()
                else self.commercial_button_disabled_image
            ),
        )
        self.electric_public_label.configure(
            image=(
                self.public_images[self.public_selected[ResourceType.ELECTRIC].get()]
                if self.resource_selected[ResourceType.ELECTRIC].get()
                else self.public_button_disabled_image
            ),
        )

        self.hot_water_domestic_label.configure(
            image=(
                self.domestic_images[
                    self.domestic_selected[ResourceType.HOT_CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.HOT_CLEAN_WATER].get()
                else self.domestic_button_disabled_image
            ),
        )
        self.hot_water_commercial_label.configure(
            image=(
                self.commercial_images[
                    self.commercial_selected[ResourceType.HOT_CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.HOT_CLEAN_WATER].get()
                else self.commercial_button_disabled_image
            ),
        )
        self.hot_water_public_label.configure(
            image=(
                self.public_images[
                    self.public_selected[ResourceType.HOT_CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.HOT_CLEAN_WATER].get()
                else self.public_button_disabled_image
            ),
        )

        self.clean_water_domestic_label.configure(
            image=(
                self.domestic_images[
                    self.domestic_selected[ResourceType.CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.CLEAN_WATER].get()
                else self.domestic_button_disabled_image
            ),
        )
        self.clean_water_commercial_label.configure(
            image=(
                self.commercial_images[
                    self.commercial_selected[ResourceType.CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.CLEAN_WATER].get()
                else self.commercial_button_disabled_image
            ),
        )
        self.clean_water_public_label.configure(
            image=(
                self.public_images[self.public_selected[ResourceType.CLEAN_WATER].get()]
                if self.resource_selected[ResourceType.CLEAN_WATER].get()
                else self.public_button_disabled_image
            ),
        )

        # Set the diesel scenario information
        # self.diesel_mode_combobox.set(scenario.diesel_scenario.mode.value)
        # self.diesel_mode_combobox.set(DieselMode.BACKUP.value)
        self.diesel_backup_threshold.set(
            round(
                (
                    scenario.diesel_scenario.backup_threshold
                    if scenario.diesel_scenario.backup_threshold is not None
                    else 0
                )
                * 100,
                1,
            )
        )

        # Set distribution network
        self.distribution_network_combobox.set(scenario.distribution_network.value)

        # Set self-prioritisation
        self.prioritise_self_generation_combobox.set(
            str(scenario.prioritise_self_generation).capitalize()
        )

        # Update the buttons on the parent frame based on the scenario.
        self.pv_icon_configuration_callback(self.solar_pv_selected.get())
        self.storage_button_configuration_callback(self.battery_selected.get())

    def set_minigrid(
        self,
        batteries: list[Battery],
        diesel_generators: list[DieselGenerator],
        grid_profile_name: str,
        minigrid: Minigrid,
        pv_panels: list[PVPanel],
    ) -> None:
        """
        Set the minigrid parameters on the system.

        :param: grid_profile_name
            The name of the grid profile being considered.

        :param: minigrid
            The :class:`Minigrid` being considered.

        """

        # Update the battery name
        if minigrid.battery is not None:
            self.battery.set(minigrid.battery.name)
        else:
            self.battery_combobox.configure(state=DISABLED)

        # Update the combobox
        self.battery_combobox["values"] = [entry.name for entry in batteries]
        self.battery_combobox.set(self.battery.get())

        # Update the PV-panel name
        try:
            if minigrid.pv_panel is not None:
                self.pv_panel.set(minigrid.pv_panel.name)
            else:
                self.pv_panel_combobox.configure(state=DISABLED)
        except ProgrammerJudgementFault:
            self.pv_panel.set(minigrid.pv_panels[0].name)

        # Update the combobox
        self.pv_panel_combobox["values"] = [entry.name for entry in pv_panels]
        self.pv_panel_combobox.set(self.pv_panel.get())

        # Update the diesel-generator name
        if minigrid.diesel_generator is not None:
            self.diesel_generator_combobox.set(minigrid.diesel_generator.name)
        else:
            self.diesel_generator_combobox.configure(state=DISABLED)

        # Update the combobox
        self.diesel_generator_combobox["values"] = [
            entry.name for entry in diesel_generators
        ]
        self.diesel_generator_combobox.set(self.diesel_generator.get())

        # # Update the heat-exchanger name
        # if minigrid.heat_exchanger is not None:
        #     self.heat_exchanger.set(minigrid.heat_exchanger.name)
        #     self.heat_exchanger_combobox.configure(state=READONLY)
        # else:
        #     self.heat_exchanger_combobox.configure(state=DISABLED)
        # self.heat_exchanger_combobox.set(self.heat_exchanger.get())

        # Update the grid profile name
        self.grid_profile_combobox.set(grid_profile_name)
