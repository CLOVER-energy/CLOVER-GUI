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

import tkinter as tk

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import DETAILS_GEOMETRY

__all__ = ("DetailsWindow",)


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

        self.columnconfigure(0, weight=2)  # First row has the header
        self.columnconfigure(1, weight=2)  # These rows have entries
        self.columnconfigure(2, weight=1)  # These rows have entries

        self.pv_panel_entry = ttk.Combobox(self, bootstyle="primary")
        self.pv_panel_entry.grid(row=0, column=0, padx=10, pady=5, sticky="w", ipadx=60)
        self.populate_available_panels()

        self.renewables_ninja_token = tk.StringVar(value="YOUR API TOKEN")
        self.renewables_ninja_token_entry = ttk.Entry(
            self,
            bootstyle=f"{WARNING}-inverted",
            state="disabled",
            textvariable=self.renewables_ninja_token,
        )
        self.renewables_ninja_token_entry.grid(
            row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew", ipadx=80
        )

        # Panel name
        self.panel_name_label = ttk.Label(self, text="Panel name")
        self.panel_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.panel_name_variable = tk.StringVar(value="m-Si")
        self.panel_name_entry = ttk.Entry(
            self, bootstyle=PRIMARY, textvariable=self.panel_name_variable
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
            bootstyle=SUCCESS,
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

        def scalar_tilt(e):
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
            bootstyle=DANGER,
            variable=self.panel_orientation,
        )
        self.panel_orientation_entry.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

        # Panel present in the system
        self.panel_present_label = ttk.Label(self, text="Panel present")
        self.panel_present_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.reference_efficiency_label = ttk.Label(self, text="Panel name")
        self.reference_efficiency_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        self.reference_temperature_label = ttk.Label(self, text="Panel name")
        self.reference_temperature_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        self.thermal_coefficient_label = ttk.Label(self, text="Panel name")
        self.thermal_coefficient_label.grid(
            row=6, column=0, padx=10, pady=5, sticky="w"
        )

        # TODO: Add configuration frame widgets and layout

    def populate_available_panels(self) -> None:
        """Populate the combo box with the set of avialable panels."""

        self.pv_panel_entry["values"] = ["m-Si"]


class StorageFrame(ttk.Frame):
    """
    Represents the Storage frame.

    Contains settings for storage units.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Storage frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class LoadFrame(ttk.Frame):
    """
    Represents the Load frame.

    Contains settings for load management.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Load frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class DieselFrame(ttk.Frame):
    """
    Represents the Diesel frame.

    Contains settings for diesel generators.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Diesel frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class GridFrame(ttk.Frame):
    """
    Represents the Grid frame.

    Contains settings for grid connection.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Grid frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class FinanceFrame(ttk.Frame):
    """
    Represents the Finance frame.

    Contains settings for financial analysis.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Finance frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class GHGFrame(ttk.Frame):
    """
    Represents the GHG frame.

    Contains settings for greenhouse gas emissions.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="GHGs frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class SystemFrame(ttk.Frame):
    """
    Represents the System frame.

    Contains settings for system configuration.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="System frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout


class DetailsWindow(tk.Toplevel):
    """
    Represents the details window.

    The details window contains tabs for inputting more precise information into the
    application.

    TODO: Update attributes.

    """

    def __init__(
        self,
    ) -> None:
        """
        Instantiate a :class:`DetailsWindow` instance.

        """

        super().__init__()

        self.title("CLOVER-GUI Details")

        self.geometry(DETAILS_GEOMETRY)

        self.protocol("WM_DELETE_WINDOW", self.withdraw)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.details_label = ttk.Label(
            self, bootstyle=SECONDARY, text="Detailed settings", font="80"
        )
        self.details_label.grid(row=0, column=0, sticky="w", padx=60, pady=5)

        self.details_notebook = ttk.Notebook(self, bootstyle=f"{SECONDARY}")
        self.details_notebook.grid(
            row=1, column=0, sticky="nsew", padx=60, pady=5
        )  # Use grid

        style = ttk.Style()
        style.configure("TNotebook.Tab", width=int(self.winfo_screenwidth() / 8))

        self.solar_frame = SolarFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Solar", sticky="news")

        self.solar_frame = StorageFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Storage", sticky="news")

        self.solar_frame = LoadFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Load", sticky="news")

        self.solar_frame = DieselFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Diesel", sticky="news")

        self.solar_frame = GridFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Grid", sticky="news")

        self.solar_frame = FinanceFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Finance", sticky="news")

        self.solar_frame = GHGFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="GHGs", sticky="news")

        self.solar_frame = SystemFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="System", sticky="news")
