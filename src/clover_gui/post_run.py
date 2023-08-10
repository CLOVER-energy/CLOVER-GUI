#!/usr/bin/python3.10
########################################################################################
# post_run.py - The post-run module for CLOVER-GUI application.                        #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 23/06/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import tkinter as tk

from typing import Callable

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen


__all__ = ("PostRunScreen",)


class PostRunScreen(BaseScreen, show_navigation=True):
    """
    Represents the post-run screen.

    The post-run screen contains options for a user when a CLOVER run has completed.

    TODO: Update attributes.

    """

    def __init__(
        self,
        open_configuration_screen: Callable,
        open_load_location_post_run: Callable,
        open_new_location_post_run: Callable,
    ) -> None:
        """
        Instantiate a :class:`ConfigureFrame` instance.

        :param: open_configuration_screen
            Function that opens the configuration screen.

        :param: open_load_location_post_run
            Function that opens the load-location window post-run.

        :param: open_new_location_post_run
            Function that opens the new-location screen post-run.

        """

        super().__init__()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=4)
        self.columnconfigure(4, weight=4)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=2)
        self.rowconfigure(5, weight=1)

        self.finished_label = ttk.Label(
            self, bootstyle=INFO, text="CLOVER RUN FINISHED", font="80"
        )
        self.finished_label.grid(
            row=0, column=0, columnspan=5, sticky="ew", padx=60, pady=20
        )

        self.go_back_prefix = ttk.Label(self, text="You can go back and ")
        self.go_back_prefix.grid(
            row=1, column=0, columnspan=3, sticky="e", padx=10, pady=5
        )

        self.configure_button = ttk.Button(
            self,
            bootstyle=f"{INFO}-inverted",
            text="Re-configure/re-run",
            command=open_configuration_screen,
        )
        self.configure_button.grid(row=1, column=3, sticky="ew", padx=10, pady=5)

        self.go_back_suffix = ttk.Label(self, text=" the same location;")
        self.go_back_suffix.grid(row=1, column=4, sticky="w", padx=10, pady=5)

        self.new_location_prefix = ttk.Label(self, text="Create a ")
        self.new_location_prefix.grid(
            row=2, column=0, columnspan=3, sticky="e", padx=10, pady=5
        )

        self.new_location_button = ttk.Button(
            self,
            bootstyle=f"{INFO}-inverted",
            text="New location",
            command=open_new_location_post_run,
        )
        self.new_location_button.grid(row=2, column=3, sticky="ew", padx=10, pady=5)

        self.load_location_prefix = ttk.Label(self, text="Or ")
        self.load_location_prefix.grid(
            row=3, column=0, columnspan=3, sticky="e", padx=10, pady=5
        )

        self.load_location_button = ttk.Button(
            self,
            bootstyle=f"{INFO}-inverted",
            text="Load a location",
            command=open_load_location_post_run,
        )
        self.load_location_button.grid(row=3, column=3, sticky="ew", padx=10, pady=5)

        self.back_button = ttk.Button(
            self,
            text="Back",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_back(self),
        )
        self.back_button.grid(row=5, column=0, padx=10, pady=5)

        self.home_button = ttk.Button(
            self,
            text="Home",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_home(self),
        )
        self.home_button.grid(row=5, column=1, padx=10, pady=5)

        self.forward_button = ttk.Button(
            self,
            text="Forward",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_forward(self),
        )
        self.forward_button.grid(row=5, column=2, padx=10, pady=5)
