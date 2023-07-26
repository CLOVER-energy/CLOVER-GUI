#!/usr/bin/python3.10
########################################################################################
# load.py - The load module for CLOVER-GUI application.                                #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import enum

from typing import Any, Callable

import pandas as pd
import ttkbootstrap as ttk

from clover.load.load import DemandType, Device
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

__all__ = ("LoadFrame",)


class GUIDevice:
    """
    Contains settings for a device.

    TODO: Update docstring.

    """

    def __init__(
        self,
        parent: Any,
        name: str,
        active: bool,
        electric_power: float,
        initial_ownership: float,
        final_ownership: float,
        innovation: float,
        imitation: float,
        device_type: DemandType,
        clean_water_consumption: float = 0,
    ) -> None:

        self.name: ttk.StringVar = ttk.StringVar(parent, name)
        self.electric_power: ttk.DoubleVar = ttk.DoubleVar(parent, electric_power)
        self.initial_ownership: ttk.DoubleVar = ttk.DoubleVar(parent, initial_ownership)
        self.final_ownership: ttk.DoubleVar = ttk.DoubleVar(parent, final_ownership)
        self.innovation: ttk.DoubleVar = ttk.DoubleVar(parent, innovation)
        self.imitation: ttk.DoubleVar = ttk.DoubleVar(parent, imitation)
        self.device_type: ttk.StringVar = ttk.StringVar(parent, device_type.value)
        self.clean_water_consumption: ttk.DoubleVar = ttk.DoubleVar(
            parent, clean_water_consumption
        )
        self.active: ttk.BooleanVar = ttk.BooleanVar(
            parent, active, f"{self.name}-active"
        )


