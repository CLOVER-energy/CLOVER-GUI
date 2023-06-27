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

from .grid import GridFrame
from .load import LoadFrame
from .storage import StorageFrame
from .solar import SolarFrame


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
        self.details_label.grid(row=0, column=0, sticky="w", padx=20, pady=5)

        self.details_notebook = ttk.Notebook(self, bootstyle=f"{SECONDARY}")
        self.details_notebook.grid(
            row=1, column=0, sticky="nsew", padx=20, pady=5
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
