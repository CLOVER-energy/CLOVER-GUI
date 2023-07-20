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

from clover import DieselMode, ResourceType, Scenario
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

    def __init__(self, parent, data_directory: str, open_details_window: Callable):
        super().__init__(parent)

        self.open_details_window = open_details_window

        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        # self.pack(fill="both", expand=True)

        # Scenario details information
        self.hover_information_frame: ttk.Labelframe = ttk.Labelframe(
            self, style="info.TLabelframe", text="Information"
        )
        self.hover_information_frame.grid(
            row=0, column=1, padx=10, pady=5, sticky="news"
        )

        self.hover_text: ttk.StringVar = ttk.StringVar(self, "")

        self.hover_label = ttk.Label(
            self.hover_information_frame, textvariable=self.hover_text
        )
        self.hover_label.grid(row=0, column=0, sticky="news")

        self.scrollable_scenario_frame = ScrolledFrame(self)
        self.scrollable_scenario_frame.grid(
            row=0,
            column=0,
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

        # Selecting system components
        self.power_generation_label: ttk.Label = ttk.Label(
            self.scrollable_scenario_frame, text="Power sources"
        )
        self.power_generation_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

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
                    data_directory, _IMAGES_DIRECTORY_NAME, "solar_gui_deselected.png"
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
        self.pv_button.grid(row=1, column=1, pady=5, padx=10)

        self.pv_tooltip = ToolTip(
            self.pv_button,
            text="Toggle whether PV collectors are present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

        self.pv_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="PV settings",
            bootstyle=INFO,
            command=self.open_pv_settings,
        )
        self.pv_settings_button.grid(row=2, column=1, padx=20)

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
                    data_directory, _IMAGES_DIRECTORY_NAME, "battery_gui_deselected.png"
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
        self.battery_button.grid(row=1, column=2, pady=5, padx=10, sticky="")

        self.battery_tooltip = ToolTip(
            self.battery_button,
            text="Toggle whether electric batteries are present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

        self.battery_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Battery settings",
            bootstyle=INFO,
            command=self.open_battery_settings,
        )
        self.battery_settings_button.grid(row=2, column=2, padx=20)

        self.battery_settings_tooltip = ToolTip(
            self.battery_settings_button,
            text="Opens the detailed settings for configuring batteries",
        )

        self.diesel_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "diesel_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "diesel_gui_deselected.png"
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
        self.diesel_button.grid(row=1, column=3, pady=5, padx=10)

        self.diesel_tooltip = ToolTip(
            self.diesel_button,
            text="Toggle whether backup diesel power is present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

        self.diesel_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Diesel settings",
            bootstyle=INFO,
            command=self.open_diesel_settings,
        )
        self.diesel_settings_button.grid(row=2, column=3, padx=20)
        self.diesel_settings_tooltip = ToolTip(
            self.diesel_settings_button,
            text="Opens the detailed settings for configuring diesel generators",
        )

        self.grid_images: dict[bool, ttk.PhotoImage] = {
            True: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "grid_gui_selected.png"
                )
            ),
            False: ttk.PhotoImage(
                file=os.path.join(
                    data_directory, _IMAGES_DIRECTORY_NAME, "grid_gui_deselected.png"
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
        self.grid_button.grid(row=1, column=4, pady=5, padx=10)

        self.grid_tooltip = ToolTip(
            self.grid_button,
            text="Toggle whether backup a grid connection is present in the system",
            bootstyle=f"{INFO}-{INVERSE}",
        )

        self.grid_settings_button = ttk.Button(
            self.scrollable_scenario_frame,
            text="Grid settings",
            bootstyle=INFO,
            command=self.open_grid_settings,
        )
        self.grid_settings_button.grid(row=2, column=4, padx=20)

        self.grid_settings_tooltip = ToolTip(
            self.grid_settings_button,
            text="Opens the detailed settings for configuring the probability of the grid being available.",
        )

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
            self.scrollable_scenario_frame, text="Electricity demand"
        )
        self.electric_power_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

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
        )
        self.electric_button.grid(row=3, column=1, pady=5, padx=10, sticky="")
        self.electric_button_tooltip = ToolTip(
            self.electric_button,
            text="Toggles whether electric power demands are included when generating stochastic demand profiles.",
            bootstyle=f"{WARNING}-{INVERSE}",
        )

        self.hot_water_power_label: ttk.Label = ttk.Label(
            self.scrollable_scenario_frame, text="Hot-water demand"
        )
        self.hot_water_power_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

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
        self.hot_water_button.grid(row=4, column=1, pady=5, padx=10, sticky="")
        self.hot_water_button_tooltip = ToolTip(
            self.hot_water_button,
            text="Toggles whether hot-water demands are included when generating stochastic demand profiles.",
            bootstyle=f"{DANGER}-{INVERSE}",
        )

        self.clean_water_power_label: ttk.Label = ttk.Label(
            self.scrollable_scenario_frame, text="Clean-water demand"
        )
        self.clean_water_power_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

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
        self.clean_water_button.grid(row=5, column=1, pady=5, padx=10, sticky="")
        self.clean_water_button_tooltip = ToolTip(
            self.clean_water_button,
            text="Toggles whether clean-water demands are included when generating stochastic demand profiles.",
            bootstyle=f"{PRIMARY}-{INVERSE}",
        )

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
                    "domestic_gui_deselected.png",
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
                    data_directory, "images", "commercial_gui_deselected.png"
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
                file=os.path.join(data_directory, "images", "public_gui_deselected.png")
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
        self.electric_domestic_button.grid(row=3, column=2, pady=5, padx=10, sticky="")
        self.electric_domestic_button_tooltip = ToolTip(
            self.electric_domestic_button,
            text="Toggles whether domestic electric demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )

        self.hot_water_domestic_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.domestic_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.domestic_button_disabled_image,
            text="",
        )
        self.hot_water_domestic_button.grid(row=4, column=2, pady=5, padx=10, sticky="")
        self.hot_water_domestic_button_tooltip = ToolTip(
            self.hot_water_domestic_button,
            text="Toggles whether domestic hot-water demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{DANGER}",
        )

        self.clean_water_domestic_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.domestic_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.domestic_button_disabled_image,
            text="",
        )
        self.clean_water_domestic_button.grid(
            row=5, column=2, pady=5, padx=10, sticky=""
        )
        self.clean_water_domestic_button_tooltip = ToolTip(
            self.clean_water_domestic_button,
            text="Toggles whether domestic clean-water demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{PRIMARY}",
        )

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
        self.electric_commercial_button.grid(row=3, column=3, pady=5, padx=10)
        self.electric_commercial_button_tooltip = ToolTip(
            self.electric_commercial_button,
            text="Toggles whether commercial electricity demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )

        self.hot_water_commercial_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.commercial_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.commercial_button_disabled_image,
            text="",
        )
        self.hot_water_commercial_button.grid(row=4, column=3, pady=5, padx=10)
        self.hot_water_commercial_button_tooltip = ToolTip(
            self.hot_water_commercial_button,
            text="Toggles whether commercial hot-water demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{DANGER}",
        )

        self.clean_water_commercial_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.commercial_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.commercial_button_disabled_image,
            text="",
        )
        self.clean_water_commercial_button.grid(row=5, column=3, pady=5, padx=10)
        self.clean_water_commercial_button_tooltip = ToolTip(
            self.clean_water_commercial_button,
            text="Toggles whether commercial clean-water demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{PRIMARY}",
        )

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
        self.electric_public_button.grid(row=3, column=4, pady=5, padx=10)
        self.electric_public_button_tooltip = ToolTip(
            self.electric_public_button,
            text="Toggles whether public electricity demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{WARNING}",
        )

        self.hot_water_public_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.public_button_callback, ResourceType.HOT_CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.public_button_disabled_image,
            text="",
        )
        self.hot_water_public_button.grid(row=4, column=4, pady=5, padx=10)
        self.hot_water_public_button_tooltip = ToolTip(
            self.hot_water_public_button,
            text="Toggles whether public hot-water demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{DANGER}",
        )

        self.clean_water_public_button = ctk.CTkButton(
            master=self.scrollable_scenario_frame,
            command=functools.partial(
                self.public_button_callback, ResourceType.CLEAN_WATER
            ),
            fg_color="transparent",
            image=self.public_button_disabled_image,
            text="",
        )
        self.clean_water_public_button.grid(row=5, column=4, pady=5, padx=10)
        self.clean_water_public_button_tooltip = ToolTip(
            self.clean_water_public_button,
            text="Toggles whether public clean-water demands are included when generating stochastic demand profiles.",
            bootstyle=f"{INVERSE}-{PRIMARY}",
        )

        self.public_buttons: dict[ResourceType, ctk.CTkButton] = {
            ResourceType.ELECTRIC: self.electric_public_button,
            ResourceType.HOT_CLEAN_WATER: self.hot_water_public_button,
            ResourceType.CLEAN_WATER: self.clean_water_public_button,
        }

        # TODO: Add configuration frame widgets and layout

    def pv_button_callback(self):
        self.solar_pv_selected.set(not self.solar_pv_selected.get())
        self.pv_button.configure(image=self.solar_images[self.solar_pv_selected.get()])

    def battery_button_callback(self):
        self.battery_selected.set(not self.battery_selected.get())
        self.battery_button.configure(
            image=self.battery_images[self.battery_selected.get()]
        )

    def diesel_button_callback(self):
        self.diesel_selected.set(not self.diesel_selected.get())
        self.diesel_button.configure(
            image=self.diesel_images[self.diesel_selected.get()]
        )

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