class DeviceSettingsFrame(ttk.Labelframe):
    """
    Represents the device-settings frame.

    Contains settings the device selected.

    TODO: Update attributes.

    """

    def __init__(self, parent: Any):
        super().__init__(parent, text="Device settings", style=SUCCESS)

        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=4)
        self.columnconfigure(2, weight=1)

        # Device name
        self.name_label = ttk.Label(self, text="Device name", style=SUCCESS)
        self.name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.name_entry = ttk.Entry(
            self, textvariable=parent.active_device.name, style=SUCCESS
        )
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, ipadx=10)

        self.name_entry.bind("<Return>", parent.update_button_label)

        # Electric Power
        self.electric_power_label = ttk.Label(self, text="Electric Power")
        self.electric_power_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.electric_power_entry = ttk.Entry(
            self, textvariable=parent.active_device.electric_power.get()
        )
        self.electric_power_entry.grid(
            row=1, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.electric_power_unit = ttk.Label(self, text="kW")
        self.electric_power_unit.grid(row=1, column=2, padx=10, pady=5, sticky="w")

        # Initial Ownership
        self.initial_ownership_label = ttk.Label(self, text="Initial Ownership")
        self.initial_ownership_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.initial_ownership_entry = ttk.Entry(
            self, textvariable=parent.active_device.initial_ownership.get()
        )
        self.initial_ownership_entry.grid(
            row=2, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.initial_ownership_unit = ttk.Label(self, text="devices / household")
        self.initial_ownership_unit.grid(row=2, column=2, padx=10, pady=5, sticky="w")

        # Final Ownership
        self.final_ownership_label = ttk.Label(self, text="Final Ownership")
        self.final_ownership_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.final_ownership_entry = ttk.Entry(
            self, textvariable=parent.active_device.final_ownership.get()
        )
        self.final_ownership_entry.grid(
            row=3, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.final_ownership_unit = ttk.Label(self, text="devices / household")
        self.final_ownership_unit.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        # Innovation
        self.innovation_label = ttk.Label(self, text="Innovation")
        self.innovation_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

        self.innovation_entry = ttk.Entry(
            self, textvariable=parent.active_device.innovation.get()
        )
        self.innovation_entry.grid(
            row=4, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.innovation_unit = ttk.Label(self, text="innovation_units")
        self.innovation_unit.grid(row=4, column=2, padx=10, pady=5, sticky="w")

        # Imitation
        self.imitation_label = ttk.Label(self, text="Imitation")
        self.imitation_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.imitation_entry = ttk.Entry(
            self, textvariable=parent.active_device.imitation.get()
        )
        self.imitation_entry.grid(
            row=5, column=1, padx=10, pady=5, sticky="ew", ipadx=10
        )

        self.imitation_unit = ttk.Label(self, text="imitation unit")
        self.imitation_unit.grid(row=5, column=2, padx=10, pady=5, sticky="w")

        # Clean Water Consumption
        self.clean_water_consumption_label = ttk.Label(
            self, text="Clean Water Consumption"
        )
        self.clean_water_consumption_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        self.clean_water_consumption_entry = ttk.Entry(
            self,
            textvariable=parent.active_device.clean_water_consumption.get(),
            state=DISABLED,
        )
        self.clean_water_consumption_entry.grid(
            row=6,
            column=1,
            padx=10,
            pady=5,
            sticky="ew",
            ipadx=10,
        )

        self.clean_water_consumption_unit = ttk.Label(
            self, text="litres / hour", style=SUCCESS, state=DISABLED
        )
        self.clean_water_consumption_unit.grid(
            row=6, column=2, padx=10, pady=5, sticky="w"
        )


class DevicesFrame(ScrolledFrame):
    """
    Represents the scrollable frame where devices can be selected.

    TODO: Update attributes.

    """

    def __init__(
        self, parent, select_device: Callable, update_device_settings_frame: Callable
    ):
        super().__init__(parent)

        # Duplicate functional call
        self.update_device_settings_frame = update_device_settings_frame

        self.device_active_buttons: dict[GUIDevice, ttk.Button] = {
            device: ttk.Checkbutton(
                self,
                style=f"{SUCCESS}.{OUTLINE}.{TOOLBUTTON}",
                variable=device.active,
            )
            for device in parent.devices
        }

        self.device_selected_buttons: dict[GUIDevice, ttk.Button] = {
            device: ttk.Button(
                self,
                text=device.name.get().capitalize(),
                style=f"{SUCCESS}.{OUTLINE}",
            )
            for device in parent.devices
        }

        for index, button in enumerate(self.device_active_buttons.values()):
            # Check button
            button.grid(row=index, column=0, padx=10, pady=5)

        for index, button in enumerate(self.device_selected_buttons.values()):
            button.grid(row=index, column=1, padx=10, pady=5, sticky="w")


class LoadFrame(ttk.Frame):
    """
    Represents the Load frame.

    Contains settings for load management.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)

        self.devices = [
            GUIDevice(self, "light", True, 3, 2, 4, 0.04, 0.5, DemandType.DOMESTIC),
        ]

        self.active_device: GUIDevice = self.devices[0]

        # Create the right-hand frame for adjusting device settings
        self.settings_frame = DeviceSettingsFrame(self)
        self.settings_frame.grid(
            row=0, column=1, padx=20, pady=10, sticky="news", rowspan=2
        )

        # Create the button for creating devices
        self.add_device_button = ttk.Button(
            self,
            bootstyle=f"{SUCCESS}-{OUTLINE}",
            command=self.add_device,
            text="New device",
        )
        self.add_device_button.grid(row=0, column=0, padx=10, pady=5, ipadx=80)

        # Create the left-hand frame for selecting the devices
        self.devices_frame = DevicesFrame(
            self, self.select_device, self.update_device_settings_frame
        )
        self.devices_frame.grid(row=1, column=0, padx=20, pady=10, sticky="news")

        for device, button in self.devices_frame.device_selected_buttons.items():
            button.configure(command=lambda device=device: self.select_device(device))

        self.select_device(self.devices[0])

    def add_device(
        self,
        seed_device: Device | None = None,
        seed_utilisation: pd.DataFrame | None = None,
    ) -> None:
        """
        Creates a new device when called.

        :param: seed_device
            If specified, the :class:`clover.load.load.Device` to use to determine
            parameters for the device.

        :param: seed_utilisation
            If specified, the seed device utilisation profile.

        """

        if seed_device is None:
            # Determine the name of the new device
            new_name = "New_device{suffix}"
            index = 0
            suffix = ""
            while new_name.format(suffix=suffix) in {
                entry.name.get() for entry in self.devices
            }:
                index += 1
                suffix = f"_{index}"

            new_name = new_name.format(suffix=suffix)

            # Create the new device and select it.
            self.devices.append(
                (
                    device := GUIDevice(
                        self, new_name, True, 0, 0, 0, 0, 0, DemandType.DOMESTIC
                    )
                )
            )

        else:
            self.devices.append(
                (
                    device := GUIDevice(
                        self,
                        seed_device.name,
                        seed_device.available,
                        seed_device.electric_power,
                        seed_device.initial_ownership,
                        seed_device.final_ownership,
                        seed_device.innovation,
                        seed_device.imitation,
                        seed_device.demand_type,
                        seed_device.clean_water_usage,
                    )
                )
            )

        self.active_device = device

        # Add a new set of buttons for the device
        self.devices_frame.device_active_buttons[device] = ttk.Checkbutton(
            self.devices_frame,
            style=f"{SUCCESS}.{OUTLINE}.{TOOLBUTTON}",
            variable=device.active,
        )
        self.devices_frame.device_active_buttons[device].grid(
            row=len(self.devices_frame.device_active_buttons), column=0, padx=10, pady=5
        )

        self.devices_frame.device_selected_buttons[device] = ttk.Button(
            self.devices_frame,
            text=device.name.get().capitalize(),
            style=f"{SUCCESS}",
            command=lambda device=device: self.select_device(device),
        )
        self.devices_frame.device_selected_buttons[device].grid(
            row=len(self.devices_frame.device_selected_buttons),
            column=1,
            padx=10,
            pady=5,
            sticky="w",
        )

        # Set the other device-selected buttons to look disabled.
        self.select_device(device)

        # Update the screen
        self.devices_frame.update()
        self.update_device_settings_frame(device)

    def update_device_settings_frame(self, device: GUIDevice) -> None:
        """Updates the information for the device currently being considered."""

        self.settings_frame.name_entry.configure(textvariable=device.name)
        self.settings_frame.electric_power_entry.configure(
            textvariable=device.electric_power
        )
        self.settings_frame.initial_ownership_entry.configure(
            textvariable=device.initial_ownership
        )
        self.settings_frame.final_ownership_entry.configure(
            textvariable=device.final_ownership
        )
        self.settings_frame.innovation_entry.configure(textvariable=device.innovation)
        self.settings_frame.imitation_entry.configure(textvariable=device.imitation)
        self.settings_frame.clean_water_consumption_entry.configure(
            textvariable=device.clean_water_consumption
        )

    def select_device(self, device: GUIDevice) -> None:
        """Called to select a device in the left-hand devices pane."""
        for button in self.devices_frame.device_selected_buttons.values():
            button.configure(style="success.Outline.TButton")
        self.active_device = device
        self.devices_frame.device_selected_buttons[self.active_device].configure(
            style="success.TButton"
        )
        self.update_device_settings_frame(device)

    def set_loads(
        self,
        device_utilisations: dict[Device, pd.DataFrame],
    ) -> None:
        """
        Set the load information for the frame based on the inputs provided.

        :param: device_utilisations
            A mapping between the devices and the device utilisations.

        """

        # Delete and forget the old devices buttons.
        for old_device in self.devices:
            old_active_button = self.devices_frame.device_active_buttons.pop(old_device)
            old_active_button.grid_forget()

            old_selected_button = self.devices_frame.device_selected_buttons.pop(
                old_device
            )
            old_selected_button.grid_forget()

        self.devices: list[GUIDevice] = []

        for device, utilisation in device_utilisations.items():
            # Create a GUI for the device
            self.add_device(device, utilisation)

        self.active_device = self.devices[0]
        self.select_device(self.active_device)

    def update_button_label(self, _) -> None:
        """Updates the button label of the active device."""

        self.devices_frame.device_selected_buttons[self.active_device].configure(
            text=self.active_device.name.get().capitalize()
        )
        self.active_device.name.set(self.active_device.name.get().replace(" ", "_"))
