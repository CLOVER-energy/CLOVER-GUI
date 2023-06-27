#!/usr/bin/python3.10
########################################################################################
# details.py - The details module for CLOVER-GUI application.                          #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import tkinter as tk

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from ..__utils__ import DETAILS_GEOMETRY

__all__ = ("GridFrame",)


class GridFrame(ttk.Frame):
    """
    Represents the Grid frame.

    Contains settings for grid connection.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=6)

        for index in range(3):
            self.columnconfigure(index, weight=1)

        # Grid-profile combobox
        self.grid_profile_name = tk.StringVar(value="all")

        self.grid_profile_values = {
            "all": self.grid_profile_name,
            "none": tk.StringVar(value="none"),
            "eight-hours": tk.StringVar(value="eight-hours"),
        }

        self.grid_profile_combobox = ttk.Combobox(
            self, bootstyle=SUCCESS, textvariable=self.grid_profile_name
        )
        self.grid_profile_combobox.grid(
            row=0, column=0, padx=10, pady=5, sticky="w", ipadx=60
        )
        self.populate_available_profiles()

        # Grid profile name
        self.grid_profile_label = ttk.Label(self, text="Profile name")
        self.grid_profile_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.grid_profile_entry = ttk.Entry(
            self, bootstyle=SUCCESS, textvariable=self.grid_profile_name
        )
        self.grid_profile_entry.grid(
            row=0, column=2, padx=10, pady=5, sticky="ew", ipadx=80
        )
        self.grid_profile_entry.bind("<Return>", self.enter_grid_profile_name)
        self.grid_profile_combobox.bind(
            "<<ComboboxSelected>>", self.select_grid_profile
        )

        # Graph
        self.graph_frame = ttk.Labelframe(
            self,
            style="success.TLabelframe",
        )
        self.graph_frame.grid(
            row=1,
            column=0,
            columnspan=3,
            padx=5,
            pady=10,
            ipady=100,
            ipadx=20,
            sticky="news",
        )

        self.graph_frame.rowconfigure(0, weight=10)
        self.graph_frame.rowconfigure(1, weight=1)
        self.graph_frame.rowconfigure(2, weight=1)

        for index in range(25):
            self.graph_frame.columnconfigure(index, weight=1)

        self.update_graph_frame_label()

        self.probabilities: dict[int, ttk.DoubleVar] = {
            hour: ttk.DoubleVar(self.graph_frame, 0.3) for hour in range(24)
        }
        self.probability_sliders: dict[int, ttk.Scale] = {}
        self.probabilitiy_entries: dict[int, ttk.Entry] = {}

        def enter_probability(hour):
            self.probabilities[hour].set(
                max(min(float(self.probabilitiy_entries[hour].get()), 1), 0)
            )
            self.probability_sliders[hour].set(self.probabilities[hour].get())

        for hour in range(24):
            self.probability_sliders[hour] = ttk.Scale(
                self.graph_frame,
                from_=1,
                to=0,
                value=self.probabilities[hour].get(),
                variable=self.probabilities[hour],
                style=SUCCESS,
                orient=VERTICAL,
                length=300,
            )
            self.probability_sliders[hour].grid(
                row=0, column=hour, padx=0, pady=5, sticky="ns"
            )

            self.probabilitiy_entries[hour] = ttk.Entry(
                self.graph_frame,
                bootstyle=SUCCESS,
                textvariable=self.probabilities[hour],
                width=4,
            )
            self.probabilitiy_entries[hour].grid(
                row=1, column=hour, padx=0, pady=5, sticky="ew"
            )
            self.probabilitiy_entries[hour].bind(
                "<Return>", lambda _, hour=hour: enter_probability(hour)
            )

        self.x_axis_label = ttk.Label(self.graph_frame, text="Hour of the day")
        self.x_axis_label.grid(row=2, column=11, columnspan=3, sticky="ew")

        # TODO: Add configuration frame widgets and layout

    def enter_grid_profile_name(self, _) -> None:
        old_profile_name: str = (
            inverse_map := {
                value.get(): key for key, value in self.grid_profile_values.items()
            }
        )[self.grid_profile_name.get()]
        old_combobox_variable = self.grid_profile_values.pop(old_profile_name)
        old_combobox_variable.set(self.grid_profile_name.get())
        self.grid_profile_name = old_combobox_variable
        self.grid_profile_values[self.grid_profile_name.get()] = self.grid_profile_name

        self.populate_available_profiles()
        self.update_graph_frame_label()
        # FIXME - This code isn't updating the combobox correctly.

    def populate_available_profiles(self) -> None:
        self.grid_profile_combobox["values"] = [
            entry for entry in self.grid_profile_values
        ]

    def select_grid_profile(self, _) -> None:
        self.grid_profile_name = self.grid_profile_values[
            self.grid_profile_combobox.get()
        ]

    def update_graph_frame_label(self) -> None:
        self.graph_frame.configure(
            text="Hourly probability of grid availability for grid "
            f"'{self.grid_profile_name.get().capitalize()}'."
        )
