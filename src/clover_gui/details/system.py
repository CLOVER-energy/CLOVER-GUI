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

        """
        ac_transmission_efficiency: 0.95 # Efficiency of AC distribution network
        dc_transmission_efficiency: 0.95 # Efficiency of DC distribution network
        battery: default_battery
        # clean_water_tank: cold_water_tank
        conversion:
        dc_to_ac: 0.95 # Conversion efficiency (0.0-1.0)
        dc_to_dc: 0.95 # Conversion efficiency (0.0-1.0)
        ac_to_dc: 0.8 # Conversion efficiency (0.0-1.0)
        ac_to_ac: 0.98 # Conversion efficiency (0.0-1.0)
        diesel_generator: default_diesel
        # heat_exchanger: default_heat_exchanger
        # hot_water_tank: hot_water_tank
        pv_panel: default_pv
        # pvt_panel: default_pvt
        
        """

        # AC transmission efficiency
