#!/usr/bin/python3.10
########################################################################################
# __init__.py - The init module for CLOVER-GUI application.                            #
#                                                                                      #
# Author: Ben Winchester, Hamish Beath                                                 #
# Copyright: Ben Winchester, 2022                                                      #
# Date created: 19/07/2023                                                             #
# License: MIT, Open-source                                                            #
# For more information, contact: benedict.winchester@gmail.com                         #
########################################################################################

import tkinter as tk

# from tkinter.messagebox import showwarning
# import subprocess
# import xterm
import ttkbootstrap as ttk

from typing import Callable

from clover import Simulation

from clover.scripts.clover import clover_main
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *

from .__utils__ import BaseScreen

__all__ = ("RunScreen",)


class RunScreen(ttk.Frame):

    """
    Represents the Run Screen.

    Displays running information when CLOVER is running simulation or optimisation.

    """

    def __init__(
        self,
        data_directory: str,
    ) -> None:
        """
        Instantiate a :class:`RunFrame` instance.

        :param: data_directory
            The path to the data directory.

        """

        super().__init__()

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # root = tk.Tk()
        # root.geometry("600x500")

        # label = tk.Label(root, text="CLOVER is running.")
        # label.pack(fill=tk.X)

        # xterm_frame = tk.Frame(root)
        # xterm_frame.pack(fill=tk.BOTH, expand=True)

        # xterm_frame_id = xterm_frame.winfo_id()

        # try:
        #     p = subprocess.Popen(
        #         ["xterm", "-into", str(xterm_frame_id), "-geometry", "80x20"],
        #         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        # except FileNotFoundError:
        #     showwarning("Error", "xterm is not installed")
        #     raise SystemExit

        # root.mainloop()
