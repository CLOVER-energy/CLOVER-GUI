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

from clover import DEFAULT_SCENARIO, DemandType, DieselMode, ResourceType, Scenario
from clover.__utils__ import DistributionNetwork, ELECTRIC_POWER
from clover.fileparser import BATTERY, DieselMode, NAME, SCENARIOS
from clover.impact.finance import ImpactingComponent
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.tooltip import ToolTip


__all__ = ("ConfigurationFrame",)


# Images directory name:
#   The name of the images directory.
_IMAGES_DIRECTORY_NAME: str = "images"


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
        pv_button_configuration_callback: Callable,
        storage_button_configuration_callback: Callable,
    ):
        super().__init__(parent)

        self.help_image = help_image
        self.open_details_window = open_details_window
        self.pv_button_configuration_callback = pv_button_configuration_callback
        self.storage_button_configuration_callback = (
            storage_button_configuration_callback
        )

        self.columnconfigure(0, weight=4)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8, minsize=300)
        # self.pack(fill="both", expand=True)

        self.columnconfigure(0, weight=1, minsize=250)
        self.columnconfigure(1, weight=4)

        self.scrollable_scenario_frame = ScrolledFrame(self)
        self.scrollable_scenario_frame.grid(
            row=1,
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
            row=0, column=0, padx=20, pady=10, sticky="ew"
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

        # # Horizontal separator
        # self.separator = ttk.Separator(
        #     self, orient="horizontal"
        # )
        # self.separator.grid(row=0, column=1, columnspan=2, pady=5, padx=10, sticky="")

        # Selecting system components
        self.power_generation_label = ttk.Label(
            self.scrollable_scenario_frame, text="Power sources", style="Bold.TLabel"
        )
        self.power_generation_label.grid(
            row=0, column=0, columnspan=5, padx=10, pady=5, sticky="w"
        )

        # Component labels
        # self.solar_label = ttk.Label(
        #     self.scrollable_scenario_frame, text="PV", bootstyle=INFO, style="Bold.TLabel")
        # self.solar_label.grid(row=0, column=1, rowspan=2, sticky="n")

        # Explainer label
        self.explainer_power_generation_label = ttk.Label(
            self.scrollable_scenario_frame,
            text="Select power sources \n"
            "and adjust settings\n"
            "and components. \n"
            # "Detailed settings can be \n"
            # "adjusted by clicking the\n"
            # "buttons below the \n"
            # "coloured icons.",
        )
        self.explainer_power_generation_label.grid(
            row=1, column=0, padx=10, pady=5, sticky="nsw"
        )
        self.power_source_used_label = ttk.Label(
            self.scrollable_scenario_frame, text="Toggle power sources\n"
            " on or off"
        )
        self.power_source_used_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.power_source_settings_label = ttk.Label(
            self.scrollable_scenario_frame, text="Open advanced settings \n"
            "for each power source"
            # "adjusted by clicking\n"
            # "respective settings buttons\n"
        )
        self.power_source_settings_label.grid(
            row=3, column=0, padx=10, pady=5, sticky="w"
        )

        self.component_selection_label = ttk.Label(
            self.scrollable_scenario_frame, text="Component selection"
        )
        self.component_selection_label.grid(
            row=4, column=0, padx=10, pady=5, sticky="w"
        )

        self.solar_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory,
                    _IMAGES_DIRECTORY_NAME,
                    "solar_gui_selected.png",
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "solar_gui_disabled.png"
                )
            ),
        }
        self.solar_pv_selected: ttk.BooleanVar = ttk.BooleanVar(self, value=False)

        self.pv_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=self.pv_button_callback,
            fg_color="transparent",
            image=self.solar_images[self.solar_pv_selected.get()],
            text="",
        )
        self.pv_button.grid(row=0, column=1, rowspan=2, padx=10)

        # self.pv_label = ttk.Label(
        #     self.scrollable_scenario_frame,
        #     text="PV",
        #     bootstyle=INFO,
        # )
        # self.pv_label.grid(row=0, column=1, rowspan=2, sticky="w")

        self.pv_tooltip = ToolTip(
            self.pv_button,
            text="Toggle whether PV collectors are present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

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
        self.PV_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            text="On / Off",
        )
        self.PV_switch.grid(row=2, column=1, pady=10, sticky="")

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
        self.pv_panel_combobox.grid(row=4, column=1, padx=20, pady=5, sticky="ew")

        self.pv_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="PV settings",
            bootstyle=INFO,
            command=self.open_pv_settings,
        )
        self.pv_settings_button.grid(row=3, column=1, padx=50, sticky="ew")

        self.pv_settings_tooltip = ToolTip(
            self.pv_settings_button,
            text="Opens the detailed settings for configuring PV collectors",
        )

        self.battery_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "battery_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "battery_gui_disabled.png"
                )
            ),
        }
        self.battery_selected: ttk.BooleanVar = ttk.BooleanVar(self, value=False)
        self.battery_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=self.battery_button_callback,
            fg_color="transparent",
            image=self.battery_images[self.battery_selected.get()],
            text="",
        )
        self.battery_button.grid(row=0, column=2, rowspan=2, pady=5, padx=10, sticky="")

        self.battery_tooltip = ToolTip(
            self.battery_button,
            text="Toggle whether electric batteries are present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

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
            text="On / Off",
        )
        self.battery_switch.grid(row=2, column=2, pady=10, sticky="")

        self.battery_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Battery settings",
            bootstyle=INFO,
            command=self.open_battery_settings,
        )
        self.battery_settings_button.grid(row=3, column=2, padx=20)

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
        self.battery_combobox.grid(row=4, column=2, pady=5, padx=30, sticky="ew")

        self.diesel_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "diesel_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "diesel_gui_disabled.png"
                )
            ),
        }
        self.diesel_selected: ttk.BooleanVar = ttk.BooleanVar(self, value=False)
        self.diesel_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=self.diesel_button_callback,
            fg_color="transparent",
            image=self.diesel_images[self.diesel_selected.get()],
            text="",
        )
        self.diesel_button.grid(row=0, column=3, rowspan=2, pady=5, padx=10)

        self.diesel_tooltip = ToolTip(
            self.diesel_button,
            text="Toggle whether backup diesel power is present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )
        self.diesel_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            text="On / Off",
        )
        self.diesel_switch.grid(row=2, column=3, pady=10, sticky="")

        self.diesel_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Diesel settings",
            bootstyle=INFO,
            command=self.open_diesel_settings,
        )
        self.diesel_settings_button.grid(row=3, column=3, padx=20)
        self.diesel_settings_tooltip = ToolTip(
            self.diesel_settings_button,
            text="Opens the detailed settings for configuring diesel generators",
        )
        # Diesel selection
        self.diesel = ttk.StringVar(self, "")
        self.diesel_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
            values=[],
            state=READONLY,
            bootstyle=INFO,
            textvariable=self.diesel,
            width=5,
        )
        self.diesel_combobox.grid(row=4, column=3, pady=5, padx=30, sticky="ew")

        self.grid_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "grid_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "grid_gui_disabled.png"
                )
            ),
        }
        self.grid_selected: ttk.BooleanVar = ttk.BooleanVar(self, value=False)
        self.grid_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=self.grid_button_callback,
            fg_color="transparent",
            image=self.grid_images[self.grid_selected.get()],
            text="",
        )
        self.grid_button.grid(row=0, column=4, rowspan=2, pady=5, padx=10)

        self.grid_tooltip = ToolTip(
            self.grid_button,
            text="Toggle whether backup a grid connection is present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )
        self.grid_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            text="On / Off",
        )
        self.grid_switch.grid(row=2, column=4, pady=10, sticky="")

        # Grid selection
        self.grid = ttk.StringVar(self, "")
        self.grid_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
            values=[],
            state=READONLY,
            bootstyle=INFO,
            textvariable=self.grid,
            width=5,
        )
        self.grid_combobox.grid(row=4, column=4, pady=5, padx=30, sticky="ew")

        self.grid_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Grid settings",
            bootstyle=INFO,
            command=self.open_grid_settings,
        )
        self.grid_settings_button.grid(row=3, column=4, padx=20)

        self.grid_settings_tooltip = ToolTip(
            self.grid_settings_button,
            text="Opens the detailed settings for configuring the probability of the "
            "grid being available.",
        )
        # Empty line
        self.empty_line = ttk.Label(self.scrollable_scenario_frame, text="")
        self.empty_line.grid(row=5, column=0, columnspan=5, pady=5, padx=10)

        # Horizontal separator
        self.separator = ttk.Separator(
            self.scrollable_scenario_frame, orient="horizontal"
        )
        self.separator.grid(row=6, column=0, columnspan=5, pady=5, padx=10, sticky="ew")

        # Resource types selection
        self.resource_images: dict[ResourceType, dict[bool, ttk.PhotoImage]] = {
            ResourceType.ELECTRIC: {
                True: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory,
                        _IMAGES_DIRECTORY_NAME,
                        "electric_gui_selected_filled.png",
                    )
                ),
                False: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory,
                        _IMAGES_DIRECTORY_NAME,
                        "electric_gui_selected_outline.png",
                    )
                ),
            },
            ResourceType.HOT_CLEAN_WATER: {
                True: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory,
                        _IMAGES_DIRECTORY_NAME,
                        "hot_water_gui_selected_filled.png",
                    )
                ),
                False: ttk.PhotoImage(
                    file=os.path.join(
                        data_directory,
                        _IMAGES_DIRECTORY_NAME,
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
            row=7, column=0, columnspan=5, padx=10, pady=5, sticky="w"
        )
       
        # Demand type headings
        self.domestic_demand_header = ttk.Label(
            self.scrollable_scenario_frame, text="Domestic", 
        )
        self.domestic_demand_header.grid(row=7, column=1, padx=10, pady=5, sticky="")

        self.commercial_demand_header = ttk.Label(
            self.scrollable_scenario_frame, text="Commercial"
        )
        self.commercial_demand_header.grid(row=7, column=2, padx=10, pady=5, sticky="")

        self.public_demand_header = ttk.Label(
            self.scrollable_scenario_frame, text="Public"
        )
        self.public_demand_header.grid(row=7, column=3, padx=10, pady=5, sticky="")

        self.electric_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.resource_button_callback, ResourceType.ELECTRIC
            ),
            fg_color="transparent",
            image=self.resource_images[ResourceType.ELECTRIC][
                self.resource_selected[ResourceType.ELECTRIC].get()
            ],
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
        self.demand_explainer.grid(row=8, column=0, pady=5, padx=10, sticky="nsw")

        self.demand_toggle_explainer = ttk.Label(
            self.scrollable_scenario_frame, text="Toggle demand types\n"
            " on or off"
        )
        self.demand_toggle_explainer.grid(
            row=9, column=0, pady=5, rowspan=2, padx=10, sticky="w"
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
                    data_directory, _IMAGES_DIRECTORY_NAME, "domestic_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory,
                    _IMAGES_DIRECTORY_NAME,
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
        self.electric_domestic_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.domestic_button_callback, ResourceType.ELECTRIC
            ),
            fg_color="transparent",
            image=self.domestic_images[
                self.domestic_selected[ResourceType.ELECTRIC].get()
            ],
            text="",
        )
        self.electric_domestic_button.grid(row=8, column=1, pady=5, padx=10, sticky="")
        self.electric_domestic_button_tooltip = ToolTip(
            self.electric_domestic_button,
            text="Toggles whether domestic electric demands are included when "
            "generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )
        self.electric_domestic_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            text="On / Off",
        )
        self.electric_domestic_switch.grid(row=9, column=1, pady=10, sticky="")

        self.hot_water_domestic_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.domestic_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.domestic_button_disabled_image,
            text="",
        )
        # self.hot_water_domestic_button.grid(row=4, column=2, pady=5, padx=10, sticky="")
        # self.hot_water_domestic_button_tooltip = ToolTip(
        #     self.hot_water_domestic_button,
        #     text="Toggles whether domestic hot-water demands are included when "
        #     "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{DANGER}",
        # )

        self.clean_water_domestic_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.domestic_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.domestic_button_disabled_image,
            text="",
        )
        # self.clean_water_domestic_button.grid(
        #     row=5, column=2, pady=5, padx=10, sticky=""
        # )
        # self.clean_water_domestic_button_tooltip = ToolTip(
        #     self.clean_water_domestic_button,
        #     text="Toggles whether domestic clean-water demands are included when "
        #     generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{PRIMARY}",
        # )

        self.domestic_buttons: dict[ResourceType, ctk.CTkButton] = {
            ResourceType.ELECTRIC: self.electric_domestic_button,
            ResourceType.HOT_CLEAN_WATER: self.hot_water_domestic_button,
            ResourceType.CLEAN_WATER: self.clean_water_domestic_button,
        }

        # Commercial buttons
        self.commercial_selected: dict[ResourceType, ttk.BooleanVar] = {
            ResourceType.ELECTRIC: ttk.BooleanVar(self, value=False),
            ResourceType.HOT_CLEAN_WATER: ttk.BooleanVar(self, value=False),
            ResourceType.CLEAN_WATER: ttk.BooleanVar(self, value=False),
        }

        self.electric_commercial_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.commercial_button_callback, ResourceType.ELECTRIC
            ),
            fg_color="transparent",
            image=self.commercial_images[
                self.commercial_selected[ResourceType.ELECTRIC].get()
            ],
            text="",
        )
        self.electric_commercial_button.grid(row=8, column=2, pady=5, padx=10)
        self.electric_commercial_button_tooltip = ToolTip(
            self.electric_commercial_button,
            text="Toggles whether commercial electricity demands are included when "
            "generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )
        self.electric_commercial_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            text="On / Off",
        )
        self.electric_commercial_switch.grid(row=9, column=2, pady=10, sticky="")

        self.hot_water_commercial_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.commercial_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.commercial_button_disabled_image,
            text="",
        )
        # self.hot_water_commercial_button.grid(row=4, column=3, pady=5, padx=10)
        # self.hot_water_commercial_button_tooltip = ToolTip(
        #     self.hot_water_commercial_button,
        #     text="Toggles whether commercial hot-water demands are included when "
        #     "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{DANGER}",
        # )

        self.clean_water_commercial_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.commercial_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.commercial_button_disabled_image,
            text="",
        )
        # self.clean_water_commercial_button.grid(row=5, column=3, pady=5, padx=10)
        # self.clean_water_commercial_button_tooltip = ToolTip(
        #     self.clean_water_commercial_button,
        #     text="Toggles whether commercial clean-water demands are included when "
        #     "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{PRIMARY}",
        # )

        self.commercial_buttons: dict[ResourceType, ctk.CTkButton] = {
            ResourceType.ELECTRIC: self.electric_commercial_button,
            ResourceType.HOT_CLEAN_WATER: self.hot_water_commercial_button,
            ResourceType.CLEAN_WATER: self.clean_water_commercial_button,
        }

        # Public buttons
        self.public_selected: dict[ResourceType, ttk.BooleanVar] = {
            ResourceType.ELECTRIC: ttk.BooleanVar(self, value=False),
            ResourceType.HOT_CLEAN_WATER: ttk.BooleanVar(self, value=False),
            ResourceType.CLEAN_WATER: ttk.BooleanVar(self, value=False),
        }

        self.electric_public_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.public_button_callback, ResourceType.ELECTRIC
            ),
            fg_color="transparent",
            image=self.public_images[self.public_selected[ResourceType.ELECTRIC].get()],
            text="",
        )
        self.electric_public_button.grid(row=8, column=3, pady=5, padx=10)
        self.electric_public_button_tooltip = ToolTip(
            self.electric_public_button,
            text="Toggles whether public electricity demands are included when "
            "generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )
        self.electric_public_switch = ttk.Checkbutton(
            self.scrollable_scenario_frame,
            bootstyle="info-square-toggle",
            text="On / Off",
        )
        self.electric_public_switch.grid(row=9, column=3, pady=10, sticky="")

        self.hot_water_public_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.public_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.public_button_disabled_image,
            text="",
        )
        # self.hot_water_public_button.grid(row=4, column=4, pady=5, padx=10)
        # self.hot_water_public_button_tooltip = ToolTip(
        #     self.hot_water_public_button,
        #     text="Toggles whether public hot-water demands are included when "
        #     "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{DANGER}",
        # )

        self.clean_water_public_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.public_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.public_button_disabled_image,
            text="",
        )
        # self.clean_water_public_button.grid(row=5, column=4, pady=5, padx=10)
        # self.clean_water_public_button_tooltip = ToolTip(
        #     self.clean_water_public_button,
        #     text="Toggles whether public clean-water demands are included when "
        #    "generating stochastic demand profiles.",
        #     bootstyle=f"{INVERSE}-{PRIMARY}",
        # )

        self.public_buttons: dict[ResourceType, ctk.CTkButton] = {
            ResourceType.ELECTRIC: self.electric_public_button,
            ResourceType.HOT_CLEAN_WATER: self.hot_water_public_button,
            ResourceType.CLEAN_WATER: self.clean_water_public_button,
        }

        self.demand_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Demand settings",
            bootstyle=INFO,
            command=NONE,
        )
        self.demand_settings_button.grid(row=8, column=4, padx=20)

        # Row with a horizontal separator
        self.separator = ttk.Separator(
            self.scrollable_scenario_frame, orient="horizontal"
        )
        self.separator.grid(
            row=11, column=0, pady=5, padx=10, columnspan=5, sticky="news"
        )

        # Empty row
        self.empty_row = ttk.Frame(self.scrollable_scenario_frame)
        self.empty_row.grid(
            row=10, column=0, pady=5, padx=10, columnspan=5, sticky="news"
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
            row=12, column=0, padx=10, pady=5, columnspan=5, sticky="w"
        )

        self.other_settings_explainer = ttk.Label(
            self.scrollable_scenario_frame,
            text="Miscellaneous settings\n"
            "for scenarios including\n"
            "grid-prioritisation and\n"
            "diesel-generator settings.",
        )
        self.other_settings_explainer.grid(
            row=13, column=0, pady=5, rowspan=3, padx=10, sticky="nsw"
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
            row=13, column=1, padx=10, pady=5, sticky="w"
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
        self.diesel_backup_slider.grid(row=13, column=2, padx=10, pady=5, sticky="ew")

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
        self.diesel_backup_entry.grid(row=13, column=3, padx=10, pady=5, sticky="ew")
        self.diesel_backup_entry.bind("<Return>", enter_threshold)

        self.diesel_backup_threshold_unit = ttk.Label(
            self.scrollable_scenario_frame, text=f"% of hours"
        )
        self.diesel_backup_threshold_unit.grid(
            row=13, column=4, padx=10, pady=5, sticky="w"
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
            row=14, column=1, padx=10, pady=5, sticky="w"
        )

        self.distribution_network_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
        )
        self.distribution_network_combobox.grid(
            row=14, column=2, padx=10, pady=5, sticky="w"
        )
        self.distribution_network_combobox["values"] = [
            e.value for e in DistributionNetwork
        ]
        self.distribution_network_combobox.set(DistributionNetwork.DC.value)

        # Self generation
        self.prioritise_self_generation_label = ttk.Label(
            self.scrollable_scenario_frame,
            text="Prioritise self\n"
            "generation",
        )
        self.prioritise_self_generation_label.grid(
            row=15, column=1, padx=10, pady=5, sticky="w"
        )

        self.prioritise_self_generation_combobox = ttk.Combobox(
            self.scrollable_scenario_frame,
        )
        self.prioritise_self_generation_combobox.grid(
            row=15, column=2, padx=10, pady=5, sticky="w"
        )
        self.prioritise_self_generation_combobox["values"] = ["True", "False"]
        self.prioritise_self_generation_combobox.set("True")

    def as_dict(
        self, grid_type: str
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
                    "grid_type": grid_type,
                    # FIXME: Implement a fixed inverter size.
                    "fixed_inverter_size": False,
                    "prioritise_self_generation": self.prioritise_self_generation_combobox.get(),
                    ImpactingComponent.PV.value: self.solar_pv_selected.get(),
                    "resource_types": resource_types,
                }
            ]
        }

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
        self.solar_pv_selected.set(not self.solar_pv_selected.get())
        self.pv_button.configure(image=self.solar_images[self.solar_pv_selected.get()])
        self.pv_button_configuration_callback(self.solar_pv_selected.get())

    def battery_button_callback(self):
        self.battery_selected.set(not self.battery_selected.get())
        self.battery_button.configure(
            image=self.battery_images[self.battery_selected.get()]
        )
        self.storage_button_configuration_callback(self.battery_selected.get())

    def diesel_button_callback(self):
        self.diesel_selected.set(not self.diesel_selected.get())
        self.diesel_button.configure(
            image=self.diesel_images[self.diesel_selected.get()]
        )

        self.update_diesel_settings()

    def grid_button_callback(self):
        self.grid_selected.set(not self.grid_selected.get())
        self.grid_button.configure(image=self.grid_images[self.grid_selected.get()])

    def resource_button_callback(self, resource_type: ResourceType):
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
            self.domestic_buttons[resource_type].configure(
                image=self.domestic_images[self.domestic_selected[resource_type].get()]
            )
            self.commercial_buttons[resource_type].configure(
                image=self.commercial_images[
                    self.commercial_selected[resource_type].get()
                ]
            )
            self.public_buttons[resource_type].configure(
                image=self.public_images[self.public_selected[resource_type].get()]
            )
        else:
            self.domestic_buttons[resource_type].configure(
                image=self.domestic_button_disabled_image
            )
            self.commercial_buttons[resource_type].configure(
                image=self.commercial_button_disabled_image
            )
            self.public_buttons[resource_type].configure(
                image=self.public_button_disabled_image
            )

    def domestic_button_callback(self, resource_type: ResourceType) -> None:
        # Return if electric loads are not selected
        if not self.resource_selected[resource_type].get():
            return
        self.domestic_selected[resource_type].set(
            not self.domestic_selected[resource_type].get()
        )
        self.domestic_buttons[resource_type].configure(
            image=self.domestic_images[self.domestic_selected[resource_type].get()]
        )

    def commercial_button_callback(self, resource_type: ResourceType) -> None:
        # Return if electric loads are not selected
        if not self.resource_selected[resource_type].get():
            return
        self.commercial_selected[resource_type].set(
            not self.commercial_selected[resource_type].get()
        )
        self.commercial_buttons[resource_type].configure(
            image=self.commercial_images[self.commercial_selected[resource_type].get()]
        )

    def public_button_callback(self, resource_type: ResourceType) -> None:
        # Return if electric loads are not selected
        if not self.resource_selected[resource_type].get():
            return
        self.public_selected[resource_type].set(
            not self.public_selected[resource_type].get()
        )
        self.public_buttons[resource_type].configure(
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

    def set_scenarios(self, scenarios: list[Scenario]) -> None:
        """
        Sets the scenarios on the configuration frame.

        """

        # FIXME: Decide on multiple scenarios approach
        scenario: Scenario = scenarios[0]

        # Power-generation sources
        self.solar_pv_selected.set(scenario.pv)
        self.pv_button.configure(image=self.solar_images[self.solar_pv_selected.get()])

        self.battery_selected.set(scenario.battery)
        self.battery_button.configure(
            image=self.battery_images[self.battery_selected.get()]
        )

        self.diesel_selected.set(scenario.diesel_scenario.mode != DieselMode.DISABLED)
        self.update_diesel_settings()
        self.diesel_button.configure(
            image=self.diesel_images[self.diesel_selected.get()]
        )

        self.grid_selected.set(scenario.grid)
        self.grid_button.configure(image=self.grid_images[self.grid_selected.get()])

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
        self.electric_domestic_button.configure(
            image=(
                self.domestic_images[
                    self.domestic_selected[ResourceType.ELECTRIC].get()
                ]
                if self.resource_selected[ResourceType.ELECTRIC].get()
                else self.domestic_button_disabled_image
            ),
        )
        self.electric_commercial_button.configure(
            image=(
                self.commercial_images[
                    self.commercial_selected[ResourceType.ELECTRIC].get()
                ]
                if self.resource_selected[ResourceType.ELECTRIC].get()
                else self.commercial_button_disabled_image
            ),
        )
        self.electric_public_button.configure(
            image=(
                self.public_images[self.public_selected[ResourceType.ELECTRIC].get()]
                if self.resource_selected[ResourceType.ELECTRIC].get()
                else self.public_button_disabled_image
            ),
        )

        self.hot_water_domestic_button.configure(
            image=(
                self.domestic_images[
                    self.domestic_selected[ResourceType.HOT_CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.HOT_CLEAN_WATER].get()
                else self.domestic_button_disabled_image
            ),
        )
        self.hot_water_commercial_button.configure(
            image=(
                self.commercial_images[
                    self.commercial_selected[ResourceType.HOT_CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.HOT_CLEAN_WATER].get()
                else self.commercial_button_disabled_image
            ),
        )
        self.hot_water_public_button.configure(
            image=(
                self.public_images[
                    self.public_selected[ResourceType.HOT_CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.HOT_CLEAN_WATER].get()
                else self.public_button_disabled_image
            ),
        )

        self.clean_water_domestic_button.configure(
            image=(
                self.domestic_images[
                    self.domestic_selected[ResourceType.CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.CLEAN_WATER].get()
                else self.domestic_button_disabled_image
            ),
        )
        self.clean_water_commercial_button.configure(
            image=(
                self.commercial_images[
                    self.commercial_selected[ResourceType.CLEAN_WATER].get()
                ]
                if self.resource_selected[ResourceType.CLEAN_WATER].get()
                else self.commercial_button_disabled_image
            ),
        )
        self.clean_water_public_button.configure(
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
        self.pv_button_configuration_callback(self.solar_pv_selected.get())
        self.storage_button_configuration_callback(self.battery_selected.get())
