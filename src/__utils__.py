#!/usr/bin/python3.10
########################################################################################
# __utils__.py - The utility module for CLOVER-GUI application.                        #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import abc
import tkinter as tk

__all__ = ("BaseScreen")

class BaseScreen(tk.Toplevel, abc.ABC):
    """
    Abstract class that represents a screen within the CLOVER-GUI application.

    """

    # Private attributes:
    #   .. attribute:: _backward_journey
    #       Keeps track of the backward journey within the GUI.
    #
    #   .. attribute:: _forward_journey
    #       Keeps track of the forward journey within the GUI if applicable.
    #

    _backward_journey: list = []
    _forward_journey: list = []

    def __init__(self, parent) -> None:
        """Instnatiate the screen."""
        tk.Toplevel(self, parent)

    def __init_subclass__(cls, show_navigation: bool) -> None:
        """
        Sub-class hook to ensure that forward and backward navigation are present if
        applicable.

        :param: show_navigation

        """

        return super().__init_subclass__()