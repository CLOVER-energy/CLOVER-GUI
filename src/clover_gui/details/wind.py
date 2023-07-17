#!/usr/bin/python3.10
########################################################################################
# wind.py - The wind module for CLOVER-GUI application.                                #
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


__all__ = ("WindFrame",)


class WindFrame(ttk.Frame):
    """
    Represents the Wind frame.

    Contains settings for wind configuration.

    TODO: Update attributes.

    """

    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text="Wind frame")
        self.label.grid(row=0, column=0)

        # TODO: Add configuration frame widgets and layout
