#!/usr/bin/python3.10
########################################################################################
# system.py - The system module for CLOVER-GUI application.                            #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 11/07/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import ttkbootstrap as ttk

from clover.simulation.energy_system import Minigrid, Scenario
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *


__all__ = ("SystemFrame",)


class SystemFrame(ttk.Frame):
    """
    Represents the System frame.

    Contains System inputs for the system.

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
        self.rowconfigure(9, weight=1)
        self.rowconfigure(10, weight=1)
        self.rowconfigure(11, weight=1)
        self.rowconfigure(12, weight=1)
        self.rowconfigure(13, weight=1)
        self.rowconfigure(14, weight=1)
        self.rowconfigure(15, weight=1)
        self.rowconfigure(16, weight=1)
        self.rowconfigure(17, weight=1)
        self.rowconfigure(18, weight=1)
        self.rowconfigure(19, weight=1)
        self.rowconfigure(20, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=1)

    def set_system(self, minigrid: Minigrid, scenarios: list[Scenario]) -> None:
        """
        Sets the scenarios on the system frame.

        """

        pass
