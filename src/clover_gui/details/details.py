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

__all__ = ("DetailsWindow",)

from .conversion import ConversionFrame
from .diesel import DieselFrame
from .finance import FinanceFrame
from .ghgs import GHGFrame
from .grid import GridFrame
from .load import LoadFrame
from .storage import StorageFrame
from .solar import SolarFrame
from .system import SystemFrame
from .transmission import TransmissionFrame
from .wind import WindFrame


class DetailsWindow(tk.Toplevel):
    """
    Represents the details window.

    The details window contains tabs for inputting more precise information into the
    application.

    TODO: Update attributes.

    """

    def __init__(self, system_lifetime: ttk.IntVar) -> None:
        """
        Instantiate a :class:`DetailsWindow` instance.

        :param: system_lifetime
            The lifetime of the system.

        """

        super().__init__()

        self.title("CLOVER-GUI Details")

        self.system_lifetime = system_lifetime

        self.geometry(DETAILS_GEOMETRY)

        self.protocol("WM_DELETE_WINDOW", self.save_and_close)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.details_label = ttk.Label(
            self, bootstyle=SECONDARY, text="Detailed settings", font="80"
        )
        self.details_label.grid(row=0, column=0, sticky="w", padx=20, pady=5)

        self.details_notebook = ttk.Notebook(self, bootstyle=f"{SECONDARY}")
        self.details_notebook.grid(
            row=1, column=0, sticky="nsew", padx=20, pady=5
        )  # Use grid

        style = ttk.Style()
        style.configure("TNotebook.Tab", width=int(self.winfo_screenwidth() / 8))

        self.solar_frame = SolarFrame(self.details_notebook)
        self.details_notebook.add(self.solar_frame, text="Solar", sticky="news")

        self.wind_frame = WindFrame(self.details_notebook)
        self.details_notebook.add(
            self.wind_frame, text="Wind", sticky="news", state=DISABLED
        )

        self.storage_frame = StorageFrame(self.details_notebook)
        self.details_notebook.add(self.storage_frame, text="Storage", sticky="news")

        self.load_frame = LoadFrame(self.details_notebook)
        self.details_notebook.add(self.load_frame, text="Load", sticky="news")

        self.conversion_frame = ConversionFrame(self.details_notebook)
        self.details_notebook.add(
            self.conversion_frame, text="Convert", sticky="news", state=DISABLED
        )

        self.transmission_frame = TransmissionFrame(self.details_notebook)
        self.details_notebook.add(
            self.transmission_frame, text="Transmit.", sticky="news", state=DISABLED
        )

        self.diesel_frame = DieselFrame(self.details_notebook)
        self.details_notebook.add(self.diesel_frame, text="Diesel", sticky="news")

        self.grid_frame = GridFrame(self.details_notebook)
        self.details_notebook.add(self.grid_frame, text="Grid", sticky="news")

        self.finance_frame = FinanceFrame(self.details_notebook)
        self.details_notebook.add(self.finance_frame, text="Finance", sticky="news")

        self.ghgs_frame = GHGFrame(self.details_notebook)
        self.details_notebook.add(self.ghgs_frame, text="GHGs", sticky="news")

        self.system_frame = SystemFrame(self.details_notebook)
        self.details_notebook.add(self.system_frame, text="System", sticky="news")

    def save_and_close(self) -> None:
        """Actioned when closed."""

        # Save all of the variables from the details screen.

        self.withdraw()
