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

from dataclasses import dataclass
from typing import Callable

import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import *
from ttkbootstrap.tooltip import ToolTip

from .__utils__ import BaseScreen


__all__ = ("PostRunScreen",)


@dataclass
class Output:
    """
    Represents an output that can be displayed.

    .. attribute:: available
        Whether the output is available for viewing.

    .. attribute:: filepath
        The filepath to the output.

    .. attribute:: title
        The title of the plot to display.

    """

    available: ttk.BooleanVar
    filepath: ttk.StringVar
    title: ttk.StringVar


class OutputsSelectionFrame(ScrolledFrame):
    """
    Represents the scrollable frame where outputs can be selected for viewing.

    TODO: Update attributes.

    """

    def __init__(
        self, parent, select_output: Callable, update_outputs_viewer_frame: Callable
    ):
        super().__init__(parent)

        # Duplicate functional call
        self.update_outputs_viewer_frame = update_outputs_viewer_frame

        self.output_selected_buttons: dict[Output, ttk.Button] = {
            output: ttk.Button(
                self,
                command=lambda output=output: select_output(output),
                style=f"{SUCCESS}.{OUTLINE}",
                text=output.title.get().capitalize(),
            )
            for output in parent.outputs
        }

        # Configure column and row weights
        for row_index in range(self.output_selected_buttons):
            self.rowconfigure(row_index, weight=1)

        self.columnconfigure(0, weight=1)

        for index, output in enumerate(self.output_selected_buttons.keys()):
            (button:=self.output_selected_buttons[output]).grid(row=index, column=0, padx=10, pady=5, sticky="ew")

            # Disable the button if the output isn't available.
            if not output.available.get():
                button.configure(state=DISABLED)
                ToolTip(
                    button,
                    style=f"{INFO}.{OUTLINE}",
                    text="This output can't be viewed. This is likely due to it not\n""being applicable to the type of CLOVER run you launched.",
                )


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

        self.rowconfigure(0, weight=1, minsize=40)
        self.rowconfigure(1, weight=1, minsize=40)
        self.rowconfigure(2, weight=1, minsize=550)
        self.rowconfigure(3, weight=1, minsize=80)

        # Finished label
        self.finished_label = ttk.Label(
            self, bootstyle=INFO, text="CLOVER RUN FINISHED", font="80"
        )
        self.finished_label.grid(
            row=0, column=0, sticky="ew", padx=60, pady=20
        )

        # Next-step options
        self.next_steps_frame = ttk.Frame(self)
        self.next_steps_frame.grid(row=1, column=0, sticky="news", padx=60, pady=20)

        self.next_steps_frame.columnconfigure(0, weight=1)
        self.next_steps_frame.columnconfigure(1, weight=1)
        self.next_steps_frame.columnconfigure(2, weight=1)
        self.next_steps_frame.columnconfigure(3, weight=1)

        self.next_steps_frame.rowconfigure(0, weight=1)

        self.next_steps_label = ttk.Label(self.next_steps_frame, text="Next steps:")
        self.next_steps_label.grid(
            row=0, column=0, sticky="ew", padx=(0, 10), pady=5
        )

        self.configure_button = ttk.Button(
            self.next_steps_frame,
            bootstyle=f"{INFO}-inverted",
            text="Re-configure/re-run\nthe same location",
            command=open_configuration_screen,
        )
        self.configure_button.grid(row=0, column=1, sticky="news", padx=10, pady=5)

        self.new_location_button = ttk.Button(
            self.next_steps_frame,
            bootstyle=f"{INFO}-inverted",
            text="Create a new location",
            command=open_new_location_post_run,
        )
        self.new_location_button.grid(row=0, column=2, sticky="news", padx=10, pady=5)

        self.load_location_button = ttk.Button(
            self.next_steps_frame,
            bootstyle=f"{INFO}-inverted",
            text="Load a different location",
            command=open_load_location_post_run,
        )
        self.load_location_button.grid(row=0, column=3, sticky="news", padx=(10, 0), pady=5)

        # Output viewer
        self.outputs_frame = ttk.Frame(self)
        self.outputs_frame.grid(row=2, column=0, sticky="news")

        self.

        # Navigation buttons
        self.bottom_bar_frame = ttk.Frame(self)
        self.bottom_bar_frame.grid(row=3, column=0, sticky="news")

        self.bottom_bar_frame.columnconfigure(0, weight=1)
        self.bottom_bar_frame.columnconfigure(1, weight=1)
        self.bottom_bar_frame.columnconfigure(2, weight=1)
        self.bottom_bar_frame.columnconfigure(3, weight=10)
        self.bottom_bar_frame.columnconfigure(4, weight=1)

        self.bottom_bar_frame.rowconfigure(0, weight=1)

        self.back_button = ttk.Button(
            self.bottom_bar_frame,
            text="Back",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_back(self),
        )
        self.back_button.grid(
            row=0, column=0, padx=(60, 20), pady=(10, 20), sticky="news"
        )

        self.home_button = ttk.Button(
            self.bottom_bar_frame,
            text="Home",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_home(self),
        )
        self.home_button.grid(row=0, column=1, padx=20, pady=(10, 20), sticky="news")

        self.forward_button = ttk.Button(
            self.bottom_bar_frame,
            text="Forward",
            bootstyle=f"{PRIMARY}-{OUTLINE}",
            command=lambda self=self: BaseScreen.go_forward(self),
        )
        self.forward_button.grid(row=0, column=2, padx=20, pady=(10, 20), sticky="news")

    def _select_output(self, output: Output) -> None:
        """
        Select the output for viewing..

        :param: output
            The output to select.

        """

        pass
